"""
An argparse.ArgumentParser wrapper to create the arguments and run the methods
"""
import argparse
import inspect
import re
import sys

from polidoro_argument.argument import Argument
from polidoro_argument.command import Command


def get_class_that_defined_object(obj):
    """
    :param obj: The object to get the classe
    :return: the class that define the object
    """

    if inspect.ismethod(obj):
        for cls in inspect.getmro(obj.__self__.__class__):
            if cls.__dict__.get(obj.__name__) is obj:
                return cls
        obj = obj.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(obj):
        cls = getattr(inspect.getmodule(obj),
                      obj.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(obj, '__objclass__', None)


def get_arguments(cmd):
    """
    Get positional and keywords arguments from cmd
    :param cmd: The commando to analyze
    :return:
    """
    positional_arguments = 0
    keyword_arguments = []
    for param in inspect.signature(cmd).parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if param.default == inspect.Parameter.empty:
                positional_arguments += 1
            else:
                keyword_arguments.append(param)
        elif param.kind == inspect.Parameter.POSITIONAL_ONLY:
            positional_arguments += 1
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            keyword_arguments.append(param)
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            positional_arguments = '*'
    return keyword_arguments, positional_arguments


class ArgumentParser(argparse.ArgumentParser):
    """
    An argparse.ArgumentParser wrapper to create the arguments and run the methods
    """

    parsers = {}

    def __new__(cls, *_args, parser_id=None, **_kwargs):
        # to create only one ArgumentParses with the same ID
        if parser_id not in ArgumentParser.parsers:
            return object.__new__(cls)
        return ArgumentParser.parsers[parser_id]

    def __init__(self, *args, version=None, parser_id=None, **kwargs):
        # Only initialize if is a new parser
        if parser_id not in ArgumentParser.parsers:
            kwargs.setdefault('argument_default', argparse.SUPPRESS)
            self.subparsers = None

            super(ArgumentParser, self).__init__(*args, **kwargs)
            if version:
                self.add_argument(
                    '-v',
                    '--version',
                    action='version',
                    version='%(prog)s ' + version
                )

            self.parsers[parser_id] = self
            self.set_defaults(method=self.print_usage)

    def parse_args(self, args=None, namespace=None):
        # Add arguments for each @Argument
        self.add_arguments()

        # Add subparser for each @Command
        self.add_commands()

        namespace, unknown_args = super(ArgumentParser, self).parse_known_args(args, namespace)
        namespace_dict = vars(namespace)
        method = namespace_dict.pop('method', None)
        if method is not None and (method != self.print_usage or unknown_args == []):
            namespace_args = namespace_dict.pop('arguments', [])
            for uk_arg in unknown_args:
                search = re.search('--(?P<key>.*?)=(?P<value>.*)', uk_arg)
                if search:
                    groupdict = search.groupdict()
                    namespace_dict[groupdict['key']] = groupdict['value']

                else:
                    namespace_args.append(uk_arg)

            method_return = method(*namespace_args, **namespace_dict)
            if method_return is None:
                method_return = 0
            sys.exit(method_return)

        return super(ArgumentParser, self).parse_args(args, namespace)

    def add_arguments(self):
        """
        Add arguments to the parser for each @Argument
        """
        for arg in Argument.arguments:
            parser = self.get_final_parser(arg.kwargs['method'], argument=True)
            parser.add_argument(*arg.args, **arg.kwargs)

    def add_commands(self):
        """
        Add commands to the parser for each @Command
        """
        for cmd in Command.commands:
            parser = self.get_final_parser(cmd)

            parser.set_defaults(method=cmd)
            keyword_arguments, positional_arguments = get_arguments(cmd)

            if positional_arguments:
                # Add positional arguments if there is any positional argument
                # and nargs = number of arguments in method
                parser.add_argument('arguments', nargs=positional_arguments)

            if keyword_arguments:
                # Add optional arguments for each keyword argument
                aliases = cmd.kwargs.get('aliases', {})
                helpers = cmd.kwargs.get('helpers', {})
                for kw_arg in keyword_arguments:
                    add_argument_kwargs = {}
                    if isinstance(kw_arg.default, bool):
                        if kw_arg.default:
                            add_argument_kwargs['action'] = 'store_false'
                        else:
                            add_argument_kwargs['action'] = 'store_true'
                    option_string = ['--%s' % kw_arg.name]
                    if kw_arg.name in aliases:
                        option_string.append('-%s' % aliases[kw_arg.name])
                    if kw_arg.name in helpers:
                        add_argument_kwargs['help'] = helpers[kw_arg.name]

                    parser.add_argument(*option_string, **add_argument_kwargs)

    def add_subparsers(self, **kwargs):
        """ Add subparsers if not exists """
        if self.subparsers is None:
            metavar = kwargs.pop('metavar', 'command')
            required = kwargs.pop('required', False)

            self.subparsers = super(ArgumentParser, self).add_subparsers(
                metavar=metavar,
                required=required,
                **kwargs
            )

        return self.subparsers

    def get_final_parser(self, target, argument=False):
        """ Return the final parser creating subparsers if needed """
        final_parser = self
        clazz = get_class_that_defined_object(target)
        full_name = [target]
        while clazz:
            full_name.append(clazz)
            clazz = get_class_that_defined_object(clazz)

        # If is an argument, remove the first name and create subparsers for the others names
        if argument:
            full_name.pop(0)

        # Create or recover the final parser
        parser_name = []
        for trgt in reversed(full_name):
            parser_name.append(trgt.__name__.lower())
            parser_name_id = '.'.join(parser_name)
            if parser_name_id in ArgumentParser.parsers:
                final_parser = ArgumentParser.parsers[parser_name_id]
            else:
                subparsers = final_parser.add_subparsers()
                kwargs = {"parser_id": parser_name_id}
                help = getattr(trgt, 'help', None)
                if help:
                    kwargs["help"] = help
                final_parser = subparsers.add_parser(parser_name[-1], **kwargs)
                default_cmd = getattr(trgt, 'default', None)
                if default_cmd:
                    final_parser.set_defaults(method=getattr(trgt, default_cmd))

        return final_parser
