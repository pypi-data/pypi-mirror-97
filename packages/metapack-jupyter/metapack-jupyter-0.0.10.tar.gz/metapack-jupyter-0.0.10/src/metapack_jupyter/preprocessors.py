# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
NBConvert preprocessors
"""

import re
from textwrap import dedent

from metapack import MetapackDoc
from metatab import TermParser
from metatab.rowgenerators import TextRowGenerator
from nbconvert.preprocessors import ExtractOutputPreprocessor, Preprocessor
from nbformat.notebooknode import from_dict
from rowgenerators import parse_app_url
from traitlets import Dict, List, Unicode


class AttachementOutputExtractor(ExtractOutputPreprocessor):
    """Extract outputs from a notebook


    """

    #  def preprocess(self, nb, resources):
    #     return super().preprocess(nb, resources)

    def preprocess(self, nb, resources):

        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)

        return nb, resources  # return super().preprocess(nb, resources) ??

    def preprocess_cell(self, cell, resources, cell_index):
        """Also extracts attachments"""
        from nbformat.notebooknode import NotebookNode

        attach_names = []

        # Just move the attachment into an output

        for k, attach in cell.get('attachments', {}).items():
            for mime_type in self.extract_output_types:
                if mime_type in attach:

                    if 'outputs' not in cell:
                        cell['outputs'] = []

                    o = NotebookNode({
                        'data': NotebookNode({mime_type: attach[mime_type]}),
                        'metadata': NotebookNode({
                            'filenames': {mime_type: k}  # Will get re-written
                        }),
                        'output_type': 'display_data'
                    })

                    cell['outputs'].append(o)

                    attach_names.append((mime_type, k))

        nb, resources = super().preprocess_cell(cell, resources, cell_index)

        output_names = list(resources.get('outputs', {}).keys())

        if attach_names:
            # We're going to assume that attachments are only on Markdown cells, and Markdown cells
            # can't generate output, so all of the outputs were added.

            # reverse + zip matches the last len(attach_names) elements from output_names

            for output_name, (mimetype, an) in zip(reversed(output_names), reversed(attach_names)):
                # We'll post process to set the final output directory
                cell.source = re.sub(r'\(attachment:{}\)'.format(an),
                                     '(__IMGDIR__/{})'.format(output_name), cell.source)

        return nb, resources


class RemoveDocsFromImages(Preprocessor):
    """Change the file name for images, because they are in the sam dir as the HTML files"""
    doc = None

    def preprocess_cell(self, cell, resources, index):

        for o in cell.get('outputs', {}):

            if 'metadata' not in o:
                continue

            image_file = o.get('metadata', {}).get('filenames', {}).get('image/png')

            if image_file:
                o['metadata']['filenames']['image/png'] = image_file.replace('docs/', '')

        return cell, resources


class ScrubPlainText(Preprocessor):
    """If there is a Latex or HTML representation for data, remove only latex representations
    This is primarily for bibliographies, where the text/plain version of the bib, which is
    just the repr() of an HTML object, is showing up in LaTex
    """
    doc = None

    def preprocess_cell(self, cell, resources, index):

        for o in cell.get('outputs', {}):

            d = o.get('data', {})

            if ('text/latex' in d or 'text/html' in d) and 'text/plain' in d:
                del d['text/plain']

        return cell, resources


class HtmlBib(Preprocessor):
    """ Keep only HTML outputs  for biblographies
    """

    remove_type = 'text/html'

    def preprocess_cell(self, cell, resources, index):

        if 'mt_bibliography' in cell.source or 'mt_data_references' in cell.source:
            outputs = []
            for o in cell.get('outputs', {}):

                d = o.get('data', {})
                remove_keys = [k for k in d.keys() if k != self.remove_type]
                o['data'] = {k: v for k, v in d.items() if k not in remove_keys}

                if o['data']:
                    outputs.append(o)

            cell['outputs'] = outputs

        return cell, resources


class LatexBib(HtmlBib):
    """ Keep only Latex outputs  for biblographies
    """

    remove_type = 'text/latex'


class MoveTitleDescription(Preprocessor):
    """Look for Markdown cells with Title or Description tags, clear them out. The ExtractMetatabTerms
    preprocessor is used to move these values into the Metatab metadata"""

    def preprocess(self, nb, resources):

        r = super().preprocess(nb, resources)

        return r

    def preprocess_cell(self, cell, resources, index):

        if cell['cell_type'] == 'markdown':
            tags = cell['metadata'].get('tags', [])

            if 'Title' in tags:
                m = resources.get('metadata', {})
                m['name'] = cell.source.strip().replace('#', '')
                resources['metadata'] = m
                cell.source = ''

            if 'Description' in tags:
                cell.source = ''

        return cell, resources


class ExtractMetatabTerms(Preprocessor):
    """Look for tagged markdown cells and use the value to set some metatab doc terms"""

    terms = None

    def preprocess_cell(self, cell, resources, index):

        if not self.terms:
            self.terms = []

        if cell['cell_type'] == 'markdown':

            tags = cell['metadata'].get('tags', [])

            if 'Title' in tags:
                self.terms.append(('Root', 'Root.Title', cell.source.strip().replace('#', '')))

            elif 'Description' in tags:
                self.terms.append(('Root', 'Root.Description', cell.source.strip()))

        return cell, resources


class ExtractInlineMetatabDoc(ExtractMetatabTerms):
    """Extract the Inlined Metatab document. Will Apply the metatab cell vaules for
    the Title and Description to the document terms. """

    package_url = Unicode(help='Metapack Package Url').tag(config=True)

    doc = None

    extra_terms = None

    def preprocess_cell(self, cell, resources, index):
        import re
        from metatab.rowgenerators import TextRowGenerator

        if not self.extra_terms:
            self.extra_terms = []

        if cell['source'].startswith('%%metatab'):

            tp = TermParser(TextRowGenerator(re.sub(r'\%\%metatab.*\n', '', cell['source'])),
                            resolver=self.doc.resolver, doc=self.doc)

            self.doc.load_terms(tp)

        elif cell['cell_type'] == 'markdown':

            tags = cell['metadata'].get('tags', [])

            if 'Title' in tags:
                self.extra_terms.append(('Root', 'Root.Title', cell.source.strip().replace('#', '')))

            elif 'Description' in tags:
                self.extra_terms.append(('Root', 'Root.Description', cell.source.strip()))

        else:
            cell, resources = super().preprocess_cell(cell, resources, index)

        return cell, resources

    def preprocess(self, nb, resources):

        r = super().preprocess(nb, resources)

        for section, term, value in self.terms:
            self.doc[section].get_or_new_term(term, value)

        return r

    def run(self, nb):

        assert str(self.package_url)

        self.doc = MetapackDoc(TextRowGenerator("Declare: metatab-latest\n"),
                               package_url=parse_app_url(self.package_url))

        self.preprocess(nb, {})

        for section, term, value in self.extra_terms:
            self.doc[section].get_or_new_term(term, value)

        return self.doc


class ExtractFinalMetatabDoc(Preprocessor):
    """Extract the metatab document produced from the %mt_show_metatab magic"""

    doc = None

    def preprocess_cell(self, cell, resources, index):
        from metatab.rowgenerators import TextRowGenerator

        if cell['metadata'].get('mt_final_metatab'):
            if cell['outputs']:
                o = ''.join(e['text'] for e in cell['outputs'])

                self.doc = MetapackDoc(TextRowGenerator(o))

                # Give all of the sections their standard args, to make the CSV versions of the doc
                # prettier

                for name, s in self.doc.sections.items():
                    try:
                        s.args = self.doc.decl_sections[name.lower()]['args']
                    except KeyError:
                        pass

        return cell, resources


class ExtractMaterializedRefs(Preprocessor):
    """Extract the metatab document produced from the %mt_show_metatab magic"""

    materialized = None

    def preprocess_cell(self, cell, resources, index):

        from json import loads

        if cell['metadata'].get('mt_materialize'):

            if cell['outputs']:
                o = ''.join(e['text'] for e in cell['outputs'])

                self.materilized = loads(o)

        return cell, resources


class ExtractLibDirs(Preprocessor):
    """Extract the metatab document produced from the %mt_show_metatab magic"""

    lib_dirs = []

    def preprocess_cell(self, cell, resources, index):

        from json import loads

        if cell['metadata'].get('mt_show_libdirs'):

            if cell['outputs']:
                o = ''.join(e['text'] for e in cell['outputs'])

                if o:
                    self.lib_dirs = loads(o)

        return cell, resources


class RemoveMetatab(Preprocessor):
    """NBConvert preprocessor to remove the %metatab block"""

    def preprocess(self, nb, resources):

        out_cells = []

        for cell in nb.cells:

            source = cell['source']

            if cell['metadata'].get('epilog'):
                continue

            if source.startswith('%%metatab'):
                # lines = source.splitlines()  # resplit to remove leading blank lines
                raise NotImplementedError('Following line seems not to work, so maybe never get here')
                # args = parse_argstring(MetatabMagic.metatab, lines[0].replace('%%metatab', ''))

                cell.source = "%mt_open_package\n"
                cell.outputs = []

                cell['metadata']['hide_input'] = True
                cell['metadata']['show_input'] = 'hide'
                cell['metadata']['hide_output'] = True

            out_cells.append(cell)

        nb.cells = out_cells

        return nb, resources


class RemoveMagics(Preprocessor):
    """Remove line magic lines, or entire cell magic cells"""

    def preprocess(self, nb, resources):
        import re

        for i, cell in enumerate(nb.cells):

            if re.match(r'^\%\%', cell.source):
                cell.source = ''
            else:
                cell.source = re.sub(r'\%[^\n]+\n?', '', cell.source)

        return nb, resources


class PrepareScript(Preprocessor):
    """Add an import so converted scripts can handle some magics"""

    def preprocess(self, nb, resources):
        nb.cells = [from_dict({
            'cell_type': 'code',
            'outputs': [],
            'metadata': {},
            'execution_count': None,
            'source': dedent("""
            from metatab.jupyter.script import get_ipython
            """)
        })] + nb.cells
        return nb, resources


class ReplaceMagics(Preprocessor):
    """Replace some magics"""


class NoShowInput(Preprocessor):
    """NBConvert preprocessor to add hide_input metatab to cells, except to cells that have either
     an %mt_showinput magic, or a 'show' tag """

    def preprocess(self, nb, resources):
        import re

        out_cells = []

        for cell in nb.cells:

            #  Code cells aren't displayed at all, unless it starts with
            # a '%mt_showinput' magic, which is removed

            if cell['cell_type'] == 'code':

                source = cell['source']

                tags = cell['metadata'].get('tags', [])

                if source.startswith('%mt_showinput') or 'show' in tags:
                    cell['source'] = re.sub(r'\%mt_showinput', '', source)
                else:
                    cell['metadata']['hide_input'] = True
                    cell['metadata']['show_input'] = 'hide'

            out_cells.append(cell)

        nb.cells = out_cells

        return nb, resources


class AddEpilog(Preprocessor):
    """Add final cells that writes the Metatab file, materializes datasets, etc.  """

    pkg_dir = Unicode(help='Metatab package Directory').tag(config=True)

    dataframes = List(help='Names of dataframes to materialize', trait=Unicode())

    def preprocess(self, nb, resources):
        from datetime import datetime

        # Well, now we are adding prolog in the epilog ...
        nb.cells = [
                       from_dict({
                           'cell_type': 'code',
                           'outputs': [],
                           'metadata': {'': True, 'prolog': True},
                           'execution_count': None,
                           'source': ("#{}\n".format(datetime.now())) + "%load_ext metapack_jupyter.magic"
                       })
                   ] + nb.cells

        assert self.pkg_dir

        if len(self.dataframes) > 0:
            nb.cells.append(from_dict({
                'cell_type': 'code',
                'outputs': [],
                'metadata': {'mt_dataframes': True, 'epilog': True},
                'execution_count': None,
                'source': '\n'.join("%mt_materialize {} '{}' ".format(df, self.pkg_dir) for df in self.dataframes)
            }))

        nb.cells.append(from_dict({
            'cell_type': 'code',
            'outputs': [],
            'metadata': {'mt_materialize': True, 'epilog': True},
            'execution_count': None,
            'source': dedent("""
            %mt_materialize_all '{pkg_dir}'
            """.format(pkg_dir=self.pkg_dir))
        }))

        nb.cells.append(from_dict({
            'cell_type': 'code',
            'outputs': [],
            'metadata': {'mt_final_metatab': True, 'epilog': True},
            'execution_count': None,
            'source': dedent("""
            %mt_show_metatab

            """.format(pkg_dir=self.pkg_dir))
        }))

        nb.cells.append(from_dict({
            'cell_type': 'code',
            'outputs': [],
            'metadata': {'mt_show_libdirs': True, 'epilog': True},
            'execution_count': None,
            'source': dedent("""
            %mt_show_libdirs

            """.format(pkg_dir=self.pkg_dir))
        }))

        return nb, resources


class AddProlog(Preprocessor):
    """Add final cells that writes the Metatab file, materializes datasets, etc.  """

    env = Dict(help='Initial local variables. Must be primitive types').tag(config=True)

    def preprocess(self, nb, resources):
        source = '\n'.join('{}={}'.format(k, repr(v)) for k, v in self.env.items()
                           if k and isinstance(v, (int, float, str)))

        nb.cells = [
                       from_dict({
                           'cell_type': 'code',
                           'outputs': [],
                           'metadata': {'': True, 'prolog': True},
                           'execution_count': None,
                           'source': source
                       }),
                       # Mark this notebook as being run in a build, which can change the behaviour of some magics
                       from_dict({
                           'cell_type': 'code',
                           'outputs': [],
                           'metadata': {'': True, 'prolog': True},
                           'execution_count': None,
                           'source': "METAPACK_BUILDING=True"
                       }),

                   ] + nb.cells

        return nb, resources
