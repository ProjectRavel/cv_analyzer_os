from typing import Any

class ResponseModel:
    def __init__(self, status_code: int, message: str, data: Any = None):
        self.status_code = status_code
        self.message = message
        self.data = data or {}

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data
        }