from pathlib import Path
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi
import click
import os
import shutil
import sys


@click.command()
@click.option('-n', '--service_name', help="Service Name")
@click.option('-v', '--version', help="Version Name")
@click.option('-u', '--url', multiple=True, help="List of URLs")
@click.option('-t', 'tmp_dir', required=False, default='/tmp/generated',
              type=click.Path(dir_okay=True, file_okay=False, exists=False),
              multiple=False, help="Directory where the files will be extract")
def download_schema(service_name, version, url, tmp_dir):
    """ Download a list of schemas of the same service, extract it in order
    and overwrite the files.

    NFE: Has one big file with all the xsd and some small files with
        new fixes named "Pacote de Liberação"

    """

    click.echo("Downloading Schema")
    click.echo("Service: {}, Version: {}, Temp dir: {}".format(
        service_name,
        version,
        tmp_dir,
    ))

    os.makedirs(tmp_dir, exist_ok=True)

    for u in url:
        click.echo("Fetching url: {}".format(u))
        remote_file = urlopen(u)
        #
        # Get file name with extension
        #
        value, params = cgi.parse_header(
            remote_file.info()['Content-Disposition']
        )
        filename = params["filename"]
        file_path = os.path.join(tmp_dir, filename)
        click.echo("Downloading file to: {}".format(file_path))
        urlretrieve(u, file_path)
        #
        # Exaction
        #
        extract_dir = os.path.join(tmp_dir, 'extract_schema')
        shutil.unpack_archive(file_path, extract_dir)
        #
        # Move files recursive
        #

        destination_extract_dir = os.path.join(
            tmp_dir, 'schemas', service_name, version
        ).replace('.', '_')

        os.makedirs(destination_extract_dir, exist_ok=True)

        for filename in Path(extract_dir).rglob('*.xsd'):
            destination_extract_file = os.path.join(
                destination_extract_dir, str(filename).split('/')[-1]
            )
            shutil.move(filename, destination_extract_file)


if __name__ == "__main__":
    sys.exit(download_schema())
