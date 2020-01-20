from glob import glob
import shutil
from pathlib import Path
import click
import os
import sys
from odoo import gends_run_gen_odoo
import generateDS


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
    dest_dir_path = os.path.join(dest_dir, 'l10n_br_spec_%s/' % service_name)
    output_path = dest_dir_path + 'models/' + version
    security_path = dest_dir_path + 'security/%s' % version

    if force and os.path.isdir(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.makedirs(output_path, exist_ok=True)
    output_dir = open(output_path + '/__init__.py', 'w+')
    output_dir.close()

    import_models_file = open(dest_dir_path + '__init__.py', 'w+')
    import_models_file.write('from . import models')
    import_models_file.close()

    import_version_file = open(dest_dir_path + 'models/__init__.py', 'w+')
    import_version_file.write('from . import %s' % version)
    import_version_file.close()

    manifest_file = open(dest_dir_path + '__manifest__.py', 'w+')
    manifest_file.write("""
{
    'name': '%s spec',
    'version': '12.0.1.0.0',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'summary': '%s spec',
    'depends': ['base'],
    'data': ['security/%s/ir.model.access.csv'],
    'installable': True,
    'application': False,
}
""" % (service_name, service_name, version))
    manifest_file.close()

    spec_models_file = open(dest_dir_path + 'models/spec_models.py', 'w+')
    spec_models_file.write("""
from odoo import models, fields


class NfeSpecMixin(models.AbstractModel):
    _description = "Abstract Model"
    _inherit = 'spec.mixin'
    _name = 'spec.mixin.nfe'
    # TODO exact schema version
    # TODO tab name...

    brl_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moeda',
        compute='_compute_brl_currency_id',
        default=lambda self: self.env.ref('base.BRL').id,
    )

    def _compute_brl_currency_id(self):
        for item in self:
            item.currency_id = self.env.ref('base.BRL').id
""")
    spec_models_file.close()

    os.makedirs(security_path, exist_ok=True)
    security_dir = open(security_path + '/ir.model.access.csv', 'w+')
    security_dir.write('id,name,model_id:id,group_id:id,'
                       'perm_read,perm_write,perm_create,perm_unlink')
    security_dir.close()


def generate_file(service_name, version, output_dir, module_name, filename):
    """ Generate the odoo model for the xsd passed by filename
    To further information see the implementation of
    gends_run_gen_odoo.generate"""

    gends_run_gen_odoo.generate({
        'force': True,
        'path': str(generateDS.__file__),
        'schema_name': service_name,
        'version': version,
        'output_dir': output_dir,
        'verbose': True,
        'class_suffixes': True,
    }, str(filename))
    init_file = open(output_dir + '/__init__.py', 'a')
    init_file.write('from . import %s\n' % module_name)
    init_file.close()


def finish(output_dir):
    if os.path.isdir(os.path.join(output_dir, '__pycache__')):
        shutil.rmtree(os.path.join(output_dir, '__pycache__'))
    for file in glob(os.path.join(output_dir, '*lib.py')):
        os.remove(file)
    os.remove(os.path.join(output_dir, 'generateds_definedsimpletypes.py'))


@click.command()
@click.option('-n', '--service_name', help="Service Name")
@click.option('-v', '--version', help="Version Name")
@click.option('-s', '--schema_dir', help="Schema dir",
              default='/tmp/generated/schema')
@click.option('-f', '--force', is_flag=True, help="force")
@click.option('-d', '--dest_dir', required=False,
              default='/tmp/generated/odoo',
              type=click.Path(dir_okay=True, file_okay=False, exists=False),
              multiple=False, help="Directory where the files will be extract")
@click.option('-i', '--file_filter', help="Regex to filter xsd files",
              default='')
def generate_odoo(
        service_name, version, schema_dir, force, dest_dir, file_filter):
    """ Create a module in the path dest_dir and generates the odoo class for
    each xsd found in the path schema_dir

    :param service_name: for example nfe
    :param version: v4.00
    :param schema_dir: /tmp/schemas
    :param force: flag
    :param dest_dir: /tmp/generated_specs
    :param file_filter: Regex to filter xsd files
    :return:
    """
    version = version.replace('.', '_')
    os.makedirs(dest_dir, exist_ok=True)

    prepare(service_name, version, dest_dir, force)

    output_dir = os.path.join(
        dest_dir, 'l10n_br_spec_%s/models/%s' % (service_name, version)
    )

    filenames = []
    if file_filter:
        for pattern in file_filter.strip('\'').split('|'):
            filenames += [file for file in Path(schema_dir + '/%s/%s' % (
                service_name, version
            )).rglob(pattern + '*.xsd')]
    else:
        filenames = [file for file in Path(schema_dir + '/%s/%s' % (
            service_name, version
        )).rglob('*.xsd')]

    for filename in filenames:
        module_name = str(filename).split('/')[-1].split('_%s' % version)[0]
        generate_file(service_name, version, output_dir, module_name, filename)

    finish(output_dir)


if __name__ == "__main__":
    sys.exit(generate_odoo())
