class RollbarMixin(object):
    def __init__(self, *args, **kwargs):
        self.rollbar = kwargs.pop('rollbar', None)
        super().__init__(*args, **kwargs)

    def is_rollbar(self) -> bool:
        """
        To check if rollbar is available or not
        :return: if rollbar is available
        """
        return self.rollbar and self.rollbar.SETTINGS.get('enabled')

    def track_message(self, message: str, level: str):
        """
        To send a message to rollbar
        :param message:
        :param level: any of the following levels:
        ['critical', 'error', 'warning', 'info', 'debug', 'ignored']
        :return:
        """
        # Levels:
        if not self.is_rollbar():
            print(f"{level} - {message}")
            return

        level = level.lower()

        self.rollbar.report_message(message, level)

    def track_error(self, message: str = None):
        if not self.is_rollbar():
            raise

        self.rollbar.report_exc_info(extra_data=message, level='error')
