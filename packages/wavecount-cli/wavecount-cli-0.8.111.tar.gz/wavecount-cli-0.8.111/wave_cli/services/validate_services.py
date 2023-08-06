from PyInquirer import ValidationError, Validator
from datetime import datetime


class SerialNumberValidate(Validator):
    def validate(self, document):
        if not (isinstance(document.text, str) and len(str(document.text)) >= 10):
            raise ValidationError(
                message='"{}" is not a valid serial-number. should be at least 10 characters'.format(document.text),
                cursor_position=len(document.text))
        else:
            return True


class PartNumberValidate(Validator):
    def validate(self, document):
        if not (isinstance(document.text, str) and len(str(document.text)) >= 4):
            raise ValidationError(
                message='"{}" is not a valid part-number. should be at least 40 characters'.format(document.text),
                cursor_position=len(document.text))
        else:
            return True


class DateValidate(Validator):
    def validate(self, document):
        try:
            datetime.strptime(document.text, '%Y-%m-%d')
            return True
        except ValueError:
            raise ValidationError(
                message='"{}" incorrect date format, should be <YYYY-MM-DD>'.format(document.text),
                cursor_position=len(document.text))


class StringValidate(Validator):
    def validate(self, document):
        chars_limit = 1
        if not (isinstance(document.text, str) and len(str(document.text)) >= chars_limit):
            raise ValidationError(
                message='"{}" is not a valid. should be at least {} characters'.format(document.text, chars_limit),
                cursor_position=len(document.text))
        else:
            return True


class IntValidate(Validator):
    def validate(self, document):
        digits_limit = 1
        if len(str(document.text)) < 1:
            raise ValidationError(
                message='"{}" is not valid. should be at least {} digits'.format(document.text, digits_limit),
                cursor_position=len(document.text)
            )
        try:
            int(document.text)
            return True
        except ValueError:
            raise ValidationError(
                message='"{}" is not valid. should be digit'.format(document.text),
                cursor_position=len(document.text))
