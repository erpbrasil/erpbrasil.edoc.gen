import shutil
from pathlib import Path
import click
import os
import sys
import re
import subprocess


DOC_CONTENT = """Module contents
=================

"""
DOCS_MODULE_DOCUMENTATION = """.. automodule:: %s
    :members:
    :undoc-members:
    :show-inheritance:
"""

FILE_SKIP = ['^tipos.*', '^xmldsig.*']


def prepare(service_name, version, dest_dir, force):
    """ Create the module l10n_br_spec_<service_name> with the structure:
    l10n_br_spec_<service_name>
    |-__manifest__.py
    |-__init__.py
    |-models
      |-__init__.py
      |-spec_models.py
      |-<version>
    |-security
      |-<version>
        |-ir.model.access.csv
    """
    version = version.replace('.', '_')
    dest_dir_path = os.path.join(dest_dir, '%slib/' % service_name)
    output_path = os.path.join(dest_dir_path, version)
    doc_path = os.path.join(dest_dir_path, 'docs')

    if force and os.path.isdir(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.makedirs(output_path, exist_ok=True)

    Path(os.path.join(output_path, '__init__.py')).touch()
    Path(os.path.join(dest_dir_path, '__init__.py')).touch()

    os.makedirs(doc_path, exist_ok=True)
    with open(os.path.join(doc_path, 'module_contents.txt'), 'w+') as f:
        f.write(DOC_CONTENT)

    if os.path.isfile(os.path.join(doc_path, 'conf.py')):
        with open(os.path.join(doc_path, 'conf.py'), 'w+') as f:
            if not re.findall(r'{}'.format(output_path), f.read()):
                f.write("sys.path.append(os.path.abspath('../{}'))".format(
                    os.path.join(('%slib' % service_name), version)
                ))
    else:
        with open(os.path.join(doc_path, 'conf.py'), 'w+') as f:
            f.write("sys.path.append(os.path.abspath('../{}'))".format(
                os.path.join(('%slib' % service_name), version)
            ))


def generate_file(service_name, version, output_dir, module_name, filename,
        dest_dir, schema_version_dir):
    """ Generate the odoo model for the xsd passed by filename
    To further information see the implementation of
    gends_run_gen_odoo.generate"""

    out_process_includes_dir = schema_version_dir
    out_file_process_included = str(os.path.join(
        out_process_includes_dir, "pre_%s.xsd" % (module_name,)
    ))
    os.makedirs(out_process_includes_dir, exist_ok=True)

    out_file_generated = os.path.join(
        output_dir, "%s.py" % (module_name,))

    gends_args = ['generateDS.py',
         '--no-namespace-defs',
         '--member-specs', 'list',
         '--use-getter-setter=none', '-f', '-o',
         out_file_generated, str(filename)]
    print(" ".join(gends_args))
    subprocess.check_output(gends_args, cwd=schema_version_dir)

    dest_dir_path = os.path.join(dest_dir, '%slib/' % service_name)
    doc_path = os.path.join(dest_dir_path, 'docs')

    with open(os.path.join(doc_path, 'module_contents.txt'), 'a') as f:
        f.write(DOCS_MODULE_DOCUMENTATION % module_name)


@click.command()
@click.option('-n', '--service_name', help="Service Name")
@click.option('-v', '--version', help="Version Name")
@click.option('-s', '--schema_dir', help="Schema dir",
              default='/tmp/generated/schemas')
@click.option('-f', '--force', is_flag=True, help="force")
@click.option('-d', '--dest_dir', required=False,
              default='/tmp/generated/python',
              type=click.Path(dir_okay=True, file_okay=False, exists=False),
              multiple=False, help="Directory where the files will be extract")
@click.option('-i', '--file_filter', help="File Filter", default='')
def generate_python(service_name, version, schema_dir, force, dest_dir,
                    file_filter):
    """ Create a module in the path dest_dir and generates the python lib for
    each xsd found in the path schema_dir

    :param service_name: for example nfe
    :param version: v4.00
    :param schema_dir: /tmp/schemas
    :param force: flag
    :param dest_dir: /tmp/generated_specs
    :return:
    """
    os.makedirs(dest_dir, exist_ok=True)

    prepare(service_name, version, dest_dir, force)

    version = version.replace('.', '_')
    dest_dir_path = os.path.join(dest_dir, '%slib/' % service_name)
    output_path = os.path.join(dest_dir_path, version)
    schema_version_dir = schema_dir + '/%s/%s' % (service_name,
            version.replace('.', '_'),)

    filenames = []
    if file_filter:
        for pattern in file_filter.strip('\'').split('|'):
            filenames += [file for file in Path(schema_version_dir
            ).rglob(pattern + '*.xsd')]
    else:
        filenames = [f for f in Path(schema_version_dir).rglob('*.xsd')]

    for filename in filenames:
        module_name = str(filename).split('/')[-1].split('_v')[0]
        if not any(re.search(pattern, module_name) for pattern in FILE_SKIP):
            generate_file(service_name, version, output_path,
                          module_name, filename, dest_dir, schema_version_dir)

    src_dir = os.path.join(dest_dir, 'src', 'nfe')
    if os.path.isdir(src_dir):
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(output_path, item)
            shutil.copy2(s, d)

if __name__ == "__main__":
    sys.exit(generate_python())
