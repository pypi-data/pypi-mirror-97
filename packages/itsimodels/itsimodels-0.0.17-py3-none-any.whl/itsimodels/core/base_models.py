import collections
import copy

from itsimodels import __version__
from itsimodels.core.compat import string_types
from itsimodels.core.field_decode import FieldDecoder
from itsimodels.core.fields import (
    BaseField,
    DictField,
    FieldValidationError,
    ListField,
    StringField,
    TypeField
)
from itsimodels.core.migrators import Migrator
from itsimodels.core.setup_logging import logger


KEY_FIELD_NAME = 'key'


class ValidationError(Exception):
    """Raised when a data or validation error occurs on the model"""


class BaseModel(object):
    """Represents an ITSI knowledge object"""

    # Helper object to handle data migrations between different model versions
    migrator = Migrator()

    # The model version
    version = StringField(default=__version__, required=True)

    @classmethod
    def model_fields(cls):
        """
        Returns a mapping dict of field name to field types

        :return: a dict from str to an instance of BaseField
        :rtype: dict
        """
        fields = {}

        class_items = list(BaseModel.__dict__.items()) + list(cls.__dict__.items())
        for name, value in class_items:
            if not isinstance(value, BaseField):
                continue

            fields[name] = value

        return fields

    def __init__(self, data=None, auto_validate=True, auto_migrate=True, field_decoder=None):
        """
        :param dict data: The model data
        :param bool auto_validate: Whether to automatically call validate on the model
        :param bool auto_migrate: Whether to automatically migrate the model's data to the latest model version
        :param object field_decoder: Optional object to help parse a field value
        """
        if data is None:
            data = {}

        if data.get('version', None) is None:
            data['version'] = self.version.default

        if self.get_key() is not None:
            if KEY_FIELD_NAME in data:
                logger.info('Processing {} with {}={}...'.format(self.__class__.__name__,
                    KEY_FIELD_NAME,
                    data.get(KEY_FIELD_NAME)))
            elif self.get_key().alias is not None and self.get_key().alias in data:
                logger.info('Processing {} with {}={}...'.format(self.__class__.__name__,
                    self.get_key().alias,
                    data.get(self.get_key().alias)))

        if auto_migrate:
            data = self.migrator.migrate(data)

        self._fields = self._populate(data, field_decoder=field_decoder)

        if auto_validate:
            self.validate()

    def get_key(self):
        return getattr(self, KEY_FIELD_NAME, None)

    def validate(self):
        """
        Validates the current model based on its schema of fields.
        """
        for name, field in self._fields.items():
            value = getattr(self, name)
            try:
                field.validate(value)
            except FieldValidationError as exc:
                raise ValidationError('"{}" {} for {}'.format(name, exc, self))

    @property
    def fields(self):
        return self._fields

    def to_dict(self, use_alias=False):
        """
        Returns a dict object that represents the given model.

        :param use_alias: whether to use the alias name instead
        :type use_alias: bool

        :return: a dict containing the model's data
        :rtype: dict
        """
        obj = {}

        for name, field in self.fields.items():
            field_value = getattr(self, name)

            if (field_value and isinstance(field, TypeField) and
                    field.type and issubclass(field.type, BaseModel)):
                copied_value = field_value.to_dict(use_alias=use_alias)

            elif (field_value and isinstance(field, ListField) and
                  field.subtype and issubclass(field.subtype, BaseModel)):
                values = []

                for index, value in enumerate(field_value):
                    values.append(value.to_dict(use_alias=use_alias))

                copied_value = values

            elif (field_value and isinstance(field, DictField) and
                  field.subtype and issubclass(field.subtype, BaseModel)):
                values = {}

                for key, value in field_value.items():
                    values[key] = value.to_dict(use_alias=use_alias)

                copied_value = values
            else:
                copied_value = copy.deepcopy(field_value)

            field_name = field.alias if use_alias and field.alias else name

            obj[field_name] = copied_value

        return obj


    def _populate(self, data, field_decoder=None):
        """
        Populates the model with values from data for each field

        :param dict data: a dict from field name to data value
        :param object field_decoder: Optional object to help parse a field value
        """
        try:
            fields = self.model_fields()

            #missing_fields = set(list({k: v for k, v in sorted(data.items())}.keys())) - set(
            #    list({k: v for k, v in sorted(fields.items())}.keys()))

            #class_key = self.__class__.__name__
            #print('\n ===== for class:{} the following are missing\n{}'.format(class_key, missing_fields))

            #if class_key in GLOBAL_MISSING_IMPORT_FIELD_MAP:
            #    GLOBAL_MISSING_IMPORT_FIELD_MAP[class_key].update(missing_fields)
            #else:
            #    GLOBAL_MISSING_IMPORT_FIELD_MAP[class_key] = missing_fields

            #print('===========GLOBAL_MISSING_IMPORT_FIELD_MAP==={}'.format(GLOBAL_MISSING_IMPORT_FIELD_MAP))

            return self._populate_with_fields(data, fields, field_decoder=field_decoder)
        except Exception:
            logger.exception('Failed to populate data for class {}. data.items={}'.format(self.__class__.__name__,
                data.items()))


    def _populate_with_fields(self, data, fields, field_decoder=None):
        """
        Populates the model with values from data for each field in the given set of fields

        :param dict data: a dict from field name to data value
        :param object field_decoder: Optional object to help parse a field value
        """
        try:
            if field_decoder is None:
                field_decoder = FieldDecoder()

            for field_name, field in fields.items():
                default = field.default

                value = field_decoder.decode(field_name, field, data)

                if value is None and default is not None:
                    if isinstance(default, collections.Callable):
                        value = default()
                    else:
                        value = copy.deepcopy(default)

                setattr(self, field_name, value)

            return fields
        except Exception:
            logger.exception('Failed to populate with fields for object type {}'.format(self.__class__.__name__))


class ChildModel(BaseModel):
    """Represents an ITSI knowledge object that's nested in another model"""

    def __init__(self, *args, **kwargs):
        super(ChildModel, self).__init__(*args, **kwargs)

        if hasattr(self, 'version'):
            delattr(self, 'version')
            self._fields.pop('version', None)


class DynamicModel(BaseModel):
    """Represents an object with a dynamic field set"""

    def to_dict(self, *args, **kwargs):
        """
        Returns a dict obj that represents the current model

        :return: a dict
        :rtype: dict
        """
        data = {}

        for field in dir(self):
            if field.startswith('__') or field.startswith('_') or field in ['fields']:
                continue

            value = getattr(self, field)
            if isinstance(value, (string_types, int, float, dict, list)):
                data[field] = value

        return data

    def _populate(self, data, field_decoder=None):
        """
        Populates the model with values from data for each field

        :param dict data: a dict from field name to data value
        :param object field_decoder: Optional object to help parse a field value
        """
        fields = {}

        key = self.get_key()
        if key is not None:
            fields[KEY_FIELD_NAME] = key

        for field_name, value in data.items():
            if isinstance(value, list):
                field = ListField()
            elif isinstance(value, dict):
                field = DictField()
            else:
                field = StringField()

            fields[field_name] = field

        fields.update(self.model_fields())

        return self._populate_with_fields(data, fields, field_decoder=field_decoder)


class ConfModel(DynamicModel):
    """Represents a conf object"""


class ImageModel(BaseModel):
    """Represents an image object"""
