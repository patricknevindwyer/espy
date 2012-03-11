# Espy Reqfile version 2 syntax parser
#

# Load base syntax

# Pull syntax from loaded modules list

# parse file and generate AST

# run the AST using the provided set of modules

class EspySyntaxParser (object):
    
    def __init__(self):
        """
        Initialize the Reqfile parser and include the basic syntax elements.
        
          * section
          * include
          * with
        """
        
        # Sigils track the leading indicators for shortforms, while longforms
        # are handled by the _with_ sigil
        self.sigils = {
            'section' : {
                'internal': True,
                'callback': self._create_section
            },
            'include': {
                'internal': True,
                'callback': self._include
            },
            'with': {
                'internal': True,
                'callback': self._with_block
            }
        }
        
        # Setup our parsing queue
        self.parse_queue = []
        
        # Setup the outbound ast
        self.ast = []
        
    def includeSyntaxFrom(self, modules):
        """
        Load the shortform and longform syntax from the provided modules, maintaining
        links back to the module UIDs for later use when building ASTs. Each module
        has three necessary methods (any of which can return None or empty values):
        
          * shortforms() -> [{}]
          * longforms() -> [{}]
          * preconditions() -> {}
        
        The layout of these datastructures, and their purpose, is described below.
        
        # Reqfile syntax
        
        Each Check module can perform multiple different actions, although they should
        be grouped logically by the underlying technologies. The syntax used to describe
        the actions supported by a module can take two forms; shortform and longform.
        
        ## _shortforms_
        
        The _shortform_ syntax is how a single check is specified on a line:
        
            python pymongo exists
            python xlrd > 0.1.0
        
        The above snippit defines two shortform actions, each using the Python check
        module. Shortforms start with a defined sigil, and the remainder is captured
        via regular expression. The sigil must be followed by a space. The shortforms
        for the above syntax might be:
            
            {
                name: 'py_module_exists',
                syntax: r'([^\s]+)\s+exists',
                callback: self.check_py_module_exists,
                preconditions: None,
                sigil: 'python'
            }
            
            {
                name: 'py_module_version',
                syntax: r'([^\s]+)\s+' + SyntaxChunks.VERSION_COMP_REGEX,
                callback: self.check_py_module_version,
                preconditions: None,
                sigil: 'python'            
            }
        
        Note two things of interest comparing these shortforms:
        
          # Both share a sigil; _python_. In this case which ever of the two syntax 
            blocks first match the current line is used.
          # The syntax for *py_module_version* uses a predefined value from 
            SyntaxChunks (in this case captures for the version comparators and the version number)
        
        ## _longforms_
        
        The _longform_ syntax takes a slightly different approach, and instead of applying 
        one action per line, allows the definition of a block of actions related to a module:
        
            with ruby
                actionpack exists
                mysql > 2.4
            end
            
            with mongo using config: db/mongo.yml, environment: dev
                can connect
                has collection prefs, posts in db users
            end
        
        Here we have two _longform_ examples, one checking *Ruby* modules, another testing for the presence and 
        configuration of a MongoDB database. While the Ruby checks would have been two lines instead of
        four using _shortforms_, the MongoDB checks couldn't have been done at all using _shortforms_, because
        only the _longform_ supports inline configuration options.
        
        Let's look at the _longform_ syntax that handles the MongoDB example:
        
            {
                name: 'mongo_with_config',
                callback: self.check_mongo_with_config,
                preconditions: ["command mongod exists"],
                sigil: 'mongo',
                configs: [
                    {
                        name: 'config',
                        required: True
                    },
                    {
                        name: 'environment',
                        required: False,
                        default: "development"
                    }
                ],
                internal_syntax: [
                    {
                        name: 'can_connect',
                        syntax: r'can connect'
                    },
                    {
                        name: 'has_collection',
                        syntax: r'has\s+collection\s+([\S]+,\s*?)+\s*in\sdb\s([\S]+)'
                    }
                ]
            }
        
        That's a bit more complicated, isn't it? Thankfully, most of the _longform_ syntax is the same as you
        would use for a shortform. We have a longform name, a callback, and a sigil. In the longform the sigil
        isn't the first word on a line, rather it's a component of the _with_ syntax.
        
        Our Mongo example brings three new pieces of syntax to the table; preconditions, configs, and internal_syntax.
        
        Preconditions are full Reqfile commands that are issued before a syntax block is checked for the first
        time. In this case, if Espy determines that the *mongo_with_config* longform will be run, it will first
        inject the precondition(s) configured for that longform. In this case, before the first invocation of
        *mongo_with_config* the built in command checker will be run to ensure that the mongod daemon is installed.
        
        If any of the preconditions fail, the syntax block as a whole fails, and internal block commands are not
        run.
        
        Configs allow a module to define what longform configuration options can be passed into the module
        at runtime. Each config option has a _name_, and can be _required_ or optional. There can also be a
        defined default value for each of the config options.
        
        The meat of the _longform_ is embodied in the *internal_syntax*; this is where the individual syntax
        blocks that can occur within the longform as enumerated. For this example we've included two types of
        internal syntax; one that checks that a connection to the MongoDB database can be establised, and
        another that checks for one or more _collections_ within a database.
        """
        pass
    
    def parseReqfile(self, filename):
        """
        Parse a Reqfile using our current syntax state. The result is an AST that links
        actions to either internals or modules. Grouping are maintained by heirarchy,
        allowing for fairly complex groups
        """
        pass
        
    def _create_section(self, line):
        pass
    
    def _include(self, line):
        pass
    
    def _with_block(self, line):
        pass
        
    