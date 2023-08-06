# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Command-line tools for demo module."""
import json
import random
from datetime import date, timedelta
from os.path import dirname, join

import click
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user

from .services import Marc21RecordService, Metadata
from .vocabularies import Vocabularies


def system_identity():
    """System identity."""
    identity = Identity(1)
    identity.provides.add(any_user)
    return identity


def fake_access_right():
    """Generates a fake access_right."""
    vocabulary = Vocabularies.get_vocabulary("access_right")
    _type = random.choice(list(vocabulary.data.keys()))
    return _type


def fake_feature_date(days=365):
    """Generates a fake feature_date."""
    start_date = date.today()
    random_number_of_days = random.randrange(days)
    _date = start_date + timedelta(days=random_number_of_days)
    return _date.strftime("%Y-%m-%d")


def _load_file(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        input = fp.read()
        return input.decode("utf-8")


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


def create_fake_metadata(filename):
    """Create records for demo purposes."""
    metadata = Metadata()
    metadata.xml = _load_file(filename)
    data_acces = {
        "access_right": fake_access_right(),
        "embargo_date": fake_feature_date(),
    }

    service = Marc21RecordService()

    draft = service.create(
        metadata=metadata,
        identity=system_identity(),
        access=data_acces,
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


def create_fake_record(filename):
    """Create records for demo purposes."""
    data_to_use = _load_json(filename)
    data_acces = {
        "access_right": fake_access_right(),
        "embargo_date": fake_feature_date(),
    }

    service = Marc21RecordService()

    draft = service.create(
        data=data_to_use, identity=system_identity(), access=data_acces
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


@click.group()
def marc21():
    """InvenioMarc21 records commands."""
    pass


@marc21.command("demo")
@click.option(
    "--number",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@click.option(
    "--file",
    "-f",
    default="data/fake-metadata.xml",
    show_default=True,
    type=str,
    help="Relative path to file",
)
@click.option(
    "--metadata-only",
    "-m",
    default="True",
    type=bool,
    help="Provided metadata only in file",
)
@with_appcontext
def demo(number, file, metadata_only):
    """Create number of fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")

    for _ in range(number):
        if metadata_only:
            create_fake_metadata(file)
        else:
            create_fake_record(file)

    click.secho("Created records!", fg="green")
