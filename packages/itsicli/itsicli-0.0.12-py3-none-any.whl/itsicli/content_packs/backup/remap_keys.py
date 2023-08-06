# ${copyright}

import importlib
import logging
import re

from itsimodels.core.fields import (
    DictField,
    ForeignKey,
    ForeignKeyList,
    ListField,
    TypeField
)
from itsimodels.core.base_models import BaseModel


class KeysUpdater(object):

    def __init__(self, remapped_keys):
        self.remapped_keys = remapped_keys

    def update(self, model):
        for field_name, field in model.fields.items():
            field_value = getattr(model, field_name, None)
            if field_value is None:
                continue

            if isinstance(field, ForeignKey):
                self.update_foreign_key(model, field_name, field)

            elif isinstance(field, ForeignKeyList):
                self.update_foreign_key_list(model, field_name, field)

            elif isinstance(field, ListField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_list_of_models(field_value)

            elif isinstance(field, DictField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_dict_of_models(field_value)

            elif isinstance(field, TypeField) and field.type and issubclass(field.type, BaseModel):
                self.update(field_value)

        return model

    def update_foreign_key(self, model, field_name, field):
        old_key = getattr(model, field_name)

        if field.key_regex:
            match = re.match(field.key_regex, old_key)
            if not match:
                return

            parsed_old_key = match.groups()[0]

            remapped_key = self.get_remapped_key(field.refers, parsed_old_key)

            new_key = old_key.replace(parsed_old_key, remapped_key)
        else:
            new_key = self.get_remapped_key(field.refers, old_key)

        setattr(model, field_name, new_key)

    def update_foreign_key_list(self, model, field_name, field):
        foreign_key_list = getattr(model, field_name)

        new_keys = []

        for old_key in foreign_key_list:
            new_key = self.get_remapped_key(field.refers, old_key)
            new_keys.append(new_key)

        setattr(model, field_name, new_keys)

    def update_list_of_models(self, child_models):
        for child_model in child_models:
            self.update(child_model)

    def update_dict_of_models(self, dict_models):
        for _, child_model in dict_models.items():
            self.update(child_model)

    def get_remapped_key(self, model_import_name, old_key):
        parts = model_import_name.split('.')
        pkg_name = '.'.join(parts[:-1])
        model_name = parts[-1]

        try:
            pkg = importlib.import_module(pkg_name)
        except ImportError as exc:
            logging.exception(exc)

            return old_key

        model_class = getattr(pkg, model_name)

        new_keys = self.remapped_keys.get(model_class, {})

        new_key = new_keys.get(old_key, old_key)

        return new_key
