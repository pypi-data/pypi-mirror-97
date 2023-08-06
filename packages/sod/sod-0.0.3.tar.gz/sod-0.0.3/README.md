# sod file format

**W.I.P.**

This is just a really bad file format at the moment - because why not.

## Installation

```terminal
pip intall sod
```

## Usage

```python
import sod

with open("example.sod", "r") as file:
    text = file.read()
    data = sod.loads(text)

with open("example2.sod", "w") as file:
    new_text = sod.dumps(data)
    file.write()

```

