###############################################################################
# -*- python -*-
#
#       amlPy function implementation
#
#       Copyright or (C) or Copr. 2010 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""pylab plotting nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: py_stat.py 7897 2010-02-09 09:06:21Z cokelaer $ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict
from openalea.core.external import add_docstring


from openalea.stocatree.leaf import Leaf
class LeafConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.leaf import leaf_options as options
        self.add_input(name="fall_probability", interface = IFloat, value=options['fall_probability'])
        self.add_input(name="maturation", interface = IInt, value=12)
        self.add_input(name="mass_per_area", interface = IFloat, value=0.220)
        self.add_input(name="max_area", interface = IFloat, value=0.0030)
        self.add_input(name="min_final_area", interface = IFloat, value=0.0020)
        self.add_input(name="petiole_radius", interface = IFloat, value=0.0006)
        self.add_input(name="preformed_leaves", interface = IInt, value=8)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.leaf import leaf_options as options
        kwds = {}
        for x in options.keys():
            kwds[x] = self.get_input(x)
        return(('leaf', kwds),)


class FruitConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.fruit import config_options as fruit_options

        self.add_input(name="flower_duration", interface = IInt, value=fruit_options['flower_duration'])
        self.add_input(name="max_relative_growth_rate", interface = IFloat, value=fruit_options['max_relative_growth_rate'])
        self.add_input(name="lost_time", interface = IInt, value=fruit_options['lost_time'])
        self.add_input(name="max_age", interface = IInt, value=fruit_options['max_age'])
        self.add_input(name="probability", interface = IFloat, value=fruit_options['probability'])
        self.add_input(name="max_absolute_growth_rate", interface = IFloat, value=fruit_options['max_absolute_growth_rate'])
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.fruit import config_options as fruit_options
        kwds = {}
        for x in fruit_options.keys():
            kwds[x] = self.get_input(x)
        return(('fruit', kwds),)


class ApexConfig(Node):
    """Stocatree configuration file (apex section)"""
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.apex import apex_options
        for key,value in apex_options.iteritems():
            self.add_input(name=key, interface = IFloat, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.apex import apex_options
        kwds = {}
        for x in apex_options.keys():
            kwds[x] = self.get_input(x)
        return(('apex', kwds),)


class MarkovConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.apex import markov_options
        for key,value in markov_options.iteritems():
            self.add_input(name=key, interface = IInt, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.apex import markov_options
        kwds = {}
        for x in markov_options.keys():
            kwds[x] = self.get_input(x)
        return( ('markov', kwds),)



def Config2(*args):
    kwds = {}
    import ConfigParser, os
    config = ConfigParser.ConfigParser()
    for conf in args:
        config.add_section(conf[0])
        for option, value in conf[1].iteritems():
            config.set(conf[0], option, value)

    return (config,)



class Config(Node):
    """Stocatree Configuration file
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='config', interface=ISequence, value = [])
        self.add_output(name="result")

    def __call__(self, inputs):
        import ConfigParser, os
        config = ConfigParser.ConfigParser()
        kwds = {}
        inputs = self.get_input('config')

        # if only one entry (e.g., tuple) is given then convert to a list, 
        # otherwise, there is not need for such conversion, which means that
        # several dictionaries have been connected to the input port.
        if type(inputs)==tuple:
            inputs = list(inputs)
        for input in inputs:
            config.add_section(input[0])
            for option, value in input[1].iteritems():
                config.set(input[0], option, value)

        #config.write(open('/tmp/test.ini', 'w'))
        return (config,)


from openalea.stocatree.wood import Wood
#@add_docstring(Wood)
class WoodConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.wood import wood_options as options
        for key,value in options.iteritems():
            self.add_input(name=key, interface = IFloat, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.wood import wood_options as options
        kwds = {}
        for x in options.keys():
            kwds[x] = self.get_input(x)
        return(('wood',kwds),)

from openalea.stocatree.internode import Internode
#@add_docstring2(Internode)
class InternodeConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.internode import internode_options as options
        for key,value in options.iteritems():
            self.add_input(name=key, interface = IFloat, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.internode import internode_options as options
        kwds = {}
        for x in options.keys():
            kwds[x] = self.get_input(x)
        return(('internode', kwds),)

class TreeConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.apex import markov_options
        for key,value in markov_options.iteritems():
            self.add_input(name=key, interface = IInt, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.apex import markov_options
        kwds = {}
        for x in markov_options.keys():
            kwds[x] = self.get_input(x)
        return(('tree', kwds),)

class OutputConfig(Node):
    def __init__(self):
        Node.__init__(self)
        from openalea.stocatree.output import output_options as options
        for key,value in options.iteritems():
            self.add_input(name=key, interface = IBool, value=value)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.output import output_options as options
        kwds = {}
        for x in options.keys():
            kwds[x] = self.get_input(x)
        return(('output', kwds),)


class GeneralConfig(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="step", interface = IInt, value=100)
        self.add_output(name="result")

    def __call__(self, inputs):
        from openalea.stocatree.apex import markov_options
        kwds = {}
        for x in ['step']:
            kwds[x] = self.get_input(x)
        return(('general', kwds),)
