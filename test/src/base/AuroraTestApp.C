//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html
#include "AuroraTestApp.h"
#include "AuroraApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "MooseSyntax.h"
#include "ModulesApp.h"

InputParameters
AuroraTestApp::validParams()
{
  InputParameters params = AuroraApp::validParams();
  return params;
}

AuroraTestApp::AuroraTestApp(InputParameters parameters) : MooseApp(parameters)
{
  AuroraTestApp::registerAll(
      _factory, _action_factory, _syntax, getParam<bool>("allow_test_objects"));
}

AuroraTestApp::~AuroraTestApp() {}

void
AuroraTestApp::registerAll(Factory & f, ActionFactory & af, Syntax & s, bool use_test_objs)
{
  AuroraApp::registerAll(f, af, s);
  if (use_test_objs)
  {
    Registry::registerObjectsTo(f, {"AuroraTestApp"});
    Registry::registerActionsTo(af, {"AuroraTestApp"});
  }
}

void
AuroraTestApp::registerApps()
{
  registerApp(AuroraApp);
  registerApp(AuroraTestApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
// External entry point for dynamic application loading
extern "C" void
AuroraTestApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  AuroraTestApp::registerAll(f, af, s);
}
extern "C" void
AuroraTestApp__registerApps()
{
  AuroraTestApp::registerApps();
}
