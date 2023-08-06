class Handler:

    @staticmethod
    def error_information(db, exctype, value, tb):
        print(
            'db Connection',
            db)
        print(
            'My Error Information')
        print(
            'Type:', type(exctype).__name__)
        print(
            'Value:', value)
        print(
            'Traceback:', tb.format_exc().split('\n'))