[Mesh]
  type = GeneratedMesh
  dim = 1
  nx = 1
[]

[Problem]
  type = FEProblem
  solve = false
[]

[Executioner]
  type = Steady
[]

[MultiApps]
  [openmc]
    type = FullSolveMultiApp
    app_type = OpenMCApp
    input_files = "transfer_sub.i"
    library_path = ../openmc/lib
  []
[]

[Transfers]
  [./to_openmc]
    type = MoabMeshTransfer
    direction = to_multiapp
    multi_app = openmc
    moabname = "moab"
    apptype_from="AuroraApp"
  [../]
[]

[Outputs]
  console=false
[]
