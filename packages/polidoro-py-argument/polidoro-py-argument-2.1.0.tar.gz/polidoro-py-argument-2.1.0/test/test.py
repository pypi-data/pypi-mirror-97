"""
Test file
"""
from polidoro_argument.argument import Argument
from polidoro_argument.argument_parser import ArgumentParser
from polidoro_argument.command import Command


@Argument
def simple():
    """ Simple command line argument """
    print('simple')


@Argument(help='1 arg')
def simple_with_arg(arg):
    """ Command line argument with one argument and help """
    print('this is your arg %s' % arg)


@Argument
def simple_with_2_args(arg1, arg2):
    """ Command line argument with two arguments """
    print('those are your args: %s %s' % (arg1, arg2))


@Command
def command():
    """ Command line command """
    print('this is a command')


@Command(help='1 arg')
def command_with_arg(arg, arg1=None):
    """ Command line command with one argument and help """
    print('this the command arg: %s, arg1: %s' % (arg, arg1))


class ClassCommand:
    """ Command line command class """
    @staticmethod
    @Argument
    def argument_in_class():
        """ Class command line argument """
        print('argument_in_class')

    @staticmethod
    @Command
    def command_in_class(arg=None):
        """ Class command line command with arguments """
        print('command_in_class. arg %s' % arg)


parser = ArgumentParser()
parser.parse_args()
