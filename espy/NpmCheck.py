from espy.EspyBase import EspyBase
import re

#
# External file checker.
#
class NpmChecker (EspyBase):
    
    def prefix(self):
        return "npm"
    
    def __str__(self):
        return "Node.js Module"
        
    def check(self, req_line):
        """
        Try and check for a Node Library, with the following:
    
            npm name comp "SEMVER"
    
        Example:
    
            npm mongoose >= 2.5
            
            
        list via:
            npm ls -g
        """
        npmlib_re = r'npm\s+(\S+)\s+(\S+)\s*((\d+\.\d+)(\.\d+)?)'
        npmlib_match = re.compile(npmlib_re).match
    
        req = npmlib_match(req_line)
    
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
        cmd_res = self.getCommandResults(['npm', 'ls', '-g'])
        cmd_res += self.getCommandResults(['npm', 'ls'])
        
        # get the tuple for our requirement
        mod_ver = None
        
        # look through the lines for our module
        for mod_line in cmd_res:
            if '@' not in mod_line:
                continue
            mod_line = mod_line.strip()
            mod_line = mod_line[mod_line.rindex(' '):].strip()
            
            if mod_line.startswith(req_mod):
                
                mod_ver = mod_line.split('@')[1]
                    
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
            req_msg = "NPM module %s not installed" % (req_mod)
                            
        # finally we can print some results
        print "%s %s %s ..." % (req_mod, req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        
