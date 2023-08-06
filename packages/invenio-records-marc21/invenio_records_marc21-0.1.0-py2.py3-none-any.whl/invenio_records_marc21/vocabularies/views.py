# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Invenio vocabularies views."""


def create_subjects_blueprint_from_app(app):
    """Create app blueprint."""
    return app.extensions["invenio-records-marc21"].subjects_resource.as_blueprint(
        "vocabularies-subjects"
    )
