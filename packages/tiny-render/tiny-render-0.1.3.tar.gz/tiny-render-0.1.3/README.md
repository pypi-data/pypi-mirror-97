# Tiny Render

This is a very simple wrapper for `Jinja2` by providing few built-in variables.

Variables,

- `{{ _gitsha }}` - will be the shortsha for `git` hash, the value will be `None` if `git` is not
installed or the current directory is not a git repo.
- `{{ 'HOME' | getenv }}` - the environment variable `HOME` will be renderred. It will raise exception
if `HOME` is not set
- `{{ _date_str }}` - the current date in `yyyymmdd` format
- `{{ _time_str }}` - the current date/time in `yyyymmddHHMMSS` format


## Installation

```bash
pip install tiny-render
```

Sample Code

```python
from tiny_render import Render

with open(os.path.join("/tmp","test.txt"), 'w') as f:
    f.write("gitsha: {{_gitsha}}, hello {{key}}")

params = {"key": "world"}

r = Render("/tmp")

r.go("test.txt", **params)

# the output is "gitsha: xxxxxxx, hello world"
```