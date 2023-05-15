[Mesh]
 [filemesh]
    type = FileMeshGenerator
    file = copper_air_bcs_tetmesh.e
    show_info = true
  []
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
  launch_threads=false
[]
  
[UserObjects]
  [dag_reflecting]
    type =  DagSurfaceUserObject
    boundary_type = Reflecting
    boundary_names = 'left right'
  []
  [dag_graveyard]
    type =  DagSurfaceUserObject
    boundary_type = Graveyard
    boundary_names = 'top-outer bottom-outer left-outer right-outer front-outer back-outer'
  []
  [moab]
    type = MoabUserObject
    length_scale = 1.0
    dag_surface_names = 'dag_reflecting dag_graveyard'
  []
[]