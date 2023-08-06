# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models for Invenio Marc21 Records."""

# TODO: remove vocabularies after invenio-vocabularies is released (fixme)

from .access_right import AccessRightVocabulary
from .vocabularies import Vocabularies
from .vocabulary import Vocabulary

__all__ = (
    "AccessRightVocabulary",
    "Vocabularies",
    "Vocabulary",
)
