class EspyEngine (object):
    def __init__(self):
        pass
    
    def includeModules(self, modules):
        pass
        
    def run(self):
        """
        
          * Check for pre-conditions
          * How to do groupings
          * How to push output (console/web/etc)
          * sections versus internals
          * Recursive?
        """
        pass
    
    def evalSyntax(self):
        """
        The expected return value from any syntax processing module:
            
            {
                name: "descriptive name of what was being checked",
                status: [pass, fail, unknown, error, skipped],
                postconditions: [],
                discard: True/False
            }
            
        Questions:
        
          * How to run shortforms
          * How to run longforms
          * How to specify configs for longforms
          * Capture of pre/post conditionals
          * Injection of rewrites/transforms
        """
        pass