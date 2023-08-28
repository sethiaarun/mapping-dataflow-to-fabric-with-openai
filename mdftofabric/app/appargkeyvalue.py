"""application key value argument parser"""

import argparse


class KwargsAction(argparse.Action):
    """
    type of action to be taken when kwargs is encountered at the command line
    """
    # Constructor calling
    def __call__(self, parser, namespace,
                 values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            # split it into key and value
            key, value = value.split('=')
            # assign into dictionary
            getattr(namespace, self.dest)[key] = value
