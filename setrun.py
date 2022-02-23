"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""
from __future__ import absolute_import
from __future__ import print_function
import os
import numpy as np

#new in 5.6
try:
	CLAW = os.environ['CLAW']
except:
	raise Exception("*** Must first set CLAW environment variable")

#new in 5.6
#scratch director for storing topo and dtopo files:
scratch_dir = os.path.join(CLAW,'geoclaw', 'scratch')


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------
    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

#####
    # Lower and upper edge of computational domain:
    #Long
    clawdata.lower[0] = 93.0 #west
    clawdata.upper[0] = 95.6 #east
    #Lat
    clawdata.lower[1] = 28.0   #south          
    clawdata.upper[1] = 30.0	#north

    # Number of grid cells: Coarsest grid
    clawdata.num_cells[0] = 255 #distance between longitudes
    clawdata.num_cells[1] = 222 #distance between latitudes

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2

    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk03553'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.num_output_times = 2
        clawdata.tfinal = 226800
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0,30,60,90]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 1
        clawdata.output_t0 = True
        

    clawdata.output_format == 'ascii'      # 'ascii' or 'netcdf' 

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'none'  # could be list
    clawdata.output_aux_onlyonce = True    # output aux arrays only at t0



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.016

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.7    
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 50000000
   



    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'

    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 2

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.  
        clawdata.checkpt_times = [183600]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5


#####
    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 6

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [4,2,2,2,2]
    amrdata.refinement_ratios_y = [4,2,2,2,2]
    amrdata.refinement_ratios_t = [4,2,2,2,2]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft','center']


    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag_richardson_tol = 0.002  # Richardson tolerance --this is new in 5.6
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 3

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0


    #  ----- For developers ----- 
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # == setregions.data values ==
    #regions = rundata.regiondata.regions #old from 5.4.1
    rundata.regiondata.regions = [] #new format for 5.6
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2] <-- order: w,e,s,n
    
#AMR zones
    #1 - Lake 3088
    rundata.regiondata.regions.append([5, 5, 0, 1.e10, 94.84, 94.96, 29.54, 29.64])
    #2 
    rundata.regiondata.regions.append([4, 5, 0, 1.e10, 94.79, 94.92, 29.44, 29.54])
    #3
    rundata.regiondata.regions.append([3, 5, 0, 1.e10, 94.65, 94.79, 29.41, 29.51])
    #4
    rundata.regiondata.regions.append([3, 5, 0, 1.e10, 94.49, 94.65, 29.41, 29.53])
    #5
    rundata.regiondata.regions.append([3, 5, 0, 1.e10, 94.34, 94.49, 29.41, 29.55])
    #6 
    rundata.regiondata.regions.append([3, 4, 0, 1.e10, 94.38, 94.49, 29.29, 29.41])
    #7
    rundata.regiondata.regions.append([3, 4, 0, 1.e10, 94.27, 94.38, 29.20, 29.36])
    #8
    rundata.regiondata.regions.append([1, 4, 0, 1.e10, 93.37, 94.27, 29.04, 29.33]) 
    #9
    rundata.regiondata.regions.append([1, 3, 0, 1.e10, 92.96, 93.37, 28.96, 29.19])
    #10
    rundata.regiondata.regions.append([1, 3, 0, 1.e10, 94.29, 94.52, 29.55, 29.75])
    #11
    rundata.regiondata.regions.append([1, 3, 0, 1.e10, 94.03, 94.29, 29.71, 29.77])
    # Confluence with Brahmaputra
    rundata.regiondata.regions.append([1, 4, 0, 184400, 95.19, 95.6, 28.0, 28.18])
    #test 1
    rundata.regiondata.regions.append([1, 3, 184400, 1.e10, 95.19, 95.6, 28.0, 28.18])

