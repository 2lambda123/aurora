###############################################################################
################### MOOSE Application Standard Makefile #######################
###############################################################################
#
# Required Environment variables (one of the following)
# PACKAGES_DIR  - Location of the MOOSE redistributable package
#
# Optional Environment variables
# MOOSE_DIR     - Root directory of the MOOSE project
# FRAMEWORK_DIR - Location of the MOOSE framework
#
###############################################################################
# Use the MOOSE submodule if it exists and MOOSE_DIR is not set
MOOSE_SUBMODULE    := $(CURDIR)/../moose
ifneq ($(wildcard $(MOOSE_SUBMODULE)/framework/Makefile),)
  MOOSE_DIR        ?= $(MOOSE_SUBMODULE)
else
  MOOSE_DIR        ?= $(shell dirname `pwd`)/../moose
endif
FRAMEWORK_DIR      ?= $(MOOSE_DIR)/framework
###############################################################################

# framework
include $(FRAMEWORK_DIR)/build.mk
include $(FRAMEWORK_DIR)/moose.mk

################################## MODULES ####################################
# set desired physics modules equal to 'yes' to enable them
CHEMICAL_REACTIONS        := no
CONTACT                   := no
FLUID_PROPERTIES          := no
HEAT_CONDUCTION           := yes
MISC                      := no
NAVIER_STOKES             := no
PHASE_FIELD               := no
RDG                       := no
RICHARDS                  := no
SOLID_MECHANICS           := no
STOCHASTIC_TOOLS          := no
TENSOR_MECHANICS          := yes
XFEM                      := no
POROUS_FLOW               := no
LEVEL_SET                 := no
include           $(MOOSE_DIR)/modules/modules.mk
###############################################################################

# Extra stuff for GTEST
ADDITIONAL_INCLUDES := -I$(FRAMEWORK_DIR)/contrib/gtest
ADDITIONAL_LIBS     := $(FRAMEWORK_DIR)/contrib/gtest/libgtest.la

# dep apps
CURRENT_DIR        := $(shell pwd)
APPLICATION_DIR    := $(CURRENT_DIR)/..
APPLICATION_NAME   := aurora
include            $(FRAMEWORK_DIR)/app.mk

APPLICATION_DIR    := $(CURRENT_DIR)
APPLICATION_NAME   := aurora-unit
BUILD_EXEC         := yes

DEP_APPS    ?= $(shell $(FRAMEWORK_DIR)/scripts/find_dep_apps.py $(APPLICATION_NAME))

# Link OpenMC standalone app
OPENMC_APP_NAME = open_mc
OPENMC_APP_LIB_NAME = $(OPENMC_APP_NAME)-$(METHOD)
OPENMC_APP_DIR = $(CURRENT_DIR)/../openmc
OPENMC_APP_INC = -I$(OPENMC_APP_DIR)/include
OPENMC_APP_LIB = -Wl,-rpath,$(OPENMC_APP_DIR)/lib -L$(OPENMC_APP_DIR)/lib -l$(OPENMC_APP_LIB_NAME)


# Link OpenMC App tests
OPENMC_TEST_DIR = $(OPENMC_APP_DIR)/unit/
OPENMC_TEST_INC = -I$(OPENMC_TEST_DIR)/include
OPENMC_TEST_LIB_NAME = $(OPENMC_APP_NAME)-unit-$(METHOD)
OPENMC_APP_LIB = -Wl,-rpath,$(OPENMC_TEST_DIR)/lib -L$(OPENMC_TEST_DIR)/lib -l$(OPENMC_TEST_LIB_NAME)

include $(OPENMC_APP_DIR)/config.inc

ADDITIONAL_INCLUDES += $(OPENMC_TEST_INC) $(OPENMC_APP_INC) $(OPENMC_INC) $(MOAB_INC) $(HDF5_INC)
ADDITIONAL_LIBS += $(OPENMC_TEST_LIB) $(OPENMC_APP_LIB) $(OPENMC_LIB) $(MOAB_LIB)

include $(FRAMEWORK_DIR)/app.mk

# Find all the Aurora unit test source files and include their dependencies.
aurora_unit_srcfiles := $(shell find $(CURRENT_DIR)/src -name "*.C")
aurora_unit_deps := $(patsubst %.C, %.$(obj-suffix).d, $(aurora_unit_srcfiles))
-include $(aurora_unit_deps)

###############################################################################
# Additional special case targets should be added here
