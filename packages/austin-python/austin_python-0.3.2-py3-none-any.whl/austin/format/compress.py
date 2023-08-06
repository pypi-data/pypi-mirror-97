# This file is part of "austin-python" which is released under GPL.
#
# See file LICENCE or go to http://www.gnu.org/licenses/ for full license
# details.
#
# austin-python is a Python wrapper around Austin, the CPython frame stack
# sampler.
#
# Copyright (c) 2018-2020 Gabriele N. Tornetta <phoenix1987@gmail.com>.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import TextIO

from austin.stats import InvalidSample, Metrics, ZERO


def compress(source: TextIO, dest: TextIO, counts: bool = False) -> None:
    """Compress the source stream.

    Aggregates the metrics on equal collapsed stacks. If ``counts`` is ``True``
    then time samples are counted by occurrence rather than by sampling
    duration.
    """
    stats = {}

    for line in source:
        try:
            metrics, head = Metrics.parse(line)
            if counts and metrics.time > 1:
                metrics = Metrics(1, metrics.memory_alloc, metrics.memory_dealloc)
        except InvalidSample:
            continue
        if metrics:
            stats[head] = stats.get(head, ZERO) + metrics

    dest.writelines(
        [head + " " + str(metrics) + "\n" for head, metrics in stats.items()]
    )


def main() -> None:
    """austin-compress entry point."""
    from argparse import ArgumentParser

    arg_parser = ArgumentParser(
        prog="austin-compress",
        description=(
            "Compress a raw Austin sample file by aggregating the collected samples."
        ),
    )

    arg_parser.add_argument(
        "input",
        type=str,
        help="The input file containing Austin samples.",
    )
    arg_parser.add_argument(
        "output",
        type=str,
        help="The output file; defaults to the input file for in-place compression.",
    )

    arg_parser.add_argument(
        "-c",
        "--counts",
        action="store_true",
        default=False,
        help="Use sample counts instead of measured sampling durations.",
    )

    arg_parser.add_argument("-V", "--version", action="version", version="0.2.0")

    args = arg_parser.parse_args()

    try:
        with open(args.input, "r") as fin, open(args.output or args.input, "w") as fout:
            compress(fin, fout, args.counts)
    except FileNotFoundError:
        print(f"No such input file: {args.input}")
        exit(1)


if __name__ == "__main__":
    main()
