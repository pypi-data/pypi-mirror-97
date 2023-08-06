#!/usr/bin/env python3
"""
A simple sub-command library for writing rich CLIs
"""
import argparse
import collections
import typing as t
from abc import ABC
from abc import abstractproperty
from abc import abstractmethod


def _first_different(s1: str, s2: str) -> int:
    """
    Return index of the first different character in s1 or s2. If the strings
    are the same, raises a ValueError.
    """
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            return i
    if len(s1) == len(s2):
        raise ValueError(f"Duplicate string {s1!r} is not allowed")
    return i + 1


def _unique_prefixes(strings: t.Iterable[str]) -> t.Dict[str, t.List[str]]:
    """
    Helper to find a list of unique prefixes for each string in strings.

    Return a dict mapping each string to a list of prefixes which are unique
    among all other strings within the list. Here is an example:

        >>> _unique_prefixes(["commit", "count", "apply", "app", "shape"])
        {'app': [],
         'apply': ['appl'],
         'commit': ['com', 'comm', 'commi'],
         'count': ['cou', 'coun'],
         'launch': ['la', 'lau', 'laun', 'launc'],
         'list': ['li', 'lis'],
         'shape': ['s', 'sh', 'sha', 'shap']}
    """
    strings = sorted(strings)
    diffs = [0] * len(strings)
    for i, (s1, s2) in enumerate(zip(strings, strings[1:])):
        common = _first_different(s1, s2)
        diffs[i] = max(diffs[i], common)
        diffs[i + 1] = max(diffs[i + 1], common)
    return {
        s: [s[:i] for i in range(x + 1, len(s))]
        for (s, x) in zip(strings, diffs)
    }


class Command(ABC):
    """
    A simple class for implementing sub-commands in your command line
    application. Create a subclass for your app as follows:

        class MyCmd(subc.Command):
            pass

    Then, each command in your app can subclass this, implementing the three
    required fields:

        class HelloWorld(MyCmd):
            name = 'hello-world'
            description = 'say hello'
            def run(self):
                print('hello world')

    Finally, use your app-level subclass for creating an argument parser:

        def main():
            parser = argparse.ArgumentParser(description='a cool tool')
            MyCmd.add_commands(parser)
            args = parser.parse_args()
            args.func(args)
    """

    @abstractproperty
    def name(self) -> str:
        """A field or property which is used for the command name argument"""

    @abstractproperty
    def description(self) -> str:
        """A field or property which is used as the help/description"""

    def add_args(self, parser: argparse.ArgumentParser):
        pass  # default is no arguments

    @abstractmethod
    def run(self) -> t.Any:
        """Function which is called for this command."""

    def base_run(self, args: argparse.Namespace):
        self.args = args
        return self.run()

    @classmethod
    def add_commands(
        cls,
        parser: argparse.ArgumentParser,
        default: t.Optional[str] = None,
        shortest_prefix: bool = False
    ) -> argparse.ArgumentParser:
        """
        Add all subcommands which are descendents of this class to parser.

        This call is required in order to setup an argument parser before
        parsing args and executing sub-command. Each sub-command must be a
        sub-class (or a further descendent) of this class. Only leaf subclasses
        are considered commands -- internal "nodes" in the hierarchy are skipped
        as they are assumed to be helpers.

        A default command to run may be set with 'default'. When the argument
        parser is called without a sub-command, this command will automatically
        execute (rather than simply raising an Exception).

        Shortest prefix sub-command matching allows the user to select a
        sub-command by using any string which is a prefix of exactly one
        command, e.g. "git cl" rather than "git clone".

        :param parser: Argument parser which is already created for this app
        :param default: Name of the command which should be executed if none is
          selected
        :param shortest_prefix: Enable shortest prefix command matching
        :returns: the modified parser (this can be ignored)
        """
        default_set = False
        subparsers = parser.add_subparsers(title='sub-command')
        subclasses = collections.deque(cls.__subclasses__())
        to_add = []
        while subclasses:
            subcls = subclasses.popleft()
            this_node_subclasses = subcls.__subclasses__()
            if this_node_subclasses:
                # Assume that any class with children is not executable. Add
                # its children to the queue (BFS) but do not instantiate it.
                subclasses.extend(this_node_subclasses)
            else:
                to_add.append(subcls())

        if shortest_prefix:
            aliases = _unique_prefixes(c.name for c in to_add)
        else:
            aliases = collections.defaultdict(list)
        for cmd in to_add:
            cmd_parser = subparsers.add_parser(
                cmd.name, description=cmd.description,
                aliases=aliases[cmd.name],
            )
            cmd.add_args(cmd_parser)
            cmd_parser.set_defaults(func=cmd.base_run)
            if cmd.name == default:
                parser.set_defaults(func=cmd.base_run)
                default_set = True

        if not default_set:
            def default_func(*args, **kwargs):
                raise Exception('you must select a sub-command')
            parser.set_defaults(func=default_func)
        return parser

    @classmethod
    def main(
            cls,
            description: str,
            default: t.Optional[str] = None,
            args: t.Optional[t.List[str]] = None,
            shortest_prefix: bool = False,
    ) -> t.Any:
        """
        Parse arguments and run the selected sub-command.

        This helper function is expected to be the main, most useful API for
        subc, although you could directly call the add_commands() method.
        Creates an argument parser, adds every discovered sub-command, parses
        the arguments, and executes the selected sub-command, returning its
        return value.

        Custom arguments (rather than sys.argv) can be specified using "args".
        Details on the arguments "default" and "shortest_prefix" can be found
        in the docstring for add_commands().

        :param description: Description of the application (for help output)
        :param default: Default command name
        :param args: If specified, a list of args to use in place of sys.argv
        :param shortest_prefix: whether to enable prefix matching
        :returns: Return value of the selected command's run() method
        """
        parser = argparse.ArgumentParser(description=description)
        cls.add_commands(
            parser, default=default, shortest_prefix=shortest_prefix,
        )
        ns = parser.parse_args(args=args)
        return ns.func(ns)
