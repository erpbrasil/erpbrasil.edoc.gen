
from erpbrasil.edoc.gen.cli import main
from erpbrasil.edoc.gen.download_schema import download_schema
from erpbrasil.edoc.gen.generate_python import generate_python
from erpbrasil.edoc.gen.generate_odoo import generate_odoo
from click.testing import CliRunner


def test_main():
    assert main([]) == 0


def test_download():
    runner = CliRunner()
    result = runner.invoke(download_schema, """ -n nfe -v v4.00 -u http://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=vdxcmJ2AgTo= -u http://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=oeQ8dVnzrYo=""")  # noqa
    assert result


def test_python():
    runner = CliRunner()
    result = runner.invoke(generate_python, """ -n nfe -v v4.00""")
    assert result


def test_odoo():
    runner = CliRunner()
    result = runner.invoke(generate_odoo, """ -n nfe -v v4.00""")
    assert result
