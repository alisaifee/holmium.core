import mock

def build_mock_mapping(name):
    mock_driver = mock.Mock()
    browser_mapping = {name:mock_driver}
    mock_driver.return_value.name = name
    return browser_mapping
