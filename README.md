*Please do not use this script, although it works, it is still sometimes ineffective.*
# escape-compression
Simple file compression

## Usage
**Compressing:**
```python
import esc_comp
very_long_string = "..."
not_very_long_string = esc_comp.repetitions(very_long_string)
```
**Decompressing:**
```python
import esc_comp
not_very_long_string = "..."
very_long_string = esc_comp.decode(not_very_long_string)
```
