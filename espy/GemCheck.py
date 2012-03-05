from espy.EspyBase import EspyBase
import re

#
# External file checker.
#
class GemChecker (EspyBase):
    
    def prefix(self):
        return "gem"
    
    def __str__(self):
        return "Ruby Gem"
        
    def check(self, req_line):
        """
        Try and check for a Ruby Gem, with the following:
    
            gem name comp "SEMVER"
    
        Example:
    
            gem rack >= 1.0.1
        """
        gemlib_re = r'gem\s+(\S+)\s+(\S+)\s*((\d+\.\d+)(\.\d+)?)'
        gemlib_match = re.compile(gemlib_re).match
    
        req = gemlib_match(req_line)
    
        if req is None:
            print "The requirement line couldn't be parsed:\n\t%s" % (req_line)
    
        req_gem = req.groups()[0]
        req_comp = req.groups()[1].strip()
        req_ver = req.groups()[2]
    
        if self.options.verbose:
            print ":: Req parse:\n\t", req.groups()
            print ":: Trying requirement\n\t", reg_gem, req_comp, req_ver
        
        # track things
        req_found = False
        req_msg = None

        # try and run the command
        cmd_res = self.getCommandResults(['gem', 'list', req_gem])

        # get the tuple for our requirement
        req_ver_tuple = tuple([int(c) for c in req_ver.split('.')])
        found_versions = None
        
        # look through the lines for our gem
        for gem_line in cmd_res:
            if gem_line.startswith(req_gem):
                
                # look for versions, and check to see if any match
                versions = [v.strip() for v in gem_line.strip().split('(')[1].strip(' )').split(',')]
                found_versions = versions
                
                # check each of the versions
                for version in versions:
                    gem_ver_tuple = tuple([int(c) for c in version.split('.')])
                    fit = self.eval_cmp(req_comp, gem_ver_tuple, req_ver_tuple)
                    if fit:
                        req_found = True
        
        if not req_found:
            if found_versions is not None:
                req_msg = "Couldn't find [%s], expected %s %s, found %s" % (req_gem, req_comp, req_ver, found_versions)
            else:
                req_msg = "Gem [%s] not installed" % (req_gem)
                
        # finally we can print some results
        print "%s %s %s ..." % (req_gem, req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        
