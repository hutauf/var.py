#import stuff:
import os, sys
from numpy import linspace
from numpy import arange
import itertools
import copy

#defaults:
configfname = "var.conf"
verbose=False
pattern=""
createaj=False
d={}
infiles=[]

#load config / check for arguments:
if sys.argv[1:]:
    configfname = sys.argv[1]
    configpath = os.path.split(configfname)[0]
    os.chdir(configpath)

config=open(configfname, "r").readlines()

#parse config file:
for line in config:
    if "in=" in line:
        inputfile = line[3:].strip()
        infiles.append(inputfile)
    elif "verbose" in line:
        verbose=True
    elif "createaj=" in line.lower():
        if "yes" in line.lower():
            createaj=True
        else:
            createaj=False
    elif "out=" in line:
        pattern=line[4:]
    elif line.startswith("$"):
        var=line[1:].strip()
    elif line.strip() == "" or line.startswith("#"):
        #comment line, ignore:
        pass
    else:
        line = line.split()
        try:
            assert len(line)==3
            line[0] = float( line[0] )
            line[1] = float( line[1] )
            try:
                line[2] = int(line[2])
                mode="linspace"
                line = linspace(line[0], line[1], line[2])
            except:
                line[2] = float(line[2])
                mode="range"
                line = arange(line[0], line[1], line[2])
        except:
            mode="list"
        print "assuming mode for var %s is %s; values are: %s"%(var, mode, line)
        if var not in d:
            d[var]=[]
        for entry in line:
            entry = str(entry)
            if entry not in d[var]:
                d[var].append(entry)


#assert that mkfolder/files mode is correct
chfilename=False
mkfolder=False
if "files" in pattern and "folders" in pattern:
    chfilename=True
    mkfolder=True
    print "creating folders and renaming input file for all variants"
elif "folder" in pattern:
    chfilename=False
    mkfolder=True
    print "creating folders for all variants"
elif "files" in pattern:
    chfilename=True
    mkfolder=False
    print "creating files for all variants"
elif pattern=="":
    print "*F* pattern=... line is required!"
    exit()
else:
    print "*F* pattern=... not supported. use 'files', 'folders' or 'files and folders'"
    exit()

for inputfile in infiles:
    if not os.path.exists(inputfile):
        print "*F* inputfile does not exist"
        exit()

if verbose:
    print "done analysing config file"

def doStuff(inputfile):
    infile = os.path.abspath(inputfile)
    infilename = os.path.split(infile)[1]
    wd = os.path.split(infile)[0]
    ending = infile.split(".")[-1]
    infile_base = ".".join(infile.split(".")[:-1])

    outfiles = []
    for var in d:
        t=[]
        for entry in d[var]:
            outfname = (var, entry) # "_%s_%s"%(var, entry)
            t.append(outfname)
        outfiles.append(t)

    #magic! combine them:
    combined = list(itertools.product(*outfiles))

    outfiles = []
    outfileobjs = []
    variables = []
    for thing in combined:
        descr = ""
        for va in thing:
            descr+="_%s_%s"%(va[0], va[1])
        variables.append(thing)
        if chfilename:
            outfile = infile_base + descr + "." + ending
        else:
            outfile = infilename
        if mkfolder:
            outfolder = os.path.join(wd, descr[1:])
        else:
            outfolder = wd
        full_path = os.path.join(outfolder, os.path.split(outfile)[-1])
        aj_path = os.path.join(outfolder, "aj")
        outfiles.append(full_path)
        if not os.path.exists(outfolder):
            try:
                os.makedirs(outfolder)
            except:
                pass
        outfileobjs.append(open(full_path, "w"))
        if createaj:
            open(aj_path, "w").write("")

    if verbose:
        print "created %s file object(s) to be filled up"%(len(outfileobjs))
        #get number of lines of inputfile to calculate a status in %
        nlin=0
        inobj = open(infile)
        for lin in inobj:
            nlin+=1
        inobj.close()
        linecount=0 #current line count

    inobj = open(infile)
    for line in inobj:
        if verbose:
            linecount+=1
            if not linecount%1000:
                print "line %s/%s, %s%%"%(linecount, nlin, float(linecount)/nlin*100.)
        for i in xrange(len(outfileobjs)):
            vars = variables[i]
            curline = copy.deepcopy(line)
            for var in vars:
                varname = var[0]
                varval = var[1]
                curline = curline.replace(varname, varval)
            outfileobjs[i].write(curline)
    inobj.close()
    for i in xrange(len(outfileobjs)):
        outfileobjs[i].close()
    
for inputfile in infiles:
    doStuff(inputfile)
    
if verbose:
    print "done!"
