###############################################################################
# Borrowed from SO query: 
# http://stackoverflow.com/questions/528281/how-can-i-include-an-yaml-file-inside-another
###############################################################################

"""
 Defines a custom PyYAML Loader class that will have and !!include tag for 
 including files on markup. 
 Yet to test. 
 Hopefully this may be included later after some testing. 
"""

import yaml
import os.path


class Loader(yaml.Loader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

    def include(self, node):

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader.include)