rpt plotter
===========
Commandline tool to plot space separated files. Currently no
header lines are permitted.


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

