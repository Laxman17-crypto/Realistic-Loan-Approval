import sys
from src.utils.logger import logger

class CustomException(Exception):
    def __init__(self, error: Exception, error_detail: str = ""):
        super().__init__(str(error))
        self.error = error
        self.error_detail = error_detail

    def __str__(self):
        return f"{str(self.error)} | Details: {self.error_detail}"