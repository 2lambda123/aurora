[Mesh]
  type = FileMesh
  file = copper_air_tetmesh.e
[]

[Problem]
  type = OpenMCProblem
[]

[Executioner]
  type = OpenMCExecutioner
  variables = 'heating-local flux'
  score_names = 'heating-local flux'
  tally_ids = '1 1'
  err_variables = 'heating-local-err flux-err'
  launch_threads=true
  n_threads=4
[]

[AuxVariables]
  [heating-local]
      order = CONSTANT
      family = MONOMIAL
  []
  [heating-local-err]
      order = CONSTANT
      family = MONOMIAL
  []
  [flux]
      order = CONSTANT
      family = MONOMIAL
  []
  [flux-err]
      order = CONSTANT
      family = MONOMIAL
  []
[]

[UserObjects]
  [moab]
    type = MoabUserObject
  []
[]

[Outputs]
  exodus = true
  execute_on = "final"
[]
