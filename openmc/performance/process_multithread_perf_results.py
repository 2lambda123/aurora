#!/usr/bin/env python3

from makeplots import *

# Specify run parameters
info=RunInfo();

# Patterns for data files
info.filebase="perf_test-opt"
info.comparefilebase="openmc_perf_test"

# Run specifications
info.procs=[1]
info.threads=[1,2,4]
info.parts=[100,1000,10000]

# Get the data from file
plotdata=getPlotData(info)

# Add specific plot specifications
plotdata.title="Average time spent in OpenMCExecutioner::run vs. openmc_run"
plotdata.dataset_name="executioner_run_time"
plotdata.cmpdataset_name="simulation"
plotdata.outstem=plotdata.dataset_name
plotdata.runtype="multithreaded"

# Make plot
makePlot(plotdata)

plotdata.title="Average total application run time"
plotdata.dataset_name="main_total_time"
plotdata.cmpdataset_name="total"
plotdata.outstem="total_runtime"

# Make plot
makePlot(plotdata)
