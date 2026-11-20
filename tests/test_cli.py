from typer.testing import CliRunner

from izmir_open_data.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "get" in result.output
    assert "search" in result.output
    assert "datastore" in result.output


def test_cli_get_path_traversal():
    result = runner.invoke(app, ["get", "../etc/passwd"])
    assert result.exit_code != 0
    assert "Geçersiz veya güvensiz" in result.output


def test_cli_datastore_invalid_id():
    result = runner.invoke(app, ["datastore", "invalid;id"])
    assert result.exit_code != 0
    assert "Geçersiz veya güvensiz" in result.output
