from __future__ import annotations

from typing import Any


## Internal helpers ##

def _dict_get(data: dict, keys: list) -> Any:
    for key in keys:
        data = data[key]

    return data


def _dict_set(data: dict, keys: list, value: Any) -> dict:
    if len(keys) > 1:
        data[keys[0]] = _dict_set(data[keys[0]], keys[1:], value)
    else:
        data[keys[0]] = value

    return data


def _list_to_dict(l: list) -> dict:
    return {i: l[i] for i in range(len(l))}


## Main load/dump string functions ##

def loads(text: str) -> dict | list:
    data = {}

    nesting = []
    countings = [0]
    is_list = [True]

    for line in text.split("\n"):

        line = line.strip()

        if line == "":
            continue

        elif line.startswith("#") or line.startswith("//"):
            continue

        elif line.upper() == "END":
            if is_list.pop():
                _dict_set(data, nesting, list(_dict_get(data, nesting).values()))
            nesting.pop()
            countings.pop()

        elif "=" in line:

            parts = line.split("=", 1)

            parts[0] = parts[0].strip()
            parts[1] = parts[1].strip()

            if parts[0] == "":
                parts[0] = str(countings[-1])
                countings[-1] += 1

            else:
                try:
                    countings[-1] = int(parts[0]) + 1
                except ValueError:
                    is_list[-1] = False

            if parts[1] == "":
                nesting.append(parts[0])
                countings.append(0)
                is_list.append(True)
                _dict_set(data, nesting, {})

            else:
                _dict_set(data, nesting + [parts[0]], parts[1])

        else:
            print("Invalid line:", repr(line))

    if is_list.pop():
        data = list(data.values())

    return data


def dumps(data: dict | list | tuple, indent="    ", *, _indent_level=0) -> str:
    text = ""

    i = 0

    for key, value in data.items():
        text += indent * _indent_level

        try:
            if int(key) == i:
                text += "="
            i += 1
        except ValueError:
            text += str(key) + " ="

        if isinstance(value, dict):
            text += "\n"
            text += dumps(value, indent, _indent_level=_indent_level + 1)
            text += (indent * _indent_level) + "END\n"

        elif isinstance(value, (list, tuple)):
            text += "\n"
            text += dumps(_list_to_dict(value), indent, _indent_level=_indent_level + 1)
            text += (indent * _indent_level) + "END\n"

        else:
            text += " " + str(value) + "\n"

    return text


## __main__ ##
if __name__ == "__main__":
    import json

    with open("test.sod", "r") as file:
        text = file.read()

    data = loads(text)
    print(json.dumps(data, indent=4))
    dumped = dumps(data)

    with open("done.sod", "w") as file:
        file.write(dumped)
