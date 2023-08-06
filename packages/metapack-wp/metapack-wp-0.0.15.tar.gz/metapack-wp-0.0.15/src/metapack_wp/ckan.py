# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
CLI program for storing pacakges in CKAN

The program uses the Root.Distributions in the source package to locate packages to link into a CKAN record.

"""

import mimetypes
import traceback
from os import getenv
from os.path import basename
from textwrap import dedent

from metapack import Downloader, MetapackDoc, open_package
from metapack.cli.core import err, prt, warn, write_doc
from metapack_build.build import find_csv_packages
from metapack_build.package.s3 import S3Bucket
from metatab import MetatabError

from metapack.cli.core import MetapackCliMemo as _MetapackCliMemo

downloader = Downloader.get_instance()

class MetapackCliMemo(_MetapackCliMemo):

    def __init__(self, args, downloader):
        super().__init__(args, downloader)

        self.api_key = self.args.api or getenv('METAKAN_API_KEY')

        self.ckan_url = self.args.ckan or getenv('METAKAN_CKAN_URL')

        if not self.ckan_url:
            err("Set the --ckan option or the METAKAN_CKAN_URL env var to set the URL of a ckan instance")

        if not self.api_key:
            err("Set the --api option METAKAN_API_KEY env var  with the API key to a CKAN instance")

    def update_mt_arg(self, metatabfile):
        """Return a new memo with a new metatabfile argument"""
        o = MetapackCliMemo(self.args)
        return o

def metakan(subparsers):


    parser = subparsers.add_parser(
        'ckan',
        help='CKAN management of Metatab packages'
    )

    parser.set_defaults(run_command=run_ckan)

    parser.add_argument('-i', '--info', default=False, action='store_true',
                   help="Show configuration information")

    parser.add_argument('-c', '--ckan', help="URL for CKAN instance")

    parser.add_argument('-a', '--api', help="CKAN API Key")

    parser.add_argument('-g', '--group', nargs='?', action='append', help="Assign an additional group. Can be used "
                                                                          "multiple times, one onece with values "
                                                                          "seperated by commas")

    parser.add_argument('-t', '--tag', nargs='?', action='append', help="Assign an additional tag. Can be used "
                                                                        "multiple timesm or once with values "
                                                                        "seperated by commas")

    parser.add_argument('-p', '--packages', action='store_true',
                        help="The file argument is a text file with a list of package URLs to load")

    parser.add_argument('-C', '--configure', action='store_true',
                        help="Load groups and organizations from a metatab file")

    parser.add_argument('-D', '--dump', action='store_true',
                        help="Dump groups and organizations to a metatab file")

    parser.add_argument('metatabfile', nargs='?',
                        help='Path to a Metatab file, or an s3 link to a bucket with Metatab files. ')


def run_ckan(args):

    m = MetapackCliMemo(args, downloader=downloader)


    if m.mtfile_url.scheme == 's3':
        # Find all of the top level CSV files in a bucket and use them to create CKan entries

        b = S3Bucket(m.mtfile_arg)

        for e in b.list():
            key = e['Key']
            if '/' not in key and key.endswith('.csv'):
                url = b.access_url(key)
                prt("Processing", url)
                send_to_ckan(m.update_mt_arg(url))

    elif m.args.packages:
        # Load a list of packages
        with open(m.mtfile_arg) as f:
            for line in f.readlines():
                url = line.strip()
                prt("Processing", url)
                try:
                    send_to_ckan(m.update_mt_arg(url))
                except Exception as e:
                    warn("Failed to process {}: {}".format(line, e))

    elif m.args.configure:
        configure_ckan(m)

    elif m.args.dump:
        dump_ckan(m)

    else:
        send_to_ckan(m)

    exit(0)

def send_to_ckan(m):

    from ckanapi import RemoteCKAN, NotFound
    try:
        doc = MetapackDoc(m.mt_file, cache=m.cache)

    except (IOError, MetatabError) as e:
        err("Failed to open metatab '{}': {}".format(m.mt_file, e))

    # Check for distributions, if there aren't any, try to find a CSV package,
    # which may be an S3 package with distributions.

    if not doc.find('Root.Distribution'):
        doc = find_csv_packages(m, downloader)
        if doc:
            prt("Orig doc has no distributions, switching to doc from built packages:")
            prt("    ", doc.ref)

    if not doc or not doc.find('Root.Distribution'):
        err("No distributions found. Giving up")


    c = RemoteCKAN(m.ckan_url, apikey=m.api_key)

    ckanid = doc.find_first_value('Root.Ckanid')

    unversioned_name = doc.as_version(None)
    ckan_name = unversioned_name.replace('.','-')

    id_name = ckanid or ckan_name

    try:
        pkg = c.action.package_show(name_or_id=id_name)
        prt("Updating CKAN dataset for '{}'".format(id_name))
        found = True
    except NotFound as e:
        e.__traceback__ = None
        traceback.clear_frames(e.__traceback__)
        found = False

    if not found:
        try:
            pkg = c.action.package_show(name_or_id=ckan_name)
            prt("Updating CKAN dataset for '{}'".format(id_name))
            found = True
        except NotFound as e:
            e.__traceback__ = None
            traceback.clear_frames(e.__traceback__)
            found = False

    if not found:
        try:
            pkg = c.action.package_create(name=ckan_name)
        except Exception as e:
            err("Failed to create package for name '{}': {} ".format(ckan_name, e))

        prt("Adding CKAN dataset for '{}'".format(ckan_name))

    pkg['title'] = doc.find_first_value('Root.Title')

    if not pkg['title']:
        pkg['title'] = doc.find_first_value('Root.Description')

    pkg['version'] =  doc.find_first_value('Root.Version')

    pkg['groups'] = [ {'name': g.value } for g in doc['Root'].find('Root.Group')]

    if m.args.group:

        for g in m.args.group:
            if ',' in g:
                for g_ in g.split(','):
                    pkg['groups'].append({'name': g_})
            else:
                pkg['groups'].append({'name': g })

    pkg['tags'] = [{'name': g.value} for g in doc['Root'].find('Root.Tag')]

    if m.args.tag:
        for g in m.args.tag:
            if ',' in g:
                for g_ in g.split(','):
                    pkg['tags'].append({'name': g_})
            else:
                pkg['tags'].append({'name': g })

    org_name = doc.get_value('Root.Origin', doc.get_value('Root.CkanOrg'))

    if org_name:
        org_name_slug = org_name.replace('.','-')
        try:

            owner_org = c.action.organization_show(id=org_name_slug).get('id')
            pkg['owner_org'] = owner_org
        except NotFound:
            warn("Didn't find org for '{}'; not setting organization ".format(org_name_slug))
            org_name_slug = None
    else:
        org_name_slug = None

    extras = {}

    for t in doc.find('*.*', section='Root'):
        if not t.term_is('Root.Distribution'):
            extras[t.qualified_term] = t.value

    pkg['extras'] = [ {'key':k, 'value':v} for k, v in extras.items() ]

    resources = []

    # Try to set the markdown from a CSV package, since it will have the
    # correct links.
    markdown = ''

    inst_distributions = []
    csv_package = None


    def add_package(format, resources):

        package_url = dist.package_url

        d = dict(
            url=str(package_url.inner),
            name=basename(package_url.path),
            format=format,
            mimetype=mimetypes.guess_type(package_url.path)[0],
            description=load_instructions_description('{} version of package, in Metatab format.'.format(format),
                                                      str(package_url.inner))
        )
        resources.append(d)
        prt("Adding {} package {}".format(d['format'], d['name']))


    def load_resources(dist_url, package_url, metadata_url):

        try:
            p = open_package(metadata_url)
        except (IOError, MetatabError) as e:
            err("Failed to open package '{}' from reference '{}': {}".format(package_url, dist_url, e))

        for r in p.resources():

            mimetype = mimetypes.guess_type(r.resolved_url.path)[0]

            try:
                ext = mimetypes.guess_extension(mimetype)[1:]
            except:
                ext = None

            d = dict(
                name=r.name,
                format=ext,
                url=str(r.resolved_url),
                mimetype=mimetype,
                description=r.markdown
            )

            resources.append(d)
            prt("  Adding resource {}".format(d['name']))

        return p


    prt("Distributions:")
    for dist in doc.find('Root.Distribution'):
        prt("    {}".format(dist.value))


    for dist in doc.find('Root.Distribution'):

        if dist.type == 'zip':
            add_package('ZIP', resources)
            inst_distributions.append(dist)

        elif dist.type == 'xlsx':
            add_package('XLSX', resources)

        elif dist.type == 'csv':
            add_package('CSV', resources)
            inst_distributions.append(dist)

            # Resources are always created from the CSV package.
            csv_package = load_resources(dist.url, dist.package_url, dist.metadata_url)

        elif dist.type == 'fs':
            pass

        else:
            warn("Unknown distribution type '{}' for '{}'  ".format(dist.type, dist.value))

    from rowgenerators.appurl.web import WebUrl
    if isinstance( m.mt_file.inner, WebUrl) and  m.mt_file.inner.target_format == 'csv':

        dist = m.doc['Root'].new_term('Root.Distribution', m.mt_file)
        inst_distributions.append(dist)
        csv_package = load_resources(dist.url, dist.package_url, dist.metadata_url)


    if not csv_package:
        err("Didn't find a CSV package. Giving up")

    markdown = csv_package.markdown + "\n\n"+ package_load_instructions(inst_distributions)

    try:
        pkg['notes'] = markdown or doc.markdown #doc.find_first_value('Root.Description')
    except (OSError, DownloadError) as e:
        warn(e)

    pkg['resources'] = resources

    c.action.package_update(**pkg)

    pkg = c.action.package_show(name_or_id=pkg['id'])

    ##
    ## Add a term with CKAN info.

    doc['Root'].get_or_new_term('CkanId').value = pkg['id']

    if org_name_slug is None and pkg.get('organization'):
        doc['Root'].get_or_new_term('CkanOrg', (pkg.get('organization') or {}).get('name'))

    groups = doc['Root'].find('Group')
    for g in groups:
        doc.remove_term(g)

    for group in pkg.get('groups', []):
        doc['Root'].new_term('Group', group['name'])

    write_doc(doc)


def configure_ckan(m):
    """Load groups and organizations, from a file in Metatab format"""
    from ckanapi import RemoteCKAN

    try:
        doc = MetapackDoc(m.mt_file, cache=m.cache)
    except (IOError, MetatabError) as e:
        err("Failed to open metatab '{}': {}".format(m.mt_file, e))

    c = RemoteCKAN(m.ckan_url, apikey=m.api_key)

    groups = { g['name']:g for g in c.action.group_list(all_fields=True) }

    for g in doc['Groups']:

        if g.value not in groups:
            prt('Creating group: ', g.value)
            c.action.group_create(name=g.value,
                                  title=g.get_value('title'),
                                  description=g.get_value('description'),
                                  id=g.get_value('id'),
                                  image_url=g.get_value('image_url'))

    orgs = {o['name']: o for o in c.action.organization_list(all_fields=True)}

    for o in doc['Organizations']:

        if o.value not in orgs:
            prt('Creating organization: ', o.value)
            c.action.organization_create(name=o.value,
                                  title=o.get_value('title'),
                                  description=o.get_value('description'),
                                  id=o.get_value('id'),
                                  image_url=o.get_value('image_url'))

def load_instructions_description(desc,url):
    """Display loading the package into metapack, displayed in the resource"""

    return dedent(
        """
        {desc}

        Load dataset into a Python program:

            import metapack as mp
            pkg = mp.open_package('{url}')

        """
    ).format(desc=desc, url=url)

def package_load_instructions(inst_distributions):
    """Load instructions, displayed in the package notes"""

    per_package_inst = ''

    for dist in inst_distributions:

        if dist.type == 'zip':
            per_package_inst += dedent(
                """
                # Loading the ZIP Package

                Zip packages are compressed, so large resources may load faster.

                    import metapack as mp
                    pkg = mp.open_package('{url}')

                """.format(url=dist.package_url.inner))

        elif dist.type == 'csv':
            per_package_inst += dedent(
                """
                # Loading the CSV Package

                CSV packages load resources individually, so small resources may load faster.


                    import metapack as mp
                    pkg = mp.open_package('{url}')

                """.format(url=dist.package_url.inner))

    if per_package_inst:

        return '\n---\n'+per_package_inst

    else:
        return ''

def dump_ckan(m):
    """Create a groups and organization file"""

    doc = MetapackDoc(cache=m.cache)
    doc.new_section('Groups',        'Title Description Id Image_url'.split())
    doc.new_section('Organizations', 'Title Description Id Image_url'.split())

    c = RemoteCKAN(m.ckan_url, apikey=m.api_key)

    for g in c.action.group_list(all_fields=True):
        print(g.keys())

    for o in c.action.organization_list(all_fields=True):
        print(g.keys())
