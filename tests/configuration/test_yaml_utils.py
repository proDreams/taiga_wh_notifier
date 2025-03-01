from src.core.settings import get_strings


class TestYamlUtils:
    def test_get_strings(self):
        expected = "Hello, world!"
        result = get_strings()

        assert expected == result.get("yaml_test").get("Example").strip()
