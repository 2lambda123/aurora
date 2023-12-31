#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import numpy
import os.path

class PlotData():
    def __init__(self):
        self.title = ""
        self.x_label = ""
        self.y_label = ""
        self.markers = []
        self.colours = []
        self.dataset_name=""
        self.cmpdataset_name=""
        self.labels=[]
        self.cmplabels=[]
        self.all_datasets=[]
        self.all_cmpdatasets=[]
        self.xdata=[]
        self.outext=".png"
        self.runtype=""
        self.outstem=""
        self.ylim=[]

class RunInfo():
    def __init__(self):
        self.filebase=""
        self.comparefilebase=""
        self.ext=".csv"
        self.procs=[]
        self.parts=[]
        self.threads=[]
        self.nthreads=1
        self.dataset_label="MOOSE"
        self.cmpdataset_label="OpenMC"

def getPlotData(info):
    plotdata=PlotData()
    plotdata.xdata=info.parts
    plotdata.x_label="# Particles"
    plotdata.y_label="Time / s"
    plotdata.markers=["^","o","s","d","p"]
    plotdata.colours=["red","green","blue", "orange","purple"]

    for nmpi in info.procs:

        for nthreads in info.threads:

            # Dictionaries to store the data for different numbers of processes/threads
            datasets={}
            cmpdatasets={}

            # Loop over runs with different numbers of particles
            for np in info.parts:
                append_datasets_from_file(info.filebase,np,nmpi,nthreads,info.ext,datasets)
                append_datasets_from_file(info.comparefilebase,np,nmpi,nthreads,info.ext,cmpdatasets)

            # Create legend lables
            labelbase="# MPI = "+str(nmpi)+" # threads = "+str(nthreads)
            label=labelbase+" ("+info.dataset_label+")"
            cmplabel=labelbase+" ("+info.cmpdataset_label+")"

            # Save all the data
            if len(datasets)!=0 :
                plotdata.labels.append(label)
                plotdata.all_datasets.append(datasets)

            if len(cmpdatasets)!=0 :
                plotdata.cmplabels.append(cmplabel)
                plotdata.all_cmpdatasets.append(cmpdatasets)

    return plotdata

def makePlot(plotdata):
    # Create a new plot
    fig = plt.figure(tight_layout=True)
    gs = gridspec.GridSpec(1,1)

    #fig, axs = plt.subplots(1, 2, constrained_layout=True)
    ax=fig.add_subplot(gs[0])
    ax.set_xlabel(plotdata.x_label)
    ax.set_ylabel(plotdata.y_label)
    ax.set_xscale("log")
    ax.set_yscale("log")

    #ax2=fig.add_subplot(gs[1])
    #ax2.set_xlabel(x_label)
    #ax2.set_ylabel(y_label)
    #ax2.set_xscale("log")
    #ax2.set_yscale("log")

    nsets = len(plotdata.all_datasets)
    for iset in range(nsets):
        data=plotdata.all_datasets[iset][plotdata.dataset_name][0]
        errs=plotdata.all_datasets[iset][plotdata.dataset_name][1]
        ax.errorbar(plotdata.xdata,data,yerr=errs,c=plotdata.colours[iset],marker=plotdata.markers[iset],label=plotdata.labels[iset])

        cmpdata=plotdata.all_cmpdatasets[iset][plotdata.cmpdataset_name][0]
        cmperrs=plotdata.all_cmpdatasets[iset][plotdata.cmpdataset_name][1]
        ax.errorbar(plotdata.xdata,cmpdata,yerr=cmperrs,c=plotdata.colours[iset],mec=plotdata.colours[iset],mfc='none',marker=plotdata.markers[iset],label=plotdata.cmplabels[iset],ls="--")

    if(len(plotdata.ylim) == 2):
        ax.set_ylim(plotdata.ylim[0],plotdata.ylim[1])

    ax.legend(loc='upper left')
    #ax2.legend(loc='upper left')
    fig.suptitle(plotdata.title)

    # Specify outfile name
    outfile=plotdata.outstem
    if plotdata.runtype != "":
        outfile+="_"+plotdata.runtype
    outfile+=plotdata.outext

    # Save
    print("Plotting",outfile)
    plt.savefig(outfile)


def get_csv_data(filename):
    timers={}
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            line = f.readline()
            line = line.rstrip()
            timer_keys = line.split(",")

            ntimes=len(timer_keys)
            all_times=[]
            for i in range(ntimes):
                all_times.append([])

            while True:
                line = f.readline()
                line = line.rstrip()
                if line == "":
                    break

                times=line.split(",")
                if len(times) != ntimes:
                    print("datasets have different lengths")
                    sys.exit()

                for i in range(ntimes):
                    time = times[i]
                    all_times[i].append(time)

        timers=dict(zip(timer_keys,all_times))
    return timers

def append_datasets(timers,datasets):
    for key,times in timers.items():
        #Strip quotes
        key=key.strip("\"")
        if key=="":
            continue
        if not key in datasets :
            datasets[key]=[[],[]]

        ntimes=len(times)
        sumtime=0.
        sumsqrs=0.
        for time in times:
            val = float(time)
            sumtime += val
            sumsqrs += val*val
        sumtime /= float(ntimes)
        sumsqrs /= float(ntimes)
        var = sumsqrs-sumtime*sumtime
        err = numpy.sqrt(var)

        datasets[key][0].append(sumtime)
        datasets[key][1].append(err)

def append_datasets_from_file(filebase,np,nmpi,nthreads,ext,datasets):
    # Define csv filename
    filename=filebase+"_np"+str(np)+"_nmpi"+str(nmpi)+"_nt"+str(nthreads)+ext
    # Extract data from file
    timers=get_csv_data(filename)
    # Store timings against their keys
    append_datasets(timers,datasets)
