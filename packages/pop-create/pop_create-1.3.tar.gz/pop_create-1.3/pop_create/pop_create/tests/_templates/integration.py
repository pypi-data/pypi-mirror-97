from unittest import mock


def test_cli(hub):
    with mock.patch("sys.argv", ["R__NAME__"]):
        hub.R__CLEAN_NAME__.init.cli()
