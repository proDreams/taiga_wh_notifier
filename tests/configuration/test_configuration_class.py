from src.core.settings import Configuration


class TestConfigurationClass:
    """
    Tests the Configuration class for correct behavior and instance management.
    """

    target_class = Configuration

    def test_single_instance(self) -> None:
        """
        Ensures that a class has only one instance.

        :raises: AssertionError: If multiple instances of the target class are actually
        """
        instance1 = self.target_class()
        instance2 = self.target_class()
        assert instance1 is instance2, "Instance1 should be equal to instance2"

    def test_state_persistence(self) -> None:
        """
        Tests the persistence of state between class instances.

        :raises AssertionError: If the settings of two instances are not equal.
        """
        instance1 = self.target_class()
        instance2 = self.target_class()
        assert instance1.settings == instance2.settings, "Settings should be equal"

    def test_settings_correct_read(self) -> None:
        """
        Tests whether the settings are read correctly.

        :raises AssertionError: If the settings are not correct.
        """
        settings = self.target_class.settings

        assert settings.WEBHOOK_PATH == "/webhook", "Webhook path should be correct"
