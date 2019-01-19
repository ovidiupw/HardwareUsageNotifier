from hardware_usage_notifier.util.logging import LOGGER_ID


def raise_exception(exception, logger):
    if logger is not None:
        logger.error(exception.message + "\n")
    raise exception


def log_click_callback_exceptions(decorated_function):
    def wrap_click_callback(self, cli_context=None, param_name=None, config_file_path=None):
        logger = None

        try:
            logger = cli_context.meta[LOGGER_ID]
        except:
            pass

        try:
            decorated_function(self, cli_context, param_name, config_file_path)
        except Exception as e:
            raise_exception(e, logger)

    return wrap_click_callback
