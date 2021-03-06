#! /usr/bin/env python

import sys, os
import getopt
import matplotlib.pyplot as plt
import numpy as np

# PYTHON RPT File Plotter
# ~~~~~~~~~~~~~~~~~~~~~~~
# just add files to plot as arguments


usetext="""
Usage: rptplot [options...] input.rpt input2.rpt ...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Possible options are:
  -t, --title           set title
  -x, --xlabel          set xlabel
  -y, --ylabel          set ylabel
  --xlim                set xlim as 'min,max'
  --ylim                set ylim as 'min,max'
  --size                set figure size
  --axis                set axis dimensions 
                        (left, bottom, right, top)
  -l                    set default legend (based on file name)
  -g, --grid            set grid
  -p, --pdf             writes pdf instead of screen output
  -s, --scalefactor     set a scale factor for each argument
                        has to be a string with comma separated values.
                        e.g. -s '1.4, 4, 10'
  --scalenoiso          scale non-isotropic, additional scalefactor for y values
  --xshift              shift data in x for each argument
  --yshift              shift data in y for each argument
  --scaleall            apply given transformation to all datasets
  --style               set the style for every argument
                        e.g. --style '-k, --g, :r'
  -a                    creates markers with a given distance for each argument
  --lw                  set linewidth for each argument
  -n                    skip non-isotropic note
  -c                    set clipping of lines and markers OFF
  --legend              set a legend entry for each argument
                        has to be a string with comma separated values.
                        If None is specified no legend is plotted for this dataset.
                        e.g. --legend 'Plot 1, Plot 2, Plot 3'
  --legloc              specify the legend location, default: 'best'
  --baseaxis            plot origin axis
  --mplstyle            use mpltools stylefile
                        e.g. --mplstyle 'style1'
  -d                    copy rptscript to folder, for extended modification
  -h, --help            print this help message

Uses the matplotlib library as plotting tool. This library
has to be available. Default axes labels are Force and Displacement
"""
########################################
# Method definitions
############################################################

def usage():
    print usetext

def raw_string(s):
    ''' convert string to raw string '''
    if isinstance(s, str):
        s = s.encode('string-escape')
    elif isinstance(s, unicode):
        s = s.encode('unicode-escape')
    return s

############################################################
# Main program
############################################################

try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:s:x:y:glpnda:c", ["help", "title=","scalefactor=", "xlabel=", "ylabel=", "nogrid", "legend=", "pdf", "scalenoiso=", "style=", "legloc=", "xlim=", "ylim=", "lw=","size=", "xshift=", "yshift=", "mplstyle=", "axis=", "scaleall", "baseaxis"]) 
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

#default scalefactor, scalelist
sf = 1
sl = [sf]*len(args)
sln = [sf]*len(args)
ll = False
ls = False
legloc='best'
pdf = False
style=[]
n = False
clip = True
smooth = [False]*len(args)
xl, yl = [], []
lw = [1]*len(args)
xshift = [0]*len(args)
yshift = [0]*len(args)
scall = False
ba = False

# specify mpltools style files - has to be done in advance
for o, a  in opts:
    if '--mplstyle' in o:
        from mpltools import style as mplstyle
        mplstyle.use(a)
    elif '--scaleall' in o:
        scall = True
        print 'Scale All active!'

# create plot figure with default options
#fig = plt.figure(1,(11.5,8.3))
fig = plt.figure(1)
#ax1 = plt.axes([0.10,0.10,0.8,0.8])
ax1 = fig.add_subplot(111)
plt.xlabel("Displacement")
plt.ylabel("Force")
#plt.grid(True)

