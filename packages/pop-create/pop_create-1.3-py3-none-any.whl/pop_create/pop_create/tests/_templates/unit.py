def test_cli(mock_hub, hub):
    mock_hub.R__CLEAN_NAME__.init.cli = hub.R__CLEAN_NAME__.init.cli
    mock_hub.R__CLEAN_NAME__.init.cli()
    mock_hub.pop.config.load.assert_called_once_with(
        ["R__CLEAN_NAME__"], "R__CLEAN_NAME__"
    )
