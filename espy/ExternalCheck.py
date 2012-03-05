from espy.EspyBase import EspyBase
import re

#
# External file checker.
#
class ExternalChecker (EspyBase):
    
    def prefix(self):
        return "cmd"
    
    def __str__(self):
        return "External Command"
        
    def check(self, req_line):
        """
        Try and check an external command version, with the request line of the
        form:
    
            ext /path/to/command [optional switch] comp "SEMVER"
    
        Example:
    
            ext mongodb [--version] >= 2.0.0
        """
    
        extlib_re = r'cmd\s+([^\s\[\]]+)\s*(\[\S+\])?\s+(\S+)\s*((\d+\.\d+)(\.\d+)?)'
        extlib_match = re.compile(extlib_re).match
    
        req = extlib_match(req_line)
    
        if req is None:
            print "The requirement line couldn't be parsed:\n\t%s" % (req_line)
    
        req_cmd = req.groups()[0]
        req_flag = req.groups()[1]
        if req_flag is not None:
            req_flag = req_flag.strip("[]")
        req_comp = req.groups()[2].strip()
        req_ver = req.groups()[3]
    
        if self.options.verbose:
            print ":: Req parse:\n\t", req.groups()
            print ":: Trying requirement\n\t", req_cmd, req_flag, req_comp, req_ver
        
        # track things
        req_found = False
        req_msg = None
        cmd_ver = None

        # try and run the command
        cmd_res = []
    
        if req_flag is not None:
            cmd_res = getCommandResults([req_cmd, req_flag])
        else:
            # try some basic heuristics
            h_flags = ["--version", "--help"]
            for h_flag in h_flags:
                cmd_res = self.getCommandResults([req_cmd, h_flag])
                if len(cmd_res) > 0:
                    break
    
        if len(cmd_res) == 0:
            req_msg = "External command [%s] not found" % (req_cmd)
        else:
            # try and parse out a version from the mess of results
            ver_search = re.compile(r'((\d+\.\d+)(\.\d+)?)').search
        
            for line in cmd_res:
                ver_res = ver_search(line)
                if ver_res is not None:
                    # we have a result
                    cmd_ver = ver_res.groups()[0]
                    if self.options.verbose:
                        print "Found library version from regex search: ", cmd_ver
                    break
            if cmd_ver is None:
                req_msg = "Couldn't ascertain version of [%s]" % (req_cmd)
            
        # If we have a version, we can keep going
        if cmd_ver is not None:
            # break out our versions
            req_ver_tuple = tuple([int(c) for c in req_ver.split('.')])
            cmd_ver_tuple = tuple([int(c) for c in cmd_ver.split('.')])
        
            # figure out our comparisons
            fit = self.eval_cmp(req_comp, cmd_ver_tuple, req_ver_tuple)
            if fit:
                req_found = True
            else:
                req_msg = "Expected [%s] version %s %s, found %s" % (req_cmd, req_comp, req_ver, cmd_ver)
        
        # finally we can print some results
        print "%s %s %s ..." % (req_cmd, req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        