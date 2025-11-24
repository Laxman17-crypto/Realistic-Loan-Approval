import sys
from utils.logger import get_logger

logger = get_logger(__name__)

def error_message_detail(error, error_detail: sys):
    """
    Returns detailed error message (filename, line number, actual error)
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return f"""
    ERROR occurred in script: {file_name}
    Line number: {line_number}
    Error message: {str(error)}
    """

class CustomException(Exception):
    """
    Custom exception class that logs error with full traceback details.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
        logger.error(self.error_message)

    def __str__(self):
        return self.error_message