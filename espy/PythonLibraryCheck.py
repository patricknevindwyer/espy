from espy.EspyBase import EspyBase
import re

#
# Check python library versions
#

class PythonLibraryChecker (EspyBase):
        
    def prefix(self):
        return "py"
    
    def __str__(self):
        return "Python Module"
        
    def check(self, req_line):
        """
        Try and check a python library version, with the request line of the
        form:
    
            pylib <library name>[optional inspection variable] "SEMVER"
    
        Example:
    
            pylib pymongo[VERSION] >= 2.0.0
        """
        pylib_re = r'py\s+(\w+)(\[\w+\])?\s+(\S+)\s*((\d+\.\d+)(\.\d+)?)'
        pylib_match = re.compile(pylib_re).match
    
        req = pylib_match(req_line)
    
        if req is None:
            print "The requirement line couldn't be parsed:\n\t%s" % (req_line)
    
        req_lib = req.groups()[0]
        req_prop = req.groups()[1].strip('[]')
        req_comp = req.groups()[2].strip()
        req_ver = req.groups()[3]
    
        if self.options.verbose:
            print ":: Trying requirement\n\t", req.groups()
            print "\tprop::", req_prop
        # track things
        req_found = False
        req_msg = None
        mod_ver = None
    
        # try the basic import first
        reqmod = None
        try:
            reqmod = __import__(req_lib)
        except ImportError:
            pass
    
        if reqmod is None:
            req_msg = "[%s] not installed" % (req_lib)
    
        # if we have a module, try and get the version
        if reqmod is not None:
            if req_prop is not None:
                try:
                    # There is a specified property
                    mod_ver = getattr(reqmod, req_prop.strip())
                except AttributeError:
                    req_msg = "[%s] has no version property called [%s]" % (req_lib, req_prop)
            else:
            
                # Look for a version
                for prop in dir(reqmod):
                    if prop.lower() == "version":
                        mod_ver = getattr(reqmod, prop)
                        break
                if mod_ver is None:
                    req_msg = "[%s] has no default version property [VERSION]" % (req_lib)

        # if we have a module and version we can continue
        if mod_ver is not None:
        
            # break out our versions
            req_ver_tuple = tuple([int(c) for c in req_ver.split('.')])
            mod_ver_tuple = tuple([int(c) for c in mod_ver.split('.')])
        
            # figure out our comparisons
            fit = self.eval_cmp(req_comp, mod_ver_tuple, req_ver_tuple)
            if fit:
                req_found = True
            else:
                req_msg = "Expected [%s] version %s %s, found %s" % (req_lib, req_comp, req_ver, mod_ver)
        
        # finally we can print some results
        print "%s %s %s ..." % (req_lib, req_comp, req_ver),
        if req_found:
            print "ok"
        else:
            print "error"
            print "\t", req_msg

        return req_found
        