#run "nosetests" at the root directory of the program


import os, subprocess, re, shutil, time
import nose
from nose.tools import *
import string, random

from tempfile import mkdtemp

def test_basic():
    mydir = mkdtemp()
    
    config = "in=infile1.dat\n"
    config+= "out=folders\n"
    config+= "$MYVAR\n"
    config+= "1 2 3 4 5 6\n"
    
    open(os.path.join(mydir, "var.conf"), "w").write(config)
    
    sample = "This is a simple text with a Variable MYVAR which is being replaced"
    
    open(os.path.join(mydir, "infile1.dat"), "w").write(sample)

    #run it:
    os.system("python var.py %s"%(os.path.join(mydir, "var.conf")))
    
    ld = os.listdir(mydir)
    assert "MYVAR_1" in ld
    assert "MYVAR_6" in ld
    
    content3 = open(os.path.join(mydir, "MYVAR_3", "infile1.dat")).read()
    assert "ext with a Variable 3 which is bein" in content3
    
    #and cleanup ..TODO write a teardown method
    shutil.rmtree(mydir)
    
    
