import espy.EspyBase
import re

#
# Check the installed version of Python
#
class PythonChecker (espy.EspyBase.EspyBase):
    
    def prefix(self):
        return "python"
    
    def __str__(self):
        return "CPython Runtime"
        
    def check(self, req_line):
        """
        Test for a specific version of Python. This is a simple version of the
        *check_ext* method.
    
            python <comp> "SEMVER"
        """
        python_re = r'python\s+(.+)\s*((\d+\.\d+)(\.\d+)?)'
        python_match = re.compile(python_re).match
    
        req = python_match(req_line)
    
        if req is None:
            print "The requirement line couldn't be parsed:\n\t%s" % (req_line)
    
        req_comp = req.groups()[0].strip()
        req_ver = req.groups()[1]
    
        if self.options.verbose:
            print ":: Trying python requirement\n\t", req_comp, req_ver
        
        # track things
        req_found = False
        req_msg = None
        cmd_ver = None

        # try and run the command
        cmd_res = self.getCommandResults(["python", "--version"])
    
        if len(cmd_res) == 0:
            req_msg = "Python not found. How you got this message is beyond me."
        else:
            # try and parse out a version from the mess of results
            ver_search = re.compile(r'(\d+\.\d+\.\d+)').search
        
            for line in cmd_res:
                ver_res = ver_search(line)
                if ver_res is not None:
                    # we have a result
                    cmd_ver = ver_res.groups()[0]
                    if self.options.verbose:
                        print "Found library version from regex search: ", cmd_ver
                    break
            if cmd_ver is None:
                req_msg = "Couldn't ascertain version of Python" % (req_cmd)
            
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
                req_msg = "Expected Python version %s %s, found %s" % (req_comp, req_ver, cmd_ver)
        
        # finally we can print some results
        print "Python %s %s ..." % (req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        