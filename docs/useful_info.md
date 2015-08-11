Using AUTO INCREMENT:
[mysql doc page](https://dev.mysql.com/doc/refman/5.0/en/example-auto-increment.html)

[Managing hierarchical data](http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/)

## Recommended packages for CL applications

Recommended modules for portability:
- os
- os.path
- shutil
- fileinput
- tempfile


- sys modules supports pipes
- fileinput module supports reading from stdin and files
- recommended module for argument parsing: argparse
- recommended modules: clint, docopt

- subprocess module very useful for executing other applications,
  but envoy is recommended alternative (easier, more pythonic)

- Print errors to stderr, not just stdout

- signal handling via the signal package
  (it's bad form to ignore system exit events!)

## Testing

- doctest and unittest are 2 good approaches
- nose builds on unittest
- mock for mock testing (may be useful to provide mock ledger to avoid setting
  for moreup and tearing down database for every test!)
- pylint and pychecker are good lint tools

- See
  [testing tools taxonomy](https://wiki.python.org/moin/PythonTestingToolsTaxonomy)
  for more.

## Useful libraries

Date parsing using [dateutil](https://labix.org/python-dateutil)
