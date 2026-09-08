import sys




import sys


class CustomException(Exception):
    def __init__(self, error_msg):
        super().__init__(str(error_msg))

        _, _, exc_tb = sys.exc_info()

        if exc_tb:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_no = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.line_no = -1

    def __str__(self):
        return (
            f"Error occurred in file '{self.file_name}', "
            f"line {self.line_no}: {self.args[0]}"
        )

## checking if it is working or not:
# if __name__ == "__main__":
#     try:
#         a = 1/0
#         print("hello")
#     except Exception as e:
#         raise CustomException(e, sys) from e