# use arguments
for o, a  in opts:
    # set title
    if o in ('-t','--title'): 
        plt.title(a)
    # set xlabel
    elif o in ('-x','--xlabel'): 
        plt.xlabel(a)
    # set ylabel
    elif o in ('-y','--ylabel'): 
        plt.ylabel(a)
    # set grid flag
    elif o in ('-g','--nogrid'): 
        plt.grid(True)
    # check pdf flag
    elif o in ('-p','--pdf'): 
        pdf = True
    # check clipping flag
    elif o in ('-c'):
        clip = False
    # check origin axis flag
    elif o in ('--baseaxis'):
        ba = True
    # check and set xlim
    elif o in ('--xlim'): 
        xl = [float(i) for i in a.split(',')]
        if len(xl)==2:
            pass
        else:
            print 'Check number of entries! Need 2!'
            print 'Arguments: ' + str(args)
            usage()
            sys.exit(2)
    # check and set ylim
    elif o in ('--ylim'): 
        yl = [float(i) for i in a.split(',')]
        if len(yl)==2:
            pass
        else:
            print 'Check number of entries! Need 2!'
            print 'Arguments: ' + str(args)
            usage()
            sys.exit(2)
    # check and set scalefactor
    elif o in ('-s','--scalefactor'): 
        sl = [float(i) for i in a.split(',')]
        if len(sl)>=len(args):
            pass
        else:
            if len(sl) > 0 and scall:
                sl = [sl[0]]*len(args)
            else:
                sl += [1.0]*(len(args)-len(sl))
                print 'Check number of entries!'
                print 'Scalefactor of 1 is used for non defined'
                print 'Arguments: ' + str(args)
                print 'Scalefactors: ' + str(sl)
            #usage()
            #sys.exit(2)
    # check and set scalefactor for non isotropic
    elif o in ('--scalenoiso'): 
        sln = [float(i) for i in a.split(',')]
        if len(sln)>=len(args):
            pass
        else:
            if len(sln) > 0 and scall:
                sln = [sln[0]]*len(args)
            else:
                sln += [1.0]*(len(args)-len(sln))
                print 'Check number of entries!'
                print 'Scalefactor of 1 is used for non defined'
                print 'Arguments: ' + str(args)
                print 'Non isotropic scalefactors: ' + str(sln)
            #usage()
            #sys.exit(2)
    # check and set x shift
    elif o in ('--xshift'): 
        xshift = [float(i) for i in a.split(',')]
        if len(xshift)>=len(args):
            pass
        else:
            if len(xshift) > 0 and scall:
                xshift = [xshift[0]]*len(args)
            else:
                xshift = [0]*len(args)
                print 'Check number of entries!'
                print 'Zero x-shift is used for all data'
                print 'Arguments: ' + str(args)
                print 'X shift values: ' + str(sln)
    # check and set y shift
    elif o in ('--yshift'): 
        yshift = [float(i) for i in a.split(',')]
        if len(yshift)>=len(args):
            pass
        else:
            if len(yshift) > 0 and scall:
                yshift = [yshift[0]]*len(args)
            else:
                yshift = [0]*len(args)
                print 'Check number of entries!'
                print 'Zero y-shift is used for all data'
                print 'Arguments: ' + str(args)
                print 'Y shift values: ' + str(sln)
    # set no non-isotropic note flag
    elif o == '-n': 
        n = True
    # set default legend flag
    elif o == '-l': 
        ls = True
    # check and set customized styles
    elif o == '--style': 
        style = a.split(',')
        if len(style)>=len(args):
            pass
        else:
            style += ['-']*(len(args)-len(style))
            print 'Check number of entries!'
            print 'Default line style is used for non-defined'
            print 'Arguments: ' + str(args)
            print 'Styles: ' + str(style)
            #usage()
            #sys.exit(2)
    # set line widths
    elif o in ('--lw'): 
        lw = map(float,a.split(','))
        if len(lw)>=len(args):
            pass
        else:
            lw += [1.0]*(len(args)-len(lw))
            print 'Check number of entries!'
            print 'Default line width is used for non-defined'
            print 'Arguments: ' + str(args)
            print 'Line widths: ' + str(lw)
            #usage()
            #sys.exit(2)
    # set figure size
    elif o == '--size': 
        size = map(float,a.split(','))
        if len(size) == 2:
            fig.set_size_inches(size[0],size[1],forward=True)
        else:
            print 'Check number of entries!'
            print 'Default fiure size is used'
            #usage()
            #sys.exit(2)
    # set axis dimensions
    elif o == '--axis':
        dims = map(float,a.split(','))
        fig.subplots_adjust(*dims)

    # check and set customized legend
    elif o == '--legend': 
        ls = True
        ll = a.split(',')
        # creates problems with mathtext
        #ll = map(raw_string,ll)
        for leg in range(len(ll)):
            if ll[leg]=='None': ll[leg]=None
        if len(ll)>=len(args):
            pass
        else:
            ll += ['No Legend defined']*(len(args)-len(ll))
            print 'Check number of entries!'
            print 'No Legend is added for non-defined'
            print 'Arguments: ' + str(args)
            print 'Legends: ' + str(ll)
            #usage()
            #sys.exit(2)
    # specify legend location
    elif o == '--legloc': 
        legloc = a

    # marker distance (a)
    elif o in ('-a'):
        srad = map(float,a.split(','))
        if len(srad)>=len(args):
            pass
        else:
            srad += [srad[0]]*(len(args)-len(srad))
            print 'Check number of entries!'
            print 'Uniform marker distance used'
            print 'Arguments: ' + str(args)
            print 'Dot-distance: ' + str(srad)
            #usage()
            #sys.exit(2)
        smooth = np.array(srad)!=0
        srad = np.array(srad)**2
    # local copy (dump)
    elif o in ('-d'):
        import os
        os.system('cp /usr2/gager/tools/Scripts/rptplot/rptplot.py .')
        sys.exit(2)
    # help
    elif o in ('-h','--help'): 
        usage()
        sys.exit(2)

