ark2pan
=======

Parse XML data from Intel's ARK database and generate Pan templates for use with [Quattor](www.quattor.org).

arkparser
---------

Implements a parser to read the pseudo-spreadsheet XML format generated by ARK which returns a list of dictionaries, each dictionary representing a single CPU.

Example:
```python
from json import dumps
from arkparser import ARKParser
arkparser = ARKParser()
cpus = arkparser.parse('Intel_ARK_AdvancedSearch_2016_05_11.xml')
print dumps(cpus[34], indent=4)
```


ark2pan
-------

Uses `ARKParser` to generate a single Pan template for each CPU.

Example:
```
./ark2pan Intel_ARK_AdvancedSearch_2016_05_11.xml
```


ark2aq
------

Uses `ARKParser` to generate `add_cpu` commands for aquilon, should be used with templates from `ark2pan`.

Example:
```
./ark2aq Intel_ARK_AdvancedSearch_2016_05_11.xml
```