#Gauges
    rundata.gaugedata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2, min_time_increment]
    #1
    #rundata.gaugedata.gauges.append([])
    # gauges at every cross section (every 1km) starting at upstream end of lake
    rundata.gaugedata.gauges.append([   0   ,   94.092882   ,   29.203368   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   1   ,   94.102524   ,   29.200908   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   2   ,   94.113198   ,   29.203307   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   3   ,   94.123246   ,   29.20316    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   4   ,   94.133064   ,   29.200036   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   5   ,   94.143307   ,   29.199077   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   6   ,   94.153584   ,   29.198277   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   7   ,   94.163845   ,   29.199951   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   8   ,   94.174467   ,   29.200001   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   9   ,   94.18259    ,   29.204216   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   10  ,   94.189243   ,   29.20994    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   11  ,   94.198893   ,   29.213328   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   12  ,   94.206638   ,   29.220049   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   13  ,   94.214735   ,   29.223263   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   14  ,   94.220856   ,   29.231952   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   15  ,   94.22746    ,   29.236663   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   16  ,   94.23375    ,   29.244133   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   17  ,   94.239186   ,   29.252257   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   18  ,   94.245848   ,   29.258796   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   19  ,   94.254345   ,   29.263563   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   20  ,   94.2621 ,   29.25998    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   21  ,   94.272004   ,   29.250748   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   22  ,   94.282378   ,   29.252455   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   23  ,   94.287965   ,   29.262026   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   24  ,   94.296683   ,   29.267471   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   25  ,   94.303346   ,   29.2737 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   26  ,   94.304159   ,   29.283684   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   27  ,   94.309018   ,   29.291673   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   28  ,   94.317549   ,   29.296874   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   29  ,   94.319182   ,   29.306517   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   30  ,   94.326752   ,   29.312463   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   31  ,   94.335926   ,   29.316618   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   32  ,   94.346303   ,   29.317416   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   33  ,   94.355885   ,   29.321651   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   34  ,   94.362511   ,   29.327471   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   35  ,   94.370817   ,   29.331676   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   36  ,   94.380023   ,   29.336196   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   37  ,   94.387279   ,   29.342322   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   38  ,   94.395286   ,   29.348295   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   39  ,   94.397724   ,   29.358327   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   40  ,   94.407044   ,   29.362929   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   41  ,   94.41443    ,   29.369224   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   42  ,   94.421304   ,   29.375931   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   43  ,   94.425868   ,   29.383919   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   44  ,   94.431977   ,   29.391255   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   45  ,   94.435795   ,   29.39962    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   46  ,   94.440086   ,   29.407748   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   47  ,   94.447418   ,   29.413154   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   48  ,   94.45741    ,   29.415317   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   49  ,   94.467535   ,   29.417601   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   50  ,   94.476154   ,   29.422452   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   51  ,   94.483716   ,   29.428303   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   52  ,   94.48998    ,   29.435811   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   53  ,   94.498641   ,   29.440105   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   54  ,   94.507302   ,   29.4425 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   55  ,   94.515964   ,   29.445056   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   56  ,   94.525451   ,   29.450814   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   57  ,   94.535289   ,   29.448295   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   58  ,   94.545351   ,   29.444931   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   59  ,   94.554462   ,   29.44977    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   60  ,   94.562506   ,   29.455067   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   61  ,   94.563395   ,   29.467541   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   62  ,   94.569045   ,   29.470041   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   63  ,   94.5625 ,   29.483956   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   64  ,   94.573358   ,   29.48432    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   65  ,   94.582622   ,   29.484924   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   66  ,   94.592061   ,   29.482545   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   67  ,   94.600622   ,   29.481326   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   68  ,   94.609189   ,   29.4763 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   69  ,   94.617988   ,   29.472162   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   70  ,   94.628735   ,   29.473345   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   71  ,   94.638334   ,   29.469302   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   72  ,   94.648625   ,   29.469178   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   73  ,   94.658754   ,   29.469582   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   74  ,   94.668796   ,   29.471611   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   75  ,   94.678571   ,   29.470347   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   76  ,   94.685  ,   29.462354   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   77  ,   94.696174   ,   29.46256    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   78  ,   94.705812   ,   29.459197   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   79  ,   94.714056   ,   29.458377   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   80  ,   94.722017   ,   29.45918    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   81  ,   94.73072    ,   29.463292   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   82  ,   94.736675   ,   29.470578   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   83  ,   94.744285   ,   29.476644   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   84  ,   94.753153   ,   29.480993   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   85  ,   94.763354   ,   29.479956   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   86  ,   94.772962   ,   29.479393   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   87  ,   94.782075   ,   29.475323   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   88  ,   94.789215   ,   29.468867   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   89  ,   94.796317   ,   29.46231    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   90  ,   94.806094   ,   29.459615   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   91  ,   94.816203   ,   29.461385   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   92  ,   94.823766   ,   29.466572   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   93  ,   94.824142   ,   29.472693   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   94  ,   94.825992   ,   29.482169   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   95  ,   94.824842   ,   29.491123   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   96  ,   94.829483   ,   29.49884    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   97  ,   94.832515   ,   29.506096   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   98  ,   94.839911   ,   29.512381   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   99  ,   94.848187   ,   29.517474   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   100 ,   94.857495   ,   29.519918   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   101 ,   94.867789   ,   29.520019   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   102 ,   94.87788    ,   29.520758   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   103 ,   94.885914   ,   29.525567   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   104 ,   94.887549   ,   29.53417    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   105 ,   94.887205   ,   29.540888   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   106 ,   94.880791   ,   29.548158   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   107 ,   94.883223   ,   29.55689    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   108 ,   94.889996   ,   29.563739   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   109 ,   94.897909   ,   29.569195   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   110 ,   94.899936   ,   29.577877   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   111 ,   94.906633   ,   29.583304   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   112 ,   94.914531   ,   29.587558   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   113 ,   94.923428   ,   29.588368   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   114 ,   94.92589    ,   29.596641   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   115 ,   94.934337   ,   29.601672   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   116 ,   94.934989   ,   29.608557   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   117 ,   94.928414   ,   29.612571   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   118 ,   94.926668   ,   29.621226   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   119 ,   94.926663   ,   29.629303   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   120 ,   94.918234   ,   29.626678   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   121 ,   94.908698   ,   29.624947   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   122 ,   94.899461   ,   29.627506   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   123 ,   94.887968   ,   29.62503    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   124 ,   94.879787   ,   29.628633   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   125 ,   94.876728   ,   29.636781   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   126 ,   94.882251   ,   29.643715   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   127 ,   94.891324   ,   29.646721   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   128 ,   94.900216   ,   29.651216   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   129 ,   94.90899    ,   29.655827   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   130 ,   94.917191   ,   29.660866   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   131 ,   94.919958   ,   29.6693 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   132 ,   94.918344   ,   29.677579   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   133 ,   94.912668   ,   29.68149    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   134 ,   94.902589   ,   29.680628   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   135 ,   94.893312   ,   29.684442   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   136 ,   94.891584   ,   29.692495   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   137 ,   94.8934 ,   29.700999   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   138 ,   94.900649   ,   29.706666   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   139 ,   94.908329   ,   29.710703   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   140 ,   94.91752    ,   29.715344   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   141 ,   94.925207   ,   29.720776   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   142 ,   94.93414    ,   29.724145   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   143 ,   94.932437   ,   29.732956   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   144 ,   94.932515   ,   29.740755   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   145 ,   94.938108   ,   29.746666   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   146 ,   94.944697   ,   29.75256    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   147 ,   94.953548   ,   29.755833   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   148 ,   94.963506   ,   29.755882   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   149 ,   94.972851   ,   29.759999   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   150 ,   94.982587   ,   29.763342   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   151 ,   94.990616   ,   29.769151   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   152 ,   94.999424   ,   29.768312   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   153 ,   95.00584    ,   29.762775   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   154 ,   95.015246   ,   29.758199   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   155 ,   95.022496   ,   29.752371   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   156 ,   95.031436   ,   29.749223   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   157 ,   95.037424   ,   29.755624   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   158 ,   95.040966   ,   29.762359   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   159 ,   95.049176   ,   29.766671   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   160 ,   95.059015   ,   29.769196   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   161 ,   95.066795   ,   29.76581    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   162 ,   95.072423   ,   29.759545   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   163 ,   95.075793   ,   29.750908   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   164 ,   95.073325   ,   29.742044   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   165 ,   95.081017   ,   29.73666    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   166 ,   95.085393   ,   29.744917   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   167 ,   95.093228   ,   29.749548   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   168 ,   95.101014   ,   29.74751    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   169 ,   95.108002   ,   29.741206   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   170 ,   95.115815   ,   29.746403   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   171 ,   95.12259    ,   29.75282    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   172 ,   95.131258   ,   29.754197   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   173 ,   95.137829   ,   29.76081    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   174 ,   95.145926   ,   29.762364   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   175 ,   95.155064   ,   29.759088   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   176 ,   95.163316   ,   29.76384    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   177 ,   95.173232   ,   29.764387   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   178 ,   95.182374   ,   29.759072   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   179 ,   95.18675    ,   29.762653   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   180 ,   95.187483   ,   29.771029   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   181 ,   95.183795   ,   29.776671   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   182 ,   95.176942   ,   29.782669   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   183 ,   95.172799   ,   29.788134   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   184 ,   95.169943   ,   29.782431   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   185 ,   95.161646   ,   29.787524   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   186 ,   95.153312   ,   29.792616   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   187 ,   95.147453   ,   29.799943   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   188 ,   95.143307   ,   29.808404   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   189 ,   95.135006   ,   29.813958   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   190 ,   95.126298   ,   29.815865   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   191 ,   95.117794   ,   29.82082    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   192 ,   95.113338   ,   29.82783    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   193 ,   95.10326    ,   29.827483   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   194 ,   95.093505   ,   29.829142   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   195 ,   95.090013   ,   29.837078   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   196 ,   95.087323   ,   29.8433 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   197 ,   95.084045   ,   29.850794   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   198 ,   95.092755   ,   29.851658   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   199 ,   95.102357   ,   29.854166   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   200 ,   95.108323   ,   29.861448   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   201 ,   95.11329    ,   29.869354   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   202 ,   95.117389   ,   29.87738    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   203 ,   95.124137   ,   29.873974   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   204 ,   95.131426   ,   29.868039   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   205 ,   95.139336   ,   29.868643   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   206 ,   95.145469   ,   29.875601   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   207 ,   95.147472   ,   29.883844   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   208 ,   95.145764   ,   29.892161   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   209 ,   95.145768   ,   29.900296   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   210 ,   95.153635   ,   29.90418    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   211 ,   95.162492   ,   29.901605   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   212 ,   95.172529   ,   29.90085    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   213 ,   95.182213   ,   29.899878   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   214 ,   95.188411   ,   29.892819   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   215 ,   95.195061   ,   29.886802   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   216 ,   95.192512   ,   29.87945    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   217 ,   95.189867   ,   29.870795   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   218 ,   95.200163   ,   29.872526   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   219 ,   95.207854   ,   29.877436   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   220 ,   95.216876   ,   29.879143   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   221 ,   95.218935   ,   29.873394   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   222 ,   95.210503   ,   29.869117   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   223 ,   95.208305   ,   29.861082   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   224 ,   95.209093   ,   29.852556   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   225 ,   95.204097   ,   29.845202   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   226 ,   95.200015   ,   29.837303   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   227 ,   95.206234   ,   29.829974   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   228 ,   95.21391    ,   29.824874   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   229 ,   95.221162   ,   29.81861    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   230 ,   95.229321   ,   29.817386   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   231 ,   95.235642   ,   29.823358   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   232 ,   95.244913   ,   29.825023   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   233 ,   95.255177   ,   29.82502    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   234 ,   95.26551    ,   29.825071   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   235 ,   95.273981   ,   29.828389   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   236 ,   95.281023   ,   29.831709   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   237 ,   95.285456   ,   29.824866   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   238 ,   95.288363   ,   29.816834   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   239 ,   95.290026   ,   29.808398   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   240 ,   95.292512   ,   29.800135   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   241 ,   95.295914   ,   29.792275   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   242 ,   95.297472   ,   29.783899   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   243 ,   95.295805   ,   29.775454   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   244 ,   95.296599   ,   29.766944   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   245 ,   95.297385   ,   29.759191   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   246 ,   95.303271   ,   29.752194   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   247 ,   95.304129   ,   29.743425   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   248 ,   95.305814   ,   29.734911   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   249 ,   95.310455   ,   29.727489   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   250 ,   95.315902   ,   29.721526   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   251 ,   95.3183 ,   29.713962   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   252 ,   95.322474   ,   29.705725   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   253 ,   95.329249   ,   29.709054   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   254 ,   95.337608   ,   29.710822   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   255 ,   95.345679   ,   29.706821   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   256 ,   95.354778   ,   29.706514   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   257 ,   95.361668   ,   29.705656   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   258 ,   95.362589   ,   29.696844   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   259 ,   95.364695   ,   29.68857    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   260 ,   95.370358   ,   29.681449   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   261 ,   95.376602   ,   29.674505   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   262 ,   95.379236   ,   29.667023   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   263 ,   95.373841   ,   29.660818   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   264 ,   95.36418    ,   29.659099   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   265 ,   95.362493   ,   29.650557   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   266 ,   95.360015   ,   29.642207   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   267 ,   95.355781   ,   29.634521   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   268 ,   95.359486   ,   29.626615   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   269 ,   95.36824    ,   29.629622   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   270 ,   95.376744   ,   29.63252    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   271 ,   95.385821   ,   29.630781   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   272 ,   95.389131   ,   29.622802   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   273 ,   95.392526   ,   29.614933   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   274 ,   95.389189   ,   29.608147   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   275 ,   95.381778   ,   29.602201   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   276 ,   95.375848   ,   29.594968   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   277 ,   95.37422    ,   29.586118   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   278 ,   95.37582    ,   29.577096   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   279 ,   95.37434    ,   29.568279   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   280 ,   95.382187   ,   29.567211   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   281 ,   95.390569   ,   29.56672    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   282 ,   95.394921   ,   29.559154   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   283 ,   95.394212   ,   29.550653   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   284 ,   95.388684   ,   29.544147   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   285 ,   95.378758   ,   29.543307   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   286 ,   95.37117    ,   29.538992   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   287 ,   95.368359   ,   29.53084    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   288 ,   95.372812   ,   29.525023   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   289 ,   95.382642   ,   29.524192   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   290 ,   95.39262    ,   29.52335    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   291 ,   95.40224    ,   29.524993   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   292 ,   95.410643   ,   29.524356   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   293 ,   95.412871   ,   29.516246   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   294 ,   95.416756   ,   29.508542   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   295 ,   95.418974   ,   29.500574   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   296 ,   95.409402   ,   29.49919    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   297 ,   95.404131   ,   29.491812   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   298 ,   95.410453   ,   29.484979   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   299 ,   95.419171   ,   29.481944   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   300 ,   95.427441   ,   29.477986   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   301 ,   95.435538   ,   29.474163   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   302 ,   95.441682   ,   29.468106   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   303 ,   95.436994   ,   29.460836   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   304 ,   95.426906   ,   29.460834   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   305 ,   95.419166   ,   29.455905   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   306 ,   95.414952   ,   29.448276   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   307 ,   95.409165   ,   29.4425 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   308 ,   95.401636   ,   29.436912   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   309 ,   95.400833   ,   29.428901   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   310 ,   95.405038   ,   29.421529   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   311 ,   95.397624   ,   29.416664   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   312 ,   95.388222   ,   29.41503    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   313 ,   95.380556   ,   29.410133   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   314 ,   95.375806   ,   29.402718   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   315 ,   95.374985   ,   29.394234   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   316 ,   95.366267   ,   29.3917 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   317 ,   95.358315   ,   29.386541   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   318 ,   95.354934   ,   29.378565   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   319 ,   95.353307   ,   29.370021   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   320 ,   95.349199   ,   29.362623   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   321 ,   95.342492   ,   29.356101   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   322 ,   95.336182   ,   29.349243   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   323 ,   95.330107   ,   29.341906   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   324 ,   95.322991   ,   29.335815   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   325 ,   95.315651   ,   29.329945   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   326 ,   95.307717   ,   29.32503    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   327 ,   95.298978   ,   29.321646   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   328 ,   95.291774   ,   29.324203   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   329 ,   95.283322   ,   29.328343   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   330 ,   95.277142   ,   29.323522   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   331 ,   95.28003    ,   29.317458   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   332 ,   95.291264   ,   29.312454   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   333 ,   95.288565   ,   29.306327   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   334 ,   95.279687   ,   29.302198   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   335 ,   95.273327   ,   29.294992   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   336 ,   95.266038   ,   29.289128   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   337 ,   95.258023   ,   29.28503    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   338 ,   95.251053   ,   29.279207   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   339 ,   95.241135   ,   29.278365   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   340 ,   95.23324    ,   29.274126   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   341 ,   95.225232   ,   29.269205   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   342 ,   95.21586    ,   29.27157    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   343 ,   95.207875   ,   29.275815   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   344 ,   95.198975   ,   29.274176   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   345 ,   95.197873   ,   29.266166   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   346 ,   95.199399   ,   29.258293   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   347 ,   95.190181   ,   29.255059   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   348 ,   95.180215   ,   29.254924   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   349 ,   95.171669   ,   29.25181    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   350 ,   95.164632   ,   29.246086   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   351 ,   95.158181   ,   29.240045   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   352 ,   95.148746   ,   29.237559   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   353 ,   95.14021    ,   29.235872   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   354 ,   95.13295    ,   29.229681   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   355 ,   95.126422   ,   29.222952   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   356 ,   95.119474   ,   29.216284   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   357 ,   95.112526   ,   29.210003   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   358 ,   95.103186   ,   29.209183   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   359 ,   95.092954   ,   29.21128    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   360 ,   95.089987   ,   29.203182   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   361 ,   95.08918    ,   29.194316   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   362 ,   95.087453   ,   29.185285   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   363 ,   95.07665    ,   29.186648   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   364 ,   95.067753   ,   29.186679   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   365 ,   95.057866   ,   29.185059   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   366 ,   95.049276   ,   29.182527   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   367 ,   95.040023   ,   29.179943   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   368 ,   95.031343   ,   29.177483   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   369 ,   95.022464   ,   29.174754   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   370 ,   95.013879   ,   29.170855   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   371 ,   95.00671    ,   29.17697    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   372 ,   94.997441   ,   29.18004    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   373 ,   94.988276   ,   29.177536   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   374 ,   94.993877   ,   29.16999    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   375 ,   95.0007 ,   29.16334    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   376 ,   95.007289   ,   29.156597   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   377 ,   95.013255   ,   29.149426   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   378 ,   95.014996   ,   29.140501   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   379 ,   95.017665   ,   29.132751   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   380 ,   95.025006   ,   29.125039   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   381 ,   95.015736   ,   29.119104   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   382 ,   95.00527    ,   29.11998    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   383 ,   94.995335   ,   29.120076   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   384 ,   94.987  ,   29.119237   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   385 ,   94.976806   ,   29.119136   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   386 ,   94.967143   ,   29.120031   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   387 ,   94.960855   ,   29.116983   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   388 ,   94.957531   ,   29.108925   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   389 ,   94.952506   ,   29.10209    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   390 ,   94.949162   ,   29.094156   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   391 ,   94.94422    ,   29.086785   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   392 ,   94.938454   ,   29.079704   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   393 ,   94.933062   ,   29.072349   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   394 ,   94.930917   ,   29.063814   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   395 ,   94.928356   ,   29.055856   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   396 ,   94.920828   ,   29.050617   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   397 ,   94.912757   ,   29.047523   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   398 ,   94.902629   ,   29.047491   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   399 ,   94.901768   ,   29.040466   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   400 ,   94.900002   ,   29.03183    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   401 ,   94.896641   ,   29.024201   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   402 ,   94.903407   ,   29.017448   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   403 ,   94.900902   ,   29.009464   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   404 ,   94.899185   ,   29.001063   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   405 ,   94.9047 ,   28.995883   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   406 ,   94.905068   ,   28.98756    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   407 ,   94.89764    ,   28.981664   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   408 ,   94.888037   ,   28.98042    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   409 ,   94.884219   ,   28.972962   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   410 ,   94.88171    ,   28.964265   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   411 ,   94.872589   ,   28.961651   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   412 ,   94.864998   ,   28.956804   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   413 ,   94.857584   ,   28.951665   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   414 ,   94.849279   ,   28.947475   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   415 ,   94.840837   ,   28.943863   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   416 ,   94.830747   ,   28.9433 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   417 ,   94.822379   ,   28.940018   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   418 ,   94.82042    ,   28.932188   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   419 ,   94.815499   ,   28.924971   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   420 ,   94.806049   ,   28.925761   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   421 ,   94.798271   ,   28.930469   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   422 ,   94.788334   ,   28.92995    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   423 ,   94.780365   ,   28.924206   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   424 ,   94.77992    ,   28.914996   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   425 ,   94.778142   ,   28.906684   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   426 ,   94.775821   ,   28.898519   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   427 ,   94.77158    ,   28.8906 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   428 ,   94.770555   ,   28.881648   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   429 ,   94.762036   ,   28.878335   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   430 ,   94.757514   ,   28.869918   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   431 ,   94.769233   ,   28.869979   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   432 ,   94.778921   ,   28.869924   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   433 ,   94.787916   ,   28.86833    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   434 ,   94.795002   ,   28.862491   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   435 ,   94.80081    ,   28.85571    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   436 ,   94.800327   ,   28.846932   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   437 ,   94.792513   ,   28.841285   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   438 ,   94.782327   ,   28.842488   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   439 ,   94.775983   ,   28.835009   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   440 ,   94.773903   ,   28.826474   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   441 ,   94.782853   ,   28.822546   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   442 ,   94.792421   ,   28.821678   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   443 ,   94.79973    ,   28.815827   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   444 ,   94.804976   ,   28.808193   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   445 ,   94.810509   ,   28.801631   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   446 ,   94.816615   ,   28.808176   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   447 ,   94.819182   ,   28.816349   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   448 ,   94.82638    ,   28.821952   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   449 ,   94.835326   ,   28.825776   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   450 ,   94.842739   ,   28.819946   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   451 ,   94.850813   ,   28.815018   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   452 ,   94.860819   ,   28.814183   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   453 ,   94.869968   ,   28.816832   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   454 ,   94.876709   ,   28.823343   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   455 ,   94.884789   ,   28.820776   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   456 ,   94.89341    ,   28.815886   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   457 ,   94.902436   ,   28.814128   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   458 ,   94.909881   ,   28.809973   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   459 ,   94.917508   ,   28.805088   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   460 ,   94.92613    ,   28.800751   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   461 ,   94.930837   ,   28.79353    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   462 ,   94.923537   ,   28.78852    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   463 ,   94.914853   ,   28.785826   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   464 ,   94.908104   ,   28.792316   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   465 ,   94.899271   ,   28.795864   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   466 ,   94.89165    ,   28.790264   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   467 ,   94.885573   ,   28.783509   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   468 ,   94.877886   ,   28.78   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   469 ,   94.867781   ,   28.777486   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   470 ,   94.865077   ,   28.768766   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   471 ,   94.864317   ,   28.76096    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   472 ,   94.868353   ,   28.752912   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   473 ,   94.878941   ,   28.755029   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   474 ,   94.88755    ,   28.75755    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   475 ,   94.895059   ,   28.762457   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   476 ,   94.901936   ,   28.758841   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   477 ,   94.909275   ,   28.752928   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   478 ,   94.91663    ,   28.747886   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   479 ,   94.922562   ,   28.740786   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   480 ,   94.930023   ,   28.735332   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   481 ,   94.939135   ,   28.733116   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   482 ,   94.9475 ,   28.729041   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   483 ,   94.954996   ,   28.72506    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   484 ,   94.961459   ,   28.718291   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   485 ,   94.96826    ,   28.712222   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   486 ,   94.975008   ,   28.705829   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   487 ,   94.981658   ,   28.699644   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   488 ,   94.979719   ,   28.692256   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   489 ,   94.975704   ,   28.68395    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   490 ,   94.975057   ,   28.67656    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   491 ,   94.978529   ,   28.669242   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   492 ,   94.98542    ,   28.668278   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   493 ,   94.988988   ,   28.677418   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   494 ,   94.996867   ,   28.674135   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   495 ,   95.006561   ,   28.67292    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   496 ,   95.01375    ,   28.668417   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   497 ,   95.010812   ,   28.659992   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   498 ,   95.00792    ,   28.652323   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   499 ,   95.013878   ,   28.645291   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   500 ,   95.014475   ,   28.636383   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   501 ,   95.018322   ,   28.628413   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   502 ,   95.026043   ,   28.62229    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   503 ,   95.029919   ,   28.614466   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   504 ,   95.032874   ,   28.606526   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   505 ,   95.036616   ,   28.598579   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   506 ,   95.045148   ,   28.594996   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   507 ,   95.054606   ,   28.593279   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   508 ,   95.063692   ,   28.591237   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   509 ,   95.068571   ,   28.583861   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   510 ,   95.0712 ,   28.575739   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   511 ,   95.073252   ,   28.567398   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   512 ,   95.07708    ,   28.559642   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   513 ,   95.07742    ,   28.550892   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   514 ,   95.07958    ,   28.542434   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   515 ,   95.079083   ,   28.533464   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   516 ,   95.08037    ,   28.524669   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   517 ,   95.079142   ,   28.516002   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   518 ,   95.080836   ,   28.50778    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   519 ,   95.089131   ,   28.503337   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   520 ,   95.097949   ,   28.500804   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   521 ,   95.10125    ,   28.493127   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   522 ,   95.0983 ,   28.485092   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   523 ,   95.093379   ,   28.477473   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   524 ,   95.097875   ,   28.469941   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   525 ,   95.101269   ,   28.462061   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   526 ,   95.099166   ,   28.454278   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   527 ,   95.091642   ,   28.448251   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   528 ,   95.090772   ,   28.439445   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   529 ,   95.087546   ,   28.431501   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   530 ,   95.081641   ,   28.424218   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   531 ,   95.073362   ,   28.419992   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   532 ,   95.06659    ,   28.413262   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   533 ,   95.072444   ,   28.40648    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   534 ,   95.077445   ,   28.39897    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   535 ,   95.07666    ,   28.390463   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   536 ,   95.074089   ,   28.382368   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   537 ,   95.070898   ,   28.374287   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   538 ,   95.070808   ,   28.365422   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   539 ,   95.065771   ,   28.358395   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   540 ,   95.058262   ,   28.352516   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   541 ,   95.048531   ,   28.351624   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   542 ,   95.039373   ,   28.34999    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   543 ,   95.032467   ,   28.343949   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   544 ,   95.030005   ,   28.336065   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   545 ,   95.026376   ,   28.326662   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   546 ,   95.020276   ,   28.330787   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   547 ,   95.014649   ,   28.341737   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   548 ,   95.006417   ,   28.34582    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   549 ,   94.996674   ,   28.344654   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   550 ,   94.992479   ,   28.337272   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   551 ,   94.995065   ,   28.329203   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   552 ,   94.999186   ,   28.321824   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   553 ,   94.993693   ,   28.315078   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   554 ,   94.984924   ,   28.31163    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   555 ,   94.974833   ,   28.314183   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   556 ,   94.96619    ,   28.314146   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   557 ,   94.958334   ,   28.310398   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   558 ,   94.95247    ,   28.304881   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   559 ,   94.950801   ,   28.2962 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   560 ,   94.950041   ,   28.287349   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   561 ,   94.956638   ,   28.280786   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   562 ,   94.965802   ,   28.278364   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   563 ,   94.973478   ,   28.28662    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   564 ,   94.979879   ,   28.28665    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   565 ,   94.982245   ,   28.278289   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   566 ,   94.98625    ,   28.270808   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   567 ,   94.98708    ,   28.26206    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   568 ,   94.988357   ,   28.25352    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   569 ,   94.988713   ,   28.244549   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   570 ,   94.995499   ,   28.2383 ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   571 ,   95.003509   ,   28.23411    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   572 ,   95.00625    ,   28.226102   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   573 ,   95.007522   ,   28.217603   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   574 ,   95.00875    ,   28.208891   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   575 ,   95.007419   ,   28.200163   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   576 ,   95.010667   ,   28.192463   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   577 ,   95.020831   ,   28.192431   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   578 ,   95.02708    ,   28.186907   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   579 ,   95.030229   ,   28.178939   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   580 ,   95.036617   ,   28.171767   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   581 ,   95.044153   ,   28.166863   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   582 ,   95.051174   ,   28.160823   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   583 ,   95.05916    ,   28.155584   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   584 ,   95.068268   ,   28.153256   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   585 ,   95.077192   ,   28.150787   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   586 ,   95.085829   ,   28.147545   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   587 ,   95.094693   ,   28.144991   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   588 ,   95.102471   ,   28.140978   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   589 ,   95.110725   ,   28.136606   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   590 ,   95.120296   ,   28.134926   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   591 ,   95.130097   ,   28.134084   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   592 ,   95.139549   ,   28.136159   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   593 ,   95.145083   ,   28.143347   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   594 ,   95.153574   ,   28.146682   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   595 ,   95.161647   ,   28.150739   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   596 ,   95.17093    ,   28.152481   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   597 ,   95.179149   ,   28.156536   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   598 ,   95.186607   ,   28.162033   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   599 ,   95.196612   ,   28.162426   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   600 ,   95.200982   ,   28.167541   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   601 ,   95.204057   ,   28.175027   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   602 ,   95.212903   ,   28.176575   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   603 ,   95.216146   ,   28.170471   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   604 ,   95.223175   ,   28.16421    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   605 ,   95.232262   ,   28.16708    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   606 ,   95.242037   ,   28.16752    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   607 ,   95.24875    ,   28.163901   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   608 ,   95.254032   ,   28.156656   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   609 ,   95.263112   ,   28.154166   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   610 ,   95.271026   ,   28.149956   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   611 ,   95.27955    ,   28.146618   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   612 ,   95.286787   ,   28.140644   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   613 ,   95.29208    ,   28.133405   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   614 ,   95.29375    ,   28.124938   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   615 ,   95.288557   ,   28.11846    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   616 ,   95.28245    ,   28.113315   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   617 ,   95.282601   ,   28.10428    ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   618 ,   95.291528   ,   28.101667   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   619 ,   95.301539   ,   28.100832   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   620 ,   95.311297   ,   28.099217   ,   0   ,   226800  ,  660])
    rundata.gaugedata.gauges.append([   621 ,   95.321755   ,   28.096932   ,   0   ,   226800  ,  660])





    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")