#check if axis has been defined:
if ax1 == None:
    ax1 = fig.add_subplot(111)

# set title
if (np.array(sln)!=1).any() and not n:
    ti=ax1.get_title()
    plt.title(ti+' NON-ISOTROPIC SCALING!')

# check arguments
if len(args)==0: 
    print "arguments not defined"
    usage()
    sys.exit(2)

# plot legend
if ll == False:
    ll = [arg.split('/')[-1][:-4]+' ('+str(sl[i])+')' for i, arg in enumerate(args)]

# plot files
for i, arg in enumerate(args):
    data=np.loadtxt(arg,delimiter=None,skiprows=0)

    if smooth[i] and len(style)!=0:
        # visualize dots the graph   

        #create dummy data for legend
        plt.plot(data[:,0][0]*sl[i]+xshift[i],data[:,1][0]*sl[i]*sln[i]+yshift[i], style[i], label=ll[i], lw=lw[i], mfc='None', mew=1.)

        meanxs=[]; meanys=[]
        n=0
        n0=0
        xv = data[:,0]
        yv = data[:,1]
        meanxs.append(xv[n])
        meanys.append(yv[n])

        while n<len(xv)-1:
            if (xv[n]-xv[n0])**2+(yv[n]-yv[n0])**2 < srad[i]:
                n+=1
            else:
                meanxs.append(xv[n])
                meanys.append(yv[n])
                n0=n

        meanxs.append(xv[n])
        meanys.append(yv[n])

        plt.plot(data[:,0]*sl[i]+xshift[i],data[:,1]*sl[i]*sln[i]+yshift[i], style[i], marker='', lw=lw[i])
        data = np.hstack((np.array(meanxs)[:,np.newaxis],np.array(meanys)[:,np.newaxis]))
        plt.plot(data[:,0]*sl[i]+xshift[i],data[:,1]*sl[i]*sln[i]+yshift[i], style[i], linestyle='', mfc='None', mew=1.)

    else:
        if len(style) == 0:
            plt.plot(data[:,0]*sl[i]+xshift[i],data[:,1]*sl[i]*sln[i]+yshift[i], label=ll[i], lw=lw[i])
        else:
            plt.plot(data[:,0]*sl[i]+xshift[i],data[:,1]*sl[i]*sln[i]+yshift[i], style[i], label=ll[i], lw=lw[i], mfc='None', mew=1.)

if ls == True:
    plt.legend(loc= legloc)

if len(xl)==2:
    plt.xlim(xl)

if len(yl)==2:
    plt.ylim(yl)

if not clip:
    for ob in ax1.lines:
        ob.set_clip_on(False)
#base axis
if ba:
    plt.autoscale(False)
    plt.plot([-10000,10000],[0,0],'k-', lw=0.5, label=None)
    plt.plot([0,0],[-10000,10000],'k-', lw=0.5, label=None)
    
# show plot or write pdf
if pdf:
    plt.savefig('RPToutput.pdf')
else:
    plt.show()
