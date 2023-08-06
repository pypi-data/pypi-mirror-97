from itsimodels.core.compat import string_types, text_type


class FieldValidationError(Exception):
    """Raised when a field fails to validate its value"""

    def __init__(self, value):
        """
        :param str value: the exception's error message value
        """
        super(FieldValidationError, self).__init__()

        self.value = value

    def __str__(self):
        """
        :return: the error message value
        :rtype: str
        """
        return repr(self.value)


class BaseField(object):
    """A base implementation class for a model's field definition"""

    def __init__(self, required=False, choices=None, default=None, alias=None):
        """
        :param bool required: whether the field is required
        :param tuple choices: a tuple of possible values this field can contain
        :param object default: the default value
        :param str alias: the alias name for this field
        """
        self.required = bool(required)
        self.default = default
        self.choices = choices
        self.alias = alias

    def decode(self, value):
        """
        Decodes the given value into the appropriate type

        :param value: the value
        :return: object
        """
        return value

    def validate(self, value):
        """
        Validates the given value based on the current field type

        :param value: the value to validate
        """
        if self.required and value is None:
            raise FieldValidationError('is required')


class BoolField(BaseField):
    """A field that validates boolean values"""

    def decode(self, value):
        """
        Decodes the given value into a str

        :param value: the value
        :return: bool
        """
        if value is None:
            return None

        if isinstance(value, string_types):
            value = value.lower()

        true_values = {1, '1', 'on', 't', 'true', 'yes'}

        return value in true_values

    def validate(self, value):
        """
        Validates that the given value is a boolean

        :param value: the value to validate
        """
        super(BoolField, self).validate(value)

        if value is not None and not isinstance(value, bool):
            raise FieldValidationError('should be boolean, got "{}"'.format(value))


class StringField(BaseField):
    """A field that validates string values"""

    def decode(self, value):
        """
        Decodes the given value into a str

        :param value: the value
        :return: str
        """
        return text_type(value) if value is not None else None

    def validate(self, value):
        """
        Validates that the given value is a string

        :param value: the value to validate
        """
        super(StringField, self).validate(value)

        if value is not None and not isinstance(value, string_types):
            raise FieldValidationError('should be string, got "{}"'.format(value))


class NumberField(BaseField):
    """A field that validates number values"""

    def decode(self, value):
        """
        Decodes the given value into a number

        :param value: the value
        :return: float or int
        """
        if value is None:
            return value

        if self.default is not None and isinstance(self.default, int):
            return int(value)

        return float(value)

    def validate(self, value):
        """
        Validates that the given value is a number

        :param value: the value to validate
        """
        super(NumberField, self).validate(value)

        if value is not None and not isinstance(value, (int, float)):
            raise FieldValidationError('should be number, got "{}"'.format(value))


class TypeField(BaseField):
    """A field that validates for the provided type"""

    def __init__(self, atype=None, *args, **kwargs):
        super(TypeField, self).__init__(*args, **kwargs)

        self.type = atype

    def validate(self, value):
        """
        Validates that the given value is of the given type

        :param value: the value to validate
        """
        super(TypeField, self).validate(value)

        if value is not None and not isinstance(value, self.type):
            raise FieldValidationError('should be of type="{}", got "{}"'.format(self.type, value))


class CompoundField(BaseField):
    def __init__(self, subtype=None, *args, **kwargs):
        super(CompoundField, self).__init__(*args, **kwargs)
        self.subtype = subtype


class DictField(CompoundField):
    """A field that validates dict values"""

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = {}

        super(DictField, self).__init__(*args, **kwargs)

    def validate(self, value):
        """
        Validates that the given value is a dict

        :param value: the value to validate
        """
        super(DictField, self).validate(value)

        if value is not None and not isinstance(value, dict):
            raise FieldValidationError('should be dict, got "{}"'.format(value))

        self._validate_values_type(value)

    def _validate_values_type(self, value):
        """
        Validates that the inner values have the correct type

        :param value: the iterable value to validate
        """
        if not value or self.subtype is None:
            return

        for val in list(value.values()):
            if val is not None and not isinstance(val, self.subtype):
                raise FieldValidationError(
                    'should have all {} values, got "{}"'.format(
                        self.subtype,
                        val
                    )
                )


class ListField(CompoundField):
    """A field that validates list values"""

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = []

        super(ListField, self).__init__(*args, **kwargs)

    def validate(self, value):
        """
        Validates that the given value is a list

        :param value: the value to validate
        """
        super(ListField, self).validate(value)

        if value is not None and not isinstance(value, list):
            raise FieldValidationError('should be list')

        self._validate_values_type(value)

    def _validate_values_type(self, value):
        """
        Validates that the inner values have the correct type

        :param value: the iterable value to validate
        """
        if not value or self.subtype is None:
            return

        for val in value:
            if val is not None and not isinstance(val, self.subtype):
                raise FieldValidationError(
                    'should have all {} values, got "{}"'.format(
                        self.subtype,
                        val
                    )
                )


class ForeignKey(StringField):
    """A field that represents an object id for a particular model type"""

    def __init__(self, refers, key_regex=None, *args, **kwargs):
        super(ForeignKey, self).__init__(*args, **kwargs)

        self.refers = refers
        self.key_regex = key_regex


class ForeignKeyList(ListField):
    """A field that represents a list of object ids for a particular model type"""

    def __init__(self, refers, *args, **kwargs):
        kwargs['subtype'] = string_types

        super(ForeignKeyList, self).__init__(*args, **kwargs)

        self.refers = refers
