from espy.EspyBase import EspyBase
import re

#
# External file checker.
#
class PerlModuleChecker (EspyBase):
    
    def prefix(self):
        return "pl"
    
    def __str__(self):
        return "Perl Module"
        
    def check(self, req_line):
        """
        Try and check for a Perl Module, with the following:
    
            pl name comp "SEMVER"
    
        Example:
    
            pl Date::Calc >= 2.5
            
        """
        pllib_re = r'pl\s+(\S+)\s+(\S+)\s*((\d+\.\d+)(\.\d+)?)'
        pllib_match = re.compile(pllib_re).match
    
        req = pllib_match(req_line)
    
        if req is None:
            print "The requirement line couldn't be parsed:\n\t%s" % (req_line)
    
        req_mod = req.groups()[0]
        req_comp = req.groups()[1].strip()
        req_ver = req.groups()[2]
    
        if self.options.verbose:
            print ":: Req parse:\n\t", req.groups()
            print ":: Trying requirement\n\t", reg_mod, req_comp, req_ver
        
        # track things
        req_found = False
        req_msg = None

        # try and run the command
        cmd_res = self.getCommandResults(['perl', "-M%s" % (req_mod), '-e', "print $%s::VERSION" %(req_mod)])
        
        # get the tuple for our requirement
        mod_ver = None
        
        # look through the lines for our module
        for mod_line in cmd_res:
            if mod_line[0].isdigit():
                mod_ver = mod_line
                break
                    
        # If we have a version, we can keep going
        if mod_ver is not None:
            # break out our versions
            req_ver_tuple = tuple([int(c) for c in req_ver.split('.')])
            mod_ver_tuple = tuple([int(c) for c in mod_ver.split('.')])
        
            # figure out our comparisons
            fit = self.eval_cmp(req_comp, mod_ver_tuple, req_ver_tuple)
            if fit:
                req_found = True
            else:
                req_msg = "Expected [%s] version %s %s, found %s" % (req_mod, req_comp, req_ver, mod_ver)
        else:
            req_msg = "Perl module %s not installed" % (req_mod)
                            
        # finally we can print some results
        print "%s %s %s ..." % (req_mod, req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        
