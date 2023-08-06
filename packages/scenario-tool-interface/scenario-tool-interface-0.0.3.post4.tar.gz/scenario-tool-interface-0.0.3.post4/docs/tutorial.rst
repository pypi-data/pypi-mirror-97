==========
Quickstart
==========

The aim of the tutorial is to get you started using the Scenario-Tool as quickly as possible. At the end you will be able to

 - Login
 - Create a new project
 - Setup a simple workflow
 - Run queries to analyse the results
 - Analyse the results with pandas

Project Setup
=============


Getting your login token
------------------------


.. code-block::

    from scenario_tool_interface import ScenarioToolInterface
    sti = ScenarioToolInterface()
    # Login with your username and password
    sti.login("username", "password")


Setup project and run baseline
------------------------------

A project provides the shell for the your scenarios.

To setup the city database the project region eg. Melbourne and the case study boundary need to be defined.
Further for each model the performance assessment model may be defined.

.. code-block::


    # Create a new project
    project_id = sti.create_project()

    # Obtain region code
    region_id = sti.get_region("melbourne")

    # Load geoson file
    with open("../resources/test.geojson", 'r') as file:
             geojson_file = json.loads(file.read())

    # Upload boundary
    geojson_id = sti.upload_geojson(geojson_file, project_id)

    # Set project parameters
    sti.update_project(project_id, {
        "name": "my project",
        "active": True,
        'region_id': region_id,
        "case_study_area_id": geojson_id,
    })

    # Setup data model
    sti.set_project_data_model(project_id, {"data_model_id": 1, "parameters":
                                            {"micro_climate_grid.grid_size": "20",
                                             "district.source": 1,
                                             "district.layer_name":
                                             "sa1_2011_aust",
                                             "district.epsg_from": "4283",
                                             "parcel.source": 2,
                                             "parcel.layer_name": "property_vic",
                                             "parcel.epsg_from": "4283",
                                             "landcover_geoscape.raster_file": 3
                                            }})

    # Add assessment models
    lst_model = sti.get_assessment_model("Land Surface Temperature")

    # Set assessment models
    sti.set_project_assessment_models(project_id, [{"assessment_model_id": lst_model}])


    # Create and run baseline
    baseline_id = sti.create_scenario(token, project_id, None)
    sti.execute_scenario(baseline_id)

    # Scenarios are executed asynchronous.
    while True:
         # A status code smaller than 7 means the simulation is still executed.
         r = sti.check_status(baseline_id)
         status = r["status"]
         if status > 6:
            break
         time.sleep(1)


Create Scenario
---------------

After initialising the base model the model is ready to explore different scenarios. Scenarios
are defined as a workflow of nodes. The nodes range from sub dividing a green field development
or adding trees. To show a list of a available nodes use:


.. code-block::

    # Print a list of available nodes
    sti.show_nodes()

    # Nodes are defined as below
    residential_node = {
        "node_type_id": sti.get_node_id("Residential"),
        "area": geojson_id,
        "parameters":
            {
                "dance4water_building.site_coverage": 0.6,
                "dance4water_number_of_trees.equation": 1,
                "dance4water_tree_spacing.equation": 22
            }
    }

    nodes = []
    # Several nodes can are combined to a workflow be adding them to a vector. The
    # nodes are executed in the order the are added
    nodes.append(residential_node)

    # Scenarios need a parent. In this case we use the base line scenario created before
    baseline_scenario_id = sti.get_baseline(project_id)

    # Crate a new scenario
    scenario_id = sti.create_scenario(project_id, baseline_scenario_id, "my new scenario")

    # Set workflow
    sti.set_scenario_workflow(scenario_id, nodes)

    # Execute scenario
    sti.execute_scenario(scenario_id)

    # Scenarios are executed asynchronous
    while True:
        # A status code smaller than 7 means the simulation is still executed.
        r = sti.check_status(scenario_id)
        status = r["status"]
        if status > 6:
            break
        time.sleep(1)


Analysis
--------

This section will show how the results of the before created base line and scenario can be analysed


.. code-block::

   # Before running an analysis check if the scenarios have been executed
   # The scenario of interest should start return a 7 as simulation status which indicate the performance
   # assessment model has been successfully executed
   sti.show_scenarios(project_id)

   # The results can be obtained buy running SQL queries on the result database
   # Queries are executed asynchronous. We execute wait therefore until the return status has
   # changed to loaded

    while True:
        r = sti.run_query(scenario_id,
                          "SELECT avg(tree_cover_fraction) as tf from micro_climate_grid")

        if r['status'] != 'loaded':
           # Break the loop when query is loaded
           break
    print(r['data'])
