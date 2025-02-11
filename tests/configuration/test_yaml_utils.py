from unittest import TestCase

from src.core.settings import Configuration


class TestYamlUtils(TestCase):
    def test_get_strings(self):
        expected = "Hello, world!"
        result = Configuration().strings

        assert expected == result.get("yaml_test").get("Example").strip()
