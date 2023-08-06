# convert-html-to-dash

A conversion tool to turn html/bootstrap into Python code for use with Dash and Plotly

I find the interactive mode most useful, but exiting the program from interactive mode is unreliable.

This conversion only does so much. There are plenty of things that aren't converted fully such as dropdowns. This just creates a base framework. There is no intention of pushing the conversion process further at this time.

[convert-html-to-dash on pypi](https://pypi.org/project/convert-html-to-dash/0.1/)

```pip install convert-html-to-dash```

```
$ python -m convert-html-to-dash -h
usage: __main__.py [-h] [-f FIL] [-o OUTFILE] [-i] [-p PRIORITY_LIST]

Convert HTML into Python Code for Dash with bootstrap

optional arguments:
  -h, --help        show this help message and exit
  -f FIL            input file
  -o OUTFILE        output file
  -i                Interactive mode. (ctrl-c, ctrl-v, then add a terminating character. windows: ctrl-z, linux: ctrl-d.
  -p PRIORITY_LIST  priority list for replacing tags. :: Options: dcc = dash_core_components, dbc = dash_bootstrap_components, html = dash_html_components :: Exanple: -p dbc -p html -p dcc :: Default Order: dcc, dbc, html

```

`python -m convert-html-to-dash -f infile.html -o outfile.py`
```
  dbc.Container(
      className="container",
      children=[
          html.H1(children=["Some Test Information"]),
          dbc.Row(
              className="row",
              children=[
                dbc.Col(className="col", children=[]),
                ...
```

`python -m convert-html-to-dash -f infile.html -o outfile.py -p html`
```
html.Div(
    className="container",
    children=[
        html.H1(children=["Some Test Information"]),
        html.Div(
            className="row",
            children=[
                html.Div(className="col", children=[]),
                ...
```



