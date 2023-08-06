"""
A wrapper to create custom actions
"""
import sys
from argparse import Action


class CustomAction(Action):  # pylint: disable=too-few-public-methods
    """
    A wrapper to create custom actions
    """

    def __init__(self, *args, method=None, **kwargs):
        self.method = method
        super(CustomAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        resp = self.method(*values)
        if resp is not None:
            print(resp)
        sys.exit(0)
