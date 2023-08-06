# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
CLI program for storing packages to Data.World
"""

# flake8: noqa

import json
import mimetypes
import sys
from os import getcwd
from os.path import basename, join

from metapack import open_package
from metapack.cli.core import err, prt, warn
from metatab import (DEFAULT_METATAB_FILE, MetatabDoc, MetatabError,
                     resolve_package_metadata_url)
from metatab.util import slugify
from rowgenerators import Url, get_cache

try:
    import datadotworld as dw
    from datadotworld.client.api import RestApiError
except ImportError:
    err(
        "To run the Metataworld importer, you must first install the datadotworld package. See https://github.com/datadotworld/data.world-py")


def metaworld():
    import argparse
    parser = argparse.ArgumentParser(
        prog='metakan',
        description='Publish packages to Data.World')

    parser.add_argument('-i', '--info', default=False, action='store_true',
                        help="Show package information")

    parser.add_argument('metatabfile', nargs='?', default=DEFAULT_METATAB_FILE, help='Path to a Metatab file')

    class MetapackCliMemo(object):
        def __init__(self, args):
            self.cwd = getcwd()
            self.args = args
            self.cache = get_cache('metapack')

            self.mtfile_arg = args.metatabfile if args.metatabfile else join(self.cwd, DEFAULT_METATAB_FILE)

            self.mtfile_url = Url(self.mtfile_arg)
            self.resource = self.mtfile_url.parts.fragment

            self.package_url, self.mt_file = resolve_package_metadata_url(self.mtfile_url.rebuild_url(False, False))

    m = MetapackCliMemo(parser.parse_args(sys.argv[1:]))

    try:
        doc = MetatabDoc(m.mt_file, cache=m.cache)
    except (IOError, MetatabError) as e:
        err("Failed to open metatab '{}': {}".format(m.mt_file, e))

    if m.args.info:
        package_info(doc)
    else:
        send_to_dw(doc)

    exit(0)


def package_info(doc):
    client = dw.api_client()

    username = 'ericbusboom'

    title = doc.find_first_value("Root.Title")
    key = join(username, slugify(title))

    try:
        ds = client.get_dataset(key)
        prt(json.dumps(ds, indent=4))
    except RestApiError as e:
        err(e)


def get_resource_urls(doc):
    resources = {}

    for dist in doc.find("Root.Distribution"):

        try:
            package_url, metadata_url = resolve_package_metadata_url(dist.value)
        except Exception as e:
            warn("Failed for Distribution {}; {}".format(dist.value, e))
            continue

        u = Url(package_url)

        if u.resource_format == 'zip':
            prt("Skipping ZIP package ", package_url)

        elif u.resource_format == 'xlsx':
            if False:
                resources[basename(package_url)] = package_url
                prt("Adding XLS package ", package_url)
                pass

        elif u.resource_format == 'csv':

            resources[basename(package_url)] = u.signed_resource_url

            prt("Adding CSV package {}".format(basename(package_url)))

            try:
                p = open_package(package_url)
            except (IOError, MetatabError) as e:
                err("Failed to open package '{}' from reference '{}': {}".format(package_url, dist.value, e))

            for r in p.resources():

                mimetype = mimetypes.guess_type(r.resolved_url)[0]

                try:
                    ext = mimetypes.guess_extension(mimetype)[1:]
                except:
                    ext = None

                # '.csv': Data>world currently get the format from the name, not the URL
                resources[r.name + '.csv'] = r.resolved_url
                prt("Adding CSV resource {}".format(r.name))
        else:
            prt('Skipping {}'.format(package_url))

    return resources


def truncate(v, l, suffix=''):
    return v[:(l - len(suffix))] if len(v) > l else v


def send_to_dw(doc):
    client = dw.api_client()

    username = 'ericbusboom'

    title = doc.find_first_value("Root.Title")
    key = username + '/' + slugify(truncate(title, 30))

    d = dict(
        title=truncate(title, 30),
        description=doc.find_first_value("Root.Description"),
        summary=doc.markdown,
        visibility='OPEN',
        files=get_resource_urls(doc)
    )

    try:

        ds = client.get_dataset(key)  # Raise an error if the dataset does not exist

        ds = client.replace_dataset(key, **d)

        ds = client.get_dataset(key)

    except RestApiError:

        ds = client.create_dataset(username, **d)

        ds = client.get_dataset(key)
