*Please do not use this script, although it works, it is still ineffective most of the time.*

# escape-compression
Simple text compression

### Cons:
- Doesn't support bytes
- Finds only repeating characters. (so `'HelloHelloHello'` won't work, but `'HHHHHHHHHHHHHHH'` will)

### Coming soon:
- Finding repeated words (For example, `"Around the world, around the world\nAround the world, around the world"` will be compressed to `"Around the world, *0* *1* *2*\n*0* *1* *2*, *0* *1* *2*"`)
- Huffman tree (probably?)
- Finding duplicate bytes regardless of size (for example, `'HHHHHHHHHHHHHHH'` will work, and `'HelloHelloHello'` will too)

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
Example #2:
```python
>>> short_string = 'aaa'
>>> esc_comp.compress(short_string)
False
```
False means that compressing this text in this way is ineffective.
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

### F-string
**Compressing:**
```python
>>> import esc_comp
>>> very_long_string = "+" * 1000000
>>> not_very_long_f_string = esc_comp.compress(very_long_string, mode="py_format")
>>> not_very_long_f_string
'f"{\'+\'*1000000}"'
```
**Decompressing (dangerous):**
```python
>>> not_very_long_f_string = 'f"{\'+\'*1000000}"'
>>> very_long_string = eval(not_very_long_f_string)
```
