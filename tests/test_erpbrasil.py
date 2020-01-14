
from erpbrasil.edoc.gen.cli import main
from erpbrasil.edoc.gen.download_schema import download_schema
from click.testing import CliRunner



def test_main():
    assert main([]) == 0


def test_download():
    runner = CliRunner()
    result = runner.invoke(download_schema, """ -n nfe -v v4.00 -u http://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=vdxcmJ2AgTo= -u http://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=oeQ8dVnzrYo=""")  # noqa
    assert result
