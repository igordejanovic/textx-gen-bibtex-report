# textx-gen-bibtex-report

Generate report for the given bibtex file.

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
