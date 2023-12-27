import logging


class TraceLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def _format_message(self, message, trace_id):
        return f"[TraceID: {trace_id}] - {message}"

    def debug(self, message, trace_id="N/A"):
        formatted_message = self._format_message(message, trace_id)
        self.logger.debug(formatted_message)

    def info(self, message, trace_id="N/A"):
        formatted_message = self._format_message(message, trace_id)
        self.logger.info(formatted_message)

    def warning(self, message, trace_id="N/A"):
        formatted_message = self._format_message(message, trace_id)
        self.logger.warning(formatted_message)

    def error(self, message, trace_id="N/A"):
        formatted_message = self._format_message(message, trace_id)
        self.logger.error(formatted_message)

    def critical(self, message, trace_id="N/A"):
        formatted_message = self._format_message(message, trace_id)
        self.logger.critical(formatted_message)

    # For backward compatibility and ease of use, keep the 'log' method as an alias for 'info'
    log = info
