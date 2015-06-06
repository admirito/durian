#!/usr/bin/env python
#
# Durian Debian Deployer
# Originally Developed by Mohammad Razavi <mrazavi64 at gmail dot com>
#

"""\
DurianManager is a python modules that provides facilities for Durian python
plugins.
"""

import os, sys, subprocess

class Durian:
    def call(self, *args, **kwargs):
        """\
        Call druian instance with @args as arguments. You can also
        provide an "input" keyword argument to provide stdin for the
        durian execution.
        """
        exe = os.environ.get("DURIAN_EXE") or "durian"

        pop = lambda x: kwargs.pop(x, "NONE")
        setdefault = lambda x: subprocess.PIPE if x == "NONE" else x

        stdout, stderr, stdin = map(pop, ["stdout", "stderr", "stdin"])
        stdout, stderr, stdin = map(setdefault, [stdout, stderr, stdin])

        try:
            p = subprocess.Popen((exe,) + args, \
                                 stdout = stdout, \
                                 stderr = stderr, \
                                 stdin = stdin)
            stdout, stderr = p.communicate(**kwargs)
            retcode = p.returncode
        except Exception as e:
            stderr = "Error while calling durian: {0}\n".format(e)
            stdout = ""
            retcode = 1

        return retcode, stdout, stderr