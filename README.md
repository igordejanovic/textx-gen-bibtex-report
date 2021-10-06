# textx-gen-bibtex-report

Generate report for the given bibtex file.

# Install

For use:

``` sh
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install https://github.com/igordejanovic/textx-bibtex/archive/refs/heads/master.zip
pip install https://github.com/igordejanovic/textx-gen-bibtex-report/archive/refs/heads/main.zip
```

For development:

``` sh
git clone git@github.com:igordejanovic/textx-gen-bibtex-report.git
cd textx-gen-bibtex-report
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install https://github.com/igordejanovic/textx-bibtex/archive/refs/heads/master.zip
pip install -e .[dev,test]
```

**Note:** for zsh escape `[]` -> `pip install -e .\[dev,test\]`

# Usage

To generate a report from file `my.bib`:
```
textx generate my.bib --target text
```

To filter by years

```
textx generate my.bib --target text --year 2018
textx generate my.bib --target text --year 2018-2020
```

To filter by type:

```
textx generate my.bib --target text --type article
```

To sort by year and then by type:

```
textx generate my.bib --target text --sort year,type
```

Currently, templates for reference output format are hardcoded (see
`bibtexreport/__init__.py`) but the plan is to make them specified as separate
files. For templates processing [Jinja](https://jinja.palletsprojects.com/) is
used.


# Credits

Initial project layout generated with `textx startproject`.
