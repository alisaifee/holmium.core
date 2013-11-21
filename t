#!/usr/bin/env python 
import os 
import sys 
if not os.path.isdir(".test_env"):
    os.mkdir(".test_env")
os.system("virtualenv .test_env -q")
os.system("./.test_env/bin/pip install -r test_requirements.txt -q")
os.system("./.test_env/bin/nosetests %s" % " ".join(sys.argv[1:]))

