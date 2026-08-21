import sys

import sys


class CustomException(Exception):
    def __init__(self, error_msg):
        super().__init__(str(error_msg))

        _, _, exc_tb = sys.exc_info()

        if exc_tb is not None:
            self.line_no = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.line_no = None
            self.file_name = None

    def __str__(self):
        return (
            f"Error occurred in python script "
            f"[{self.file_name}] "
            f"at line [{self.line_no}] "
            f"error message [{self.args[0]}]"
        )

## checking if it is working or not:
# if __name__ == "__main__":
#     try:
#         a = 1/0
#         print("hello")
#     except Exception as e:
#         raise CustomException(e, sys) from e
