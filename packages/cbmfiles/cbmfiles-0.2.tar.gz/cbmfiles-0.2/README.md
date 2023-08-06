# cbmfiles

This Python module enables access to various types of file formats used by Commodore microcomputers.

It provides classes to translate BASIC and binary program files between their native format and standard text files.


## Examples

Classes reside in the `cbmfiles` module, the whole module may be imported or just those definitions referenced by the user.

### List the contents of a BASIC file

```python
from cbm_files import BASICFile

with open('example.prg', 'rb') as f:
    prog = BASICFile(f)

for line in prog.to_text():
    print(line)
```


## TODO

- detailed documentation
- support PET, C16, C128
- support BASIC variants
- more examples
