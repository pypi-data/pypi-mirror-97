# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Models for Invenio Marc21 Records."""

from os.path import dirname, join

from flask import current_app
from flask_babelex import lazy_gettext as _

from .access_right import AccessRightVocabulary


class Vocabularies:
    """Interface to vocabulary data."""

    this_dir = dirname(__file__)
    vocabularies = {
        # NOTE: dotted keys should parallel MetadataSchemaV1 fields
        "access_right": {
            "path": join(this_dir, "access_right.csv"),
            "class": AccessRightVocabulary,
            "object": None,
        },
    }

    @classmethod
    def get_vocabulary(cls, key):
        """Returns the Vocabulary object corresponding to the path.

        :param key: string of dotted subkeys for Vocabulary object.
        """
        vocabulary_dict = cls.vocabularies.get(key)

        if not vocabulary_dict:
            return None

        obj = vocabulary_dict.get("object")

        if not obj:
            custom_vocabulary_dict = current_app.config.get(
                "MARC21_RECORDS_CUSTOM_VOCABULARIES", {}
            ).get(key, {})

            path = custom_vocabulary_dict.get("path") or vocabulary_dict.get("path")

            # Only predefined classes for now
            VocabularyClass = vocabulary_dict["class"]
            obj = VocabularyClass(path)
            vocabulary_dict["object"] = obj

        return obj

    @classmethod
    def clear(cls):
        """Clears loaded vocabularies."""
        for value in cls.vocabularies.values():
            value["object"] = None

    @classmethod
    def dump(cls):
        """Returns a json-compatible dict of options for frontend.

        The current shape is influenced by current frontend, but it's flexible
        enough to withstand the test of time (new frontend would be able to
        change it easily).
        """
        options = {}
        for key in cls.vocabularies:
            result = options
            for i, dotkey in enumerate(key.split(".")):
                if i == (len(key.split(".")) - 1):
                    result[dotkey] = cls.get_vocabulary(key).dump_options()
                else:
                    result.setdefault(dotkey, {})
                    result = result[dotkey]

        return options
