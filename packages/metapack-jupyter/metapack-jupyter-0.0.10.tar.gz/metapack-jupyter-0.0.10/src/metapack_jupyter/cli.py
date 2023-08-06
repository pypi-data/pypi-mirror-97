# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""
CLI program for managing packages
"""

import sys
from os.path import basename, dirname, exists, splitext
from pathlib import Path

import requests
from metapack import Downloader, MetapackDoc
from metapack.cli.core import (
    MetapackCliMemo,
    err,
    list_rr,
    prt,
    warn,
    write_doc
)
from metapack.util import ensure_dir

from metapack_jupyter.core import edit_notebook, set_cell_source

from .hugo import convert_hugo
from .wordpress import convert_wordpress

downloader = Downloader.get_instance()


def notebook(subparsers):
    parser = subparsers.add_parser(
        'notebook',
        help='Create and convet Jupyter notebooks ',
        epilog='Cache dir: {}\n'.format(str(downloader.cache.getsyspath('/'))))

    parser.set_defaults(handler=None)

    #
    # New Notebooks

    cmdsp = parser.add_subparsers(help='sub-command help')

    cmdp = cmdsp.add_parser('new', help='Create new notebooks')
    cmdp.set_defaults(run_command=new_cmd)

    cmdp.add_argument('-m', '--metatab', action='store_true', default=False,
                      help='Create a metatab notebook from a metatab file')

    cmdp.add_argument('-E', '--eda', action='store_true', default=False,
                      help='Create an EDA notebook for a resource')

    cmdp.add_argument('-n', '--new-notebook', help='Create a new, blank notebook')

    cmdp.add_argument('metatabfile', nargs='?',
                      help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv' ")

    #
    # Convert group

    cmdp = cmdsp.add_parser('convert', help='Convert to other formats')
    cmdp.set_defaults(run_command=convert_cmd)

    cmdp.add_argument('-H', '--hugo', default=False, nargs='?',
                      help='Write images and Markdown into a Hugo static site directory. or use '
                           'METAPACK_HUGO_DIR env var')

    cmdp.add_argument('-w', '--wordpress',
                      help="Write images and html into a directory, for publication to Wordpress. "
                           "( For testing; you probably want 'mp wp' to publish to Wordpress ")

    cmdp.add_argument('notebook',
                      help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv' ")


def new_cmd(args):
    downloader = Downloader.get_instance()

    m = MetapackCliMemo(args, downloader)

    if m.args.eda:
        write_eda_notebook(m)

    elif m.args.new_notebook:
        write_notebook(m)

    elif m.args.metatab:
        write_metatab_notebook(m)


def convert_cmd(args):
    if args.wordpress:
        convert_wordpress(args.notebook, args.wordpress)

    if args.hugo:
        convert_hugo(args.notebook, args.hugo)


def write_notebook(m):
    # Get the EDA notebook file from Github

    url = "https://raw.githubusercontent.com/Metatab/notebook-templates/master/package-notebook.ipynb"

    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()

    p = Path(m.args.new_notebook)

    nb_path = f'notebooks/{p.stem}.ipynb'

    ensure_dir(dirname(nb_path))

    if exists(nb_path):
        err("Notebook {} already exists".format(nb_path))

    with open(nb_path, 'wb') as f:
        f.write(r.content)

    prt('Wrote {}'.format(nb_path))


def write_eda_notebook(m):
    # Get the EDA notebook file from Github

    url = "https://raw.githubusercontent.com/Metatab/exploratory-data-analysis/master/eda.ipynb"

    resource = m.get_resource()

    if not resource:
        warn('Must specify a resource. Select one of:')
        list_rr(m.doc)
        sys.exit(0)

    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()

    nb_path = Path('notebooks/{}-{}.ipynb'.format(splitext(basename(url))[0], resource.name))

    ensure_dir(nb_path.parent)

    if nb_path.exists():
        err("Notebook {} already exists".format(nb_path))

    with nb_path.open('wb') as f:
        f.write(r.content)

    prt('Wrote {}'.format(nb_path))

    with edit_notebook(nb_path) as nb:
        set_cell_source(nb, 'resource_name', "resource_name='{}'".format(resource.name))


def write_metatab_notebook(m):
    from metapack_jupyter.convert import write_metatab_notebook as _write_metatab_notebook

    print(m.doc.description)

    _write_metatab_notebook(m.doc)


def get_readme(m):
    for t in m.doc.find('Root.Documentation', title='README'):
        print(t.resolved_url)

        m.doc.remove_term(t)

        with t.resolved_url.fspath.open() as f:
            return f.read()


def convert_metatab_notebook(m):
    m.doc['Documentation'].get_or_new_term('Root.Readme').value = get_readme(m)

    return

    source = None  # Path(source)

    if source.suffix == '.csv':
        dest = source.with_suffix('.ipynb')
        doc = MetapackDoc(source)
        doc.ensure_identifier()
        doc.update_name(create_term=True)
        # _write_metatab_notebook(doc, dest)

    elif source.suffix == '.ipynb':
        dest = source.with_suffix('.csv')

        doc = None  # extract_notebook_metatab(source)
        doc.ensure_identifier()
        doc.update_name(create_term=True)
        write_doc(doc, dest)

    else:
        err("Source file must be either .ipynb or .csv")
