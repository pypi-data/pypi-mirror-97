#!/bin/env python3
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""This script re-order YAML map keys to be more idiomatic.
The process only support flat list of ansible task or zuul definition in the form:

- key: value

- job:
    key: value
"""

from typing import List, Tuple
import argparse
import sys


keys_order = (
    "name",
    "parent",
    "description",
    "run",
    "pre-run",
    "post-run",
    "when",
    "become",
    "loop",
    "register",
)


def reorder_items(prefix: str, items: List[str]) -> List[str]:
    """Reorder a list of items according to keys_order

    >>> reorder_items('  ', ['  run: test', '  name: n'])
    ['  name: n', '  run: test']
    """
    ordered_pos = [
        pos
        for key in keys_order
        for (pos, elem) in enumerate(items)
        if elem.startswith(prefix + key + ":")
    ]
    rest_pos = [pos for pos in range(len(items)) if pos not in ordered_pos]
    return list(map(lambda pos: items[pos], ordered_pos + rest_pos))


def split_blocks(content: str) -> Tuple[str, List[str]]:
    """Split a YAML file into a list of block per element.

    >>> nl = chr(10)
    >>> split_blocks(nl + '- elem: 42' + nl + '  key: 44' + nl + '- other: 43')
    ('', ['  elem: 42\\n  key: 44', '  other: 43'])
    """

    def remove_tick(line: str) -> str:
        return "  " + line[2:] if line.startswith("- ") else line

    block: List[str] = []
    result: List[str] = []
    header = content[: content.index("\n-")]
    lines = content[content.index("\n-") + 1 :].split("\n")
    for line in map(str.rstrip, filter(lambda line: line != "", lines + ["-"])):
        if line and line[0] == "-" and block:
            result.append("\n".join(list(map(remove_tick, block))))
            block = [line]
        else:
            block.append(line)
    return header, result


def split_items(content: str) -> List[str]:
    """Split a YAML map into a list of items.

    >>> nl = chr(10)
    >>> split_items('  key: |' + nl + '    str' + nl + '  attr: value')
    ['  key: |\\n    str', '  attr: value']
    """
    result: List[str] = []
    prefix = "    " if content.startswith("    ") else "  "
    item, pos = "", 0
    content = "\n" + content + "\n" + prefix + "eof"
    for pos in range(len(content)):
        if (
            content[pos:].startswith("\n" + prefix)
            and content[pos + len(prefix) + 1] != " "
        ):
            result.append(item[1:])
            item = content[pos]
        else:
            item += content[pos]

    return result[1:]


def reorder(block: str) -> str:
    """Re-order the block lines."""

    zuul_objs = (
        "job",
        "nodeset",
        "project",
        "tenant",
        "secret",
        "semaphore",
        "pipeline",
        "project-template",
    )
    is_zuul = block and any(
        map(lambda n: block.startswith("  " + n + ":\n"), zuul_objs)
    )
    if is_zuul:
        prefix = "    "
        header_, keys = block.split("\n", 1)
        header = header_ + "\n"
    else:
        prefix = "  "
        header, keys = "", block
    return header + "\n".join(reorder_items(prefix, split_items(keys)))


def unblocks(blocks: List[str]) -> str:
    def add_tick(block: str) -> str:
        return "-" + block[1:]

    return "\n\n".join(map(add_tick, blocks))


def fmt(content: str) -> str:
    header, blocks = split_blocks(content)
    return header + "\n" + unblocks(list(map(reorder, blocks))) + "\n"


def usage() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zuul config formatter")
    parser.add_argument("--file")
    return parser.parse_args()


def main() -> None:
    args = usage()
    if args.file:
        content = open(args.file).read()
    else:
        content = sys.stdin.read()
    formated_content = fmt(content)
    if args.file:
        open(args.file, "w").write(formated_content)
    else:
        print(formated_content, end="")


if __name__ == "__main__":
    main()
