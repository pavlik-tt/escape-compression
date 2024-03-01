*Please do not use this script, although it works, it is still ineffective most of the time.*
# escape-compression
Simple file compression

## Usage
**Compressing:**
```python
esc_comp.compress(very_long_string)
```
Example:
```python
>>> import esc_comp
>>> very_long_string = "+" * 1000000
>>> not_very_long_string = esc_comp.compress(very_long_string)
>>> not_very_long_string
'ESCCMP\x01\x1b[42;0;1000000]\x02\x1d'
```
**Decompressing:**
```python
esc_comp.decompress(not_very_long_string)
```
Example:
```python
>>> import esc_comp
>>> not_very_long_string = 'ESCCMP\x01\x1b[42;0;1000000]\x02\x1d'
>>> very_long_string = esc_comp.decompress(not_very_long_string)
```