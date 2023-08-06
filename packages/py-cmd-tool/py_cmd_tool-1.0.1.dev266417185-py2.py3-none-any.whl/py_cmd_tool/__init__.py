"""Wrapper to easily define a Python command-line tool.

This wraps argparse, and provides an entry-point string for the package setup.py.

NOTE: Supports Python 3 only

"""
import argparse
from typing import List, Optional, Tuple, Any


class CmdLineArgument(object):
    """Base for our cmdline argument wrapping"""

    def __init__(self, help_text: str,
                 keyword: Optional[str] = None,
                 short_switch: Optional[str] = None,
                 long_switch: Optional[str] = None,
                 action: str = 'store',
                 var_type: type = None,
                 default: Any = None):
        """Construct.

        :param help_text: The argument's help text
        :param keyword: Optional keyword for required, positional arguments
        :param short_switch: Optional short form switch ( "-s" )
        :param long_switch: Optional long form switch ( "--switch" )
        :param var_type: Optional type of variable
        :param default: Optional default for value args
        """
        self.help_text = help_text
        self.keyword = keyword
        self.short_switch = short_switch
        self.long_switch = long_switch
        self.action = action
        self.var_type = var_type
        self.default = default

        if not keyword and not short_switch and not long_switch:
            raise ValueError('Must supply either keyword, or the short or long switch format')

    def add_argument(self, parser: argparse.ArgumentParser, **kwargs):
        """Add this argument to the parser. Overload for more complex handling.

        This automatically handles the option_strings, action and help.

        :param parser:
        :return:
        """
        if self.var_type and 'type' not in kwargs:
            kwargs['type'] = self.var_type

        if self.action and 'action' not in kwargs:
            kwargs['action'] = self.action

        default = kwargs.get('default') or self.default
        kwargs['default'] = default

        parser.add_argument(*self.option_strings, help=self.help_text, **kwargs)

    @property
    def option_strings(self) -> Tuple[str]:
        """Get a tuple with the options from keyword, short and long switches"""
        options = [self.keyword, self.short_switch, self.long_switch]
        options = tuple([k for k in options if k])

        if not options:
            raise ValueError('Missing one of keyword, short_switch and long_switch')

        # noinspection PyTypeChecker
        return options


class PositionalArg(CmdLineArgument):
    """Simple, positional argument"""

    def __init__(self, keyword: str, help_text: str, var_type: type = None):
        super().__init__(keyword=keyword, help_text=help_text, var_type=var_type)


class SwitchValueArg(CmdLineArgument):
    """Simple switch with stored value"""

    def __init__(self, long: str, help_text: str, short: str = None, var_type: type = None, default: Any = None):
        super().__init__(short_switch=short, long_switch=long, help_text=help_text, var_type=var_type, default=default)


class SwitchTrueArg(CmdLineArgument):
    """Simple switch to store true"""

    def __init__(self, long: str, help_text: str, short: str = None, var_type: type = None):
        super().__init__(short_switch=short, long_switch=long, help_text=help_text, var_type=var_type, action='store_true')


class MultiValuesArg(CmdLineArgument):
    """For a switch that can have multiple values"""

    def __init__(self, help_text: str, long: str, short: str = None, nargs: str = '*', var_type: type = None, default: Any = None):
        super().__init__(help_text=help_text, long_switch=long, short_switch=short, var_type=var_type, default=default)

        self.nargs = nargs
        """Default is '*', but can be set to values like '+', or '2' """

    def add_argument(self, parser: argparse.ArgumentParser, **kwargs):
        """Add nargs to arguments."""
        super().add_argument(parser=parser, nargs=self.nargs)


class ChoicesArg(CmdLineArgument):
    """For a list of choices parameter"""

    def __init__(self, choices: List, help_text: str, long: str, short: str = None, var_type: type = None, default: Any = None):
        super().__init__(help_text=help_text, long_switch=long, short_switch=short, var_type=var_type, default=default)

        self.choices = choices

    def add_argument(self, parser: argparse.ArgumentParser, **kwargs):
        """Add choices to arguments."""
        super().add_argument(parser, choices=self.choices)


class RawArg(CmdLineArgument):
    """For cases not covered by these helpers.

    Example that adds "action" and "default".

    .. sourcecode: python

        RawArg(help_text="Sample raw arg", short='-r', long='--raw-arg', action='store', default='raw')

    """

    def __init__(self, help_text: str, long: str, short: str = None, var_type: type = None, **kwargs):
        super().__init__(help_text=help_text, long_switch=long, short_switch=short, var_type=var_type)

        self.extra_kwargs = kwargs

    def add_argument(self, parser: argparse.ArgumentParser, **kwargs):
        """Add raw argument."""
        super().add_argument(parser, **self.extra_kwargs)


class CmdLineTool(object):
    """
    Wrapper to easily define a cmdline tool.

    The tool implementation *must* allow creation with no parameters. This enables registering
    the tool in the setup.py "entry_points.console_scripts" list.

    .. sourcecode: python

        class Tool(CmdLineTool):
            def __init__(self):
                super().__init__(help_title='Test', cmdline_args=[
                    PositionalArg(keyword='name', help_text='Supply a name')
                ])

            def run(self, parsed_cmdline: argparse.Namespace):
                assert parsed_cmdline.name
                print(parsed_cmdline.name)

        Tool.main(['name-is-this'])

    To register within the setup.py (the tool must have no, or default arguments:

    .. sourcecode: python

        entry_points={
            'console_scripts': [
                Tool().console_scripts_line,
            ]

    """

    def __init__(self, help_title: str,
                 cmdline_args: List[CmdLineArgument],
                 install_name: str = None,
                 epilog: str = None):
        """Construct.

        :param help_title: Cmdline help title/description
        :param cmdline_args: List of cmdline arguments
        :param install_name: The cmdline tool name for setup.py to install if present.

        :param epilog: Optional epilog for help
        """
        self.help_title = help_title
        self.cmdline_args = cmdline_args
        self.install_name = install_name
        self.epilog = epilog

    @property
    def console_scripts_line(self) -> str:
        """To reference from the setup.py entry_points.console_scripts list.

        This will reference the current module, class name, and the class `main` method.

        :return:
        """
        if not self.install_name:
            raise ValueError('Class implementation must specify the "install_name"')

        return '{}={}:{}.main'.format(self.install_name, self.__module__, self.__class__.__name__)

    @classmethod
    def main(cls, cmdline=None, **kwargs):
        """The "entry point" for this tool.

        NOTE: The tool class implementation *must* allow no parameters.

        :param cmdline:
        :return:
        """
        tool = cls(**kwargs)

        parsed = tool.parse_args(cmdline=cmdline)
        return tool.run(parsed_cmdline=parsed)

    def parse_args(self, cmdline=None) -> argparse.Namespace:
        """Parse the command-line.

        :param cmdline: Optional for testing
        :return:
        """
        parser = argparse.ArgumentParser(description=self.help_title,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        if self.epilog:
            parser.epilog = self.epilog

        for arg_item in self.cmdline_args:
            arg_item.add_argument(parser=parser)

        parsed = parser.parse_args(args=cmdline)

        return parsed

    def run(self, parsed_cmdline: argparse.Namespace) -> int:
        """Must be implemented by the tool class.

        The entry point "main()" will parse the command-line arguments and then call
        this method with the parsed arguments Namespace object returned from argparse.parse_args.

        :param parsed_cmdline:
        :return: Exit code
        """
        raise NotImplementedError()