##### coordinate_system = 1 for Cartesian x-y in meters, coordinate_system = 2 for latitude-longitude on the sphere

    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.04
    geo_data.friction_depth = 20.0

    # Refinement data
    refinement_data = rundata.refinement_data
    refinement_data.wave_tolerance = 1.e-2
    refinement_data.deep_depth = 1e2
    refinement_data.max_level_deep = 3
    refinement_data.variable_dt_refinement_ratios = True

    # == settopo.data values == this has some new stuff, check setrun.py from chile2010 example
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fname]
    topo_data.topofiles.append([3, 1, 5, 0., 1.e10, 'mega_fill.txt']) #new format 5.6

    # == setdtopo.data values ==
    dtopo_data = rundata.dtopo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]

##### 0 = No perturbation specified, 1 = Perturbation to depth h, 4 = Perturbation to surface level

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == setfixedgrids.data values ==
    fixedgrids = rundata.fixed_grid_data.fixedgrids
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # == fgmax.data values ==
    fgmax_files = rundata.fgmax_data.fgmax_files
    # for fixed grids append to this list names of any fgmax input files
    rundata.fgmax_data.num_fgmax_val = 5
    # Grid
    #fgmax_files.append('fgmax1.txt')
    fgmax_files.append('fgmax_mega_20190611.txt')     
    # Profile
    #fgmax_files.append('fgmax2.txt')
    

    return rundata 
    # end of function setgeo
    # ----------------------



if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()

