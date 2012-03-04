import subprocess

class EspyBase (object):
    def __init__(self, opts):
        self.options = opts
    
    def eval_cmp(self, op, mod_tuple, req_tuple):
        # fix the tuples if need be (2 => 3)
        mod_tuple = self.pad_tuple(mod_tuple)
        req_tuple = self.pad_tuple(req_tuple)
        
        # find the comparison
        ver_cmp = cmp(mod_tuple, req_tuple)
        
        # vet the comparison versus the operators
        ops = {
            ">": lambda c: c == 1,
            ">=": lambda c: c >= 0,
            "=": lambda c: c == 0,
            "<": lambda c: c < 0,
            "<=": lambda c: c <= 0,
            "!=": lambda c: c != 0
        }
        
        return ops[op.strip()](ver_cmp)
    
    def pad_tuple(self, t):
        if len(t) < 3:
            t = tuple(list(t) + [0 for i in range(0, 3 - len(t))])
        return t
    
    def getCommandResults(self, cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lines = []
            for line in p.stdout:
                lines.append(line)
            for line in p.stderr:
                lines.append(line)
            return lines
        except:
            return []
    