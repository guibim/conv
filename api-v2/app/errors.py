class ConversionError(Exception):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnsupportedConversionError(ConversionError):
    status_code = 400


class InvalidInputError(ConversionError):
    status_code = 400


class InvalidStructureError(ConversionError):
    status_code = 422


class EncodingDetectionError(ConversionError):
    status_code = 400


class PayloadTooLargeError(ConversionError):
    status_code = 413


class ProcessingError(ConversionError):
    status_code = 500
