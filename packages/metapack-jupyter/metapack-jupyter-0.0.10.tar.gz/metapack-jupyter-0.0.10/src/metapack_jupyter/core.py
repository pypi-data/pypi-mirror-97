# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
Common support for jupyter notebooks.
"""
import nbformat
from contextlib import contextmanager
from os.path import join, dirname
from os import makedirs
import logging
from pathlib import Path
import unicodecsv as csv

logger = logging.getLogger('user')
err_logger = logging.getLogger('cli-errors')
debug_logger = logging.getLogger('debug')
doc_logger = logging.getLogger('doc')

log_init = False

def init_logging(log_level=logging.INFO):
    import sys

    global log_init

    if log_init:
        return

    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(message)s'))
    out_hdlr.setLevel(log_level)
    logger.addHandler(out_hdlr)
    logger.setLevel(log_level)

    out_hdlr = logging.StreamHandler(sys.stderr)
    out_hdlr.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    out_hdlr.setLevel(logging.WARN)
    err_logger.addHandler(out_hdlr)
    err_logger.setLevel(logging.WARN)

    out_hdlr = logging.StreamHandler(sys.stderr)
    out_hdlr.setFormatter(logging.Formatter('DBG %(levelname)s: %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    debug_logger.addHandler(out_hdlr)
    debug_logger.setLevel(logging.CRITICAL)

    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(message)s'))
    out_hdlr.setLevel(log_level)
    doc_logger.addHandler(out_hdlr)
    doc_logger.setLevel(log_level)

    log_init = True


def ensure_source_package_dir(nb_path, pkg_name):
    """Ensure all of the important directories in a source package exist"""

    pkg_path = join(dirname(nb_path), pkg_name)

    makedirs(join(pkg_path,'notebooks'),exist_ok=True)
    makedirs(join(pkg_path, 'docs'), exist_ok=True)

    return pkg_path


def get_metatab_doc(nb_path):
    """Read a notebook and extract the metatab document. Only returns the first document"""

    from metatab.generate import CsvDataRowGenerator
    from metatab.rowgenerators import TextRowGenerator
    from metatab import MetatabDoc

    with open(nb_path) as f:
        nb = nbformat.reads(f.read(), as_version=4)

    for cell in nb.cells:
        source = ''.join(cell['source']).strip()
        if source.startswith('%%metatab'):
            return MetatabDoc(TextRowGenerator(source))


def get_package_dir(nb_path):
    """Return the package directory for a Notebook that has an embeded Metatab doc, *not* for
    notebooks that are part of a package """
    doc = get_metatab_doc(nb_path)
    doc.update_name(force=True, create_term=True)
    pkg_name = doc['Root'].get_value('Root.Name')
    assert pkg_name

    return ensure_source_package_dir(nb_path, pkg_name), pkg_name


def process_schema(doc, resource, df):
    """Add schema entiries to a metatab doc from a dataframe"""
    from rowgenerators import SourceError
    from requests.exceptions import ConnectionError

    from metapack.cli.core import extract_path_name, type_map
    from metapack_build.core import alt_col_name
    from tableintuit import TypeIntuiter
    from rowgenerators.generator.python import PandasDataframeSource
    from appurl import parse_app_url

    try:
        doc['Schema']
    except KeyError:
        doc.new_section('Schema', ['DataType', 'Altname', 'Description'])

    schema_name = resource.get_value('schema', resource.get_value('name'))

    schema_term = doc.find_first(term='Table', value=schema_name, section='Schema')

    if schema_term:
        logger.info("Found table for '{}'; skipping".format(schema_name))
        return

    path, name = extract_path_name(resource.url)

    logger.info("Processing {}".format(resource.url))

    si = PandasDataframeSource(parse_app_url(resource.url), df, cache=doc._cache, )

    try:
        ti = TypeIntuiter().run(si)
    except SourceError as e:
        logger.warn("Failed to process '{}'; {}".format(path, e))
        return
    except ConnectionError as e:
        logger.warn("Failed to download '{}'; {}".format(path, e))
        return

    table = doc['Schema'].new_term('Table', schema_name)

    logger.info("Adding table '{}' to metatab schema".format(schema_name))

    for i, c in enumerate(ti.to_rows()):
        raw_alt_name = alt_col_name(c['header'], i)
        alt_name = raw_alt_name if raw_alt_name != c['header'] else ''

        t = table.new_child('Column', c['header'],
                            datatype=type_map.get(c['resolved_type'], c['resolved_type']),
                            altname=alt_name,
                            description=df[c['header']].description \
                                        if hasattr(df, 'description') and df[c['header']].description else ''
                            )

    return table


def write_geojson(path_or_flo, columns, gen):
    import fiona
    from fiona.crs import from_epsg
    from collections import OrderedDict

    type_map = {
        'number': 'float'
    }

    schema = {
        'geometry': 'Unknown',
        'properties': OrderedDict(
            [(c['header'], type_map.get(c['datatype'], c['datatype'])) for c in columns]
        )
    }

    try:
        f = fiona.open(path_or_flo,
                       driver='GeoJSON',
                       crs=from_epsg(4326),
                       schema=schema)
    except TypeError:
        f = path_or_flo  # Assume that it's already a file-like-object

    try:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(gen)

        try:
            return f.getvalue()
        except AttributeError:
            return None

    finally:
        f.close()


@contextmanager
def edit_notebook(nb_path: Path):
    import nbformat

    with nb_path.open() as f:
        nb = nbformat.read(f, as_version=4)

    yield nb

    with nb_path.open('wt') as f:
        nbformat.write(nb, f)


def get_cell_source(nb, tag):
    for cell in nb['cells']:
        if tag in cell.get('metadata', {}).get('tags', []):
            return cell.source

    return ''


def set_cell_source(nb, tag, source):
    for cell in nb['cells']:
        if tag in cell.get('metadata', {}).get('tags', []):
            cell.source = source