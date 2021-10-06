import os
from functools import partial
from jinja2 import Template
from textx import generator
from textx.generators import gen_file, get_output_filename

__version__ = "0.1.0.dev"

templates = {
    'article': '''
     {{-idx}}|
    {%- if author %}{{author}}{% endif %}
    {%- if title %}, {{title}}{% endif %}
    {%- if journal %}, {{journal}}{% endif %}
    {%- if issn %}, issn:{{issn}}{% endif %}
    {%- if volume %}, vol.{{volume}}{% endif %}
    {%- if number %}, no.{{number}}{% endif %}
    {%- if pages %}, p.{{pages}}{% endif %}
    {%- if doi %}, DOI:{{doi}}{% endif %}
    {%- if note %}, {{note}}{% endif %}
    {%- if year %}, {{year}}{% endif -%}
    .|{{rank}}''',

    'inproceedings': '''
     {{-idx}}|
    {%- if author %}{{author}}{% endif %}
    {%- if title %}, {{title}}{% endif %}
    {%- if booktitle %}, {{booktitle}}{% endif %}
    {%- if publisher %}, {{publisher}}{% endif %}
    {%- if address %}, {{address}}{% endif %}
    {%- if issn %}, issn:{{issn}}{% endif %}
    {%- if volume %}, vol.{{volume}}{% endif %}
    {%- if number %}, no.{{number}}{% endif %}
    {%- if pages %}, p.{{pages}}{% endif %}
    {%- if doi %}, DOI:{{doi}}{% endif %}
    {%- if note %}, {{note}}{% endif %}
    {%- if year %}, {{year}}{% endif -%}
    .|{{rank}}''',

    'proceedings': '{{idx}}|Edt. {{editor}}, {{title}}, {{publisher}}, {{year}}.|{{rank}}',

    'techreport': '''
     {{-idx}}|
    {%- if author %}{{author}}{% endif %}
    {%- if title %}, {{title}}{% endif %}
    {%- if institution %}, {{institution}}{% endif %}
    {%- if address %}, {{address}}{% endif %}
    {%- if note %}, {{note}}{% endif %}
    {%- if year %}, {{year}}{% endif -%}
    .|{{rank}}''',
}


def authors_filter(authors):
    """
    Reformat authors.
    """
    # Reformat authors
    authors = authors.split(' and ')
    authors = [' '.join(reversed(a.split(','))).strip() for a in authors]
    return ', '.join(authors)


def title_filter(title):
    "Strip {} from title."
    return title.replace('{', '').replace('}', '')


class BibEntry:
    def __init__(self, entry):
        self.key = entry.key
        self.type = entry.type
        for e in entry.fields:
            setattr(self, e.name, e.value)

    def __str__(self):
        return 'BibEntry({})'.format(','.join(['{}={}'.format(name, value)
                                               for name, value in vars(self).items()]))

    def __repr__(self):
        return str(self)


@generator('bibtex', 'text')
def bibtex_generate_text(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating text from bibtex descriptions"

    output_file = get_output_filename(model._tx_filename, output_path, 'txt')
    gen_file(model._tx_filename, output_file,
             partial(generator_callback, model, output_file),
             overwrite,
             success_message='Done.'
             .format(os.path.basename(output_file)))


def sort_year(entry):
    return (9999 - int(entry.year)) if hasattr(entry, 'year') else 0


def sort_default(entry, field):
    if field == 'year':
        return sort_year(entry)
    return getattr(entry, field, '').replace('{', '').replace('}', '')


def generator_callback(model, output_file):
    """
    A generator function that produce output_file from model.
    """
    # Create List of BibEntry objects
    entries = []
    for entry in model.entries:
        if entry.__class__.__name__ == 'BibRefEntry':
            e = BibEntry(entry)
            entries.append(e)

    params = dict(model._tx_model_params)

    # Is sort param is given use it
    if 'sort' in params:
        sort_f = params['sort'].split(',')
        entries.sort(key=lambda e: [sort_default(e, f) for f in sort_f])
    else:
        # Sort by year and rank by default
        entries.sort(key=lambda e: (sort_year(e), sort_default(e, 'rank')))

    # filter by year if given
    if 'year' in params:
        if '-' in params['year']:
            yfrom, yto = [int(y) for y in params['year'].split('-')]
        else:
            yfrom = int(params['year'])
            yto = yfrom
        entries = [e for e in entries
                   if hasattr(e, 'year')
                   and int(e.year) >= yfrom and int(e.year) <= yto]

    if 'type' in params:
        entries = [e for e in entries if e.type == params['type']]

    with open(output_file, 'w') as f:
        # Output each entry according to its template
        for idx, entry in enumerate(entries):
            if hasattr(entry, 'author'):
                entry.author = authors_filter(entry.author)
            if hasattr(entry, 'editor'):
                entry.editor = authors_filter(entry.editor)
            entry.title = title_filter(entry.title)

            if entry.type not in templates:
                print('Unknown entry type: {}'.format(entry.type))
            else:
                t_params = {'idx': idx + 1}
                t_params.update(vars(entry))
                template = Template(templates[entry.type])
                f.write(template.render(**t_params))
                f.write('\n')
