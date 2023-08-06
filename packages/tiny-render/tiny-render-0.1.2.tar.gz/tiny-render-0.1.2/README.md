# Tiny Render

This is a very simple wrapper for `Jinja2` by providing few built-in variables.

Variables,

- `{{ _gitsha }}` - will be the shortsha for `git` hash, the value will be `None` if `git` is not
installed or the current directory is not a git repo.
- `{{ 'HOME' | getenv }}` - the environment variable `HOME` will be renderred. It will raise exception
if `HOME` is not set
- `{{ _date_str }}` - the current date in `yyyymmdd` format
- `{{ _time_str }}` - the current date/time in `yyyymmddHHMMSS` format