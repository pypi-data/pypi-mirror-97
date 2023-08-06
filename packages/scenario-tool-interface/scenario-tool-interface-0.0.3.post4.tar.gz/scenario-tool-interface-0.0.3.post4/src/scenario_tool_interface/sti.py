#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import enum


class AccessLevel(enum.Enum):
    DEMO = 1
    PARTICIPANT = 2
    CONSULTANT = 3
    ADMIN = 4
    SUPERADMIN = 5


class ScenarioToolInterface:

    def __init__(self, api_url="https://stable-api.dance4water.org/api",
                 results_url="https://stable-sql.dance4water.org/resultsdb/"):
        self.api_url = api_url
        self.results_url = results_url

        self.authenticated = False
        self.token = None
        self._cache = {}

    def login(self, username: str, password: str):
        """
        :param username: registered user name (email address)
        :param password: top secret password
        """
        counter = 0
        while True:
            r = requests.post(self.api_url + "/user/login/", json={'username': username,
                                                                   'password': password})
            counter += 1
            if r.status_code == 200:
                self.token = r.json()["access_token"]
                self.authenticated = True
                return
            if counter > 4:
                raise Exception(f"Unable to login status {r.status_code}")

            else:
                time.sleep(2)

    def _get(self, url):

        if not self.authenticated or self.token is None:
            raise Exception(f"User not authenticated, GET FAILED, {url}")

        headers = {"Authorization": "Bearer " + self.token}
        return requests.get(url, headers=headers)

    def _put(self, url, data={}):

        if not self.authenticated or self.token is None:
            raise Exception(f"User not authenticated, PUT FAILED, {url}")

        headers = {"Authorization": "Bearer " + self.token}
        return requests.put(url, json=data, headers=headers)

    def _post(self, url, data={}):

        if not self.authenticated or self.token is None:
            raise Exception(f"User not authenticated, {url}")

        headers = {"Authorization": "Bearer " + self.token}
        return requests.post(url, json=data, headers=headers)

    def db_name(self, simulation_id):
        return simulation_id

    def run_query(self, scenario_id, query):
        """
        Run a query on the scenario spatialite database. The database supports SQLite and Spatialite commands
        Only read access is supported! To find out which data are stored in the database read the dynamind_table_definitions

        :param scenario_id: scenario id
        :param query: SQL query
        :type scenario_id: int
        :type query str
        :return: query result
        :rtype: dict
        """

        simulation_id = self.get_database_id(scenario_id)

        data = {'db_name': self.db_name(simulation_id),
                'query': query}
        r = requests.post(self.results_url, data=data)
        if r.status_code == 200:
            result = r.json()
            return result
        raise Exception(f"Unable to run query {r.status_code}")

    def add_node(self, node_data):
        return self._post(self.api_url + "/sm_node", node_data)

    def update_sm_node(self, node_id, node_data):
        return self._post(self.api_url + "/sm_node/" + str(node_id) + "/versions", node_data)

    def add_model(self, name, src):
        return self._post(self.api_url + "/models", {"name": name, "model_src": src})

    def get_models(self):
        return self._get(self.api_url + "/models/")

    def get_database_id(self, scenario_id):
        """
        Returns database ID to run data analysis

        :param scenario_1_id: scenario id
        :return: data base id needed for query
        """
        cache_key = f"get_database_id{scenario_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        r = self.get_simulations(scenario_id)
        if r.status_code != 200:
            raise Exception(f"Unable to obtain scenarios {r.status_code}, {r.json()}")

        sims = r.json()

        for s in sims["simulations"]:
            sim = json.loads(s)
            if sim["simulation_type"] == "PERFORMANCE_ASSESSMENT":
                self._cache = sim["id"]
                return self._cache[cache_key]


    def create_project(self):
        """
        Creates a new project

        :return: project id
        :rtype: int
        """

        r = self._post(self.api_url + "/projects")

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Creation of project failed {r.status_code}")

    def get_project(self, project):
        return self._get(self.api_url + "/projects/" + str(project))

    def get_projects(self):
        return self._get(self.api_url + "/projects/")

    def update_project(self, project, data):
        r = self._put(self.api_url + "/projects/" + str(project), data)

        if r.status_code == 200:
            return

        raise Exception(f"Updating project failed {r.status_code}, {r.json()}")

    def get_assessment_models(self):
        r = self._get(self.api_url + "/assessment_models/")

        if r.status_code == 200:
            return r.json()
        raise Exception(f"Failed to get performance assessment model {r.status_code}, {r.json()}")

    def get_assessment_model(self, model_name, owner_id=None):
        """
        Returns assessment model id

        :param model_name: Model Name. Currently supported are Land Surface Temperature and Target
        :param owner_id: If owner_id is set only models owned by the user will be returned
        :type model_name: str
        :type owner_id: int
        :return: model_id
        :rtype: int
        """
        r = self.get_assessment_models()

        models = r["assessment_models"]
        filtered_nodes = []
        for model in models:
            if model['name'] == model_name:
                if owner_id and model['creator'] == owner_id:
                    filtered_nodes.append(model)
                elif not owner_id:
                    filtered_nodes.append(model)
        if len(filtered_nodes) == 0:
            raise Exception(f"Performance assessment model {model_name} not found")

        if len(filtered_nodes) == 1:
            return filtered_nodes[0]["id"]

        # if multiple performance assessment models have been found return the one the user owns
        for n in filtered_nodes:
            if n["creator"] == self.get_my_status()["user_id"]:
                return n["id"]

        return filtered_nodes[0]["id"]

    def set_project_assessment_models(self, project, models):
        r = self._put(self.api_url + "/projects/" + str(project) + "/models", models)
        if not r.status_code == 200:
            raise Exception(f"Unable to set assessment model {r.status_code}, {r.json()}")

    def set_project_data_model(self, project, model):
        r = self._post(self.api_url + "/projects/" + str(project) + "/data_model", model)
        if not r.status_code == 200:
            raise Exception(f"Unable to set project data model {r.status_code}, {r.json()}")


    def share_project(self, project, username):
        """
        Share a project

        :param project: project id
        :param username: share user name
        """

        data = {"username": username}

        r = self._post(self.api_url + "/projects/" + str(project) + "/share", data)

        if r.status_code == 200:
            return

        raise Exception(f"Unable to share project {r.status_code}, {r.json()}")

    def archive_project(self, project):
        """
        Share a project

        :param project: project id
        :param username: share user name
        """

        data = {}

        r = self._post(self.api_url + "/projects/" + str(project) + "/archive", data)

        if r.status_code == 200:
            return

        raise Exception(f"Unable to archive project {r.status_code}")


    def create_scenario(self, project, parent, name="Baseline"):
        """
        Creates a new scenario. The provides the shell for the new scenarios. Scenario are derived from the base line
        or any other scenario in the project. To modify the environment workflow may be defined and executed.

        :param project: project id
        :param parent: parent scenario id
        :param name: name of scenario
        :type int
        :type int
        :type str
        :return: scenario id
        :rtype: int
        """

        data = {"project_id": project, "name": name}
        if parent is not None:
            data["parent"] = parent

        r = self._post(self.api_url  + "/scenario/", data)

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to create scenario {r.status_code}, {r.json()}")

    def set_scenario_workflow(self, scenario_id, node_data):
        """
        Set the workflow for a scenario. The workflow is defined by a series of nodes defined by the node_data
        The node_data have following structure

        .. code-block::

            [{
               name: node_id,
               area: geojson_id,
               parameters: {

                parameter.value = 1,
                paramter2.value = 2,

               }
            },
            ...
            ]

        The nodes in the workflow are executed as defined in the data structure

        :param scenario_id: scenario id
        :param node_data: node data see above
        :type scenario_id: int
        :type node_data: list

        """
        r = self._post(self.api_url + "/scenario/" + str(scenario_id) + "/nodes", node_data)
        if r.status_code == 200:
            return

        raise Exception(f"Something went wrong when adding the nodes {r.status_code} {r.json()}")

    def get_scenario_workflow_nodes(self, scenario_id=None):
        if scenario_id is None:
            return self._get(self.api_url + "/sm_node/")
        return self._get(self.api_url + "/scenario/" + str(scenario_id) + "/nodes")

    def create_dash_tile_template(self, json):
        """
        Define tile template (see doc)

        :param json:
        :return: dash_tile_template_id
        :rtype: int
        """

        r = self._post(self.api_url + "/dash_tile_template/", {"json": json})

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to create template {r.status_code}")

    def edit_dash_tile_template(self, template_id, json=None, active=True):
        """
        Define tile template (see doc)

        :param json:
        :return: dash_tile_template_id
        :rtype: int
        """
        data = {}
        if json:
            data["json"] = json
        data["active"] = active

        r = self._post(self.api_url + "/dash_tile_template/" + str(template_id), data)

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to create template {r.status_code}")

    def create_query_template(self, json, access_level):
        """
        Define tile template (see doc)

        :param json:
        :param access_level
        :type geojson: str
        :type access_level: int
        :return: query_template_id
        :rtype: int
        """

        r = self._post(self.api_url + "/query_prototypes/", {"json": json, "access_level": access_level})

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to create template {r.status_code}")

    def link_dash_tile_assessment_model(self, dash_tile_template_id, assessment_model_id):
        """
        Link dash tile with assessment model

        :param dash_tile_template_id:
        :param assessment_model_id:
        :type dash_tile_template_id: int
        :type assessment_model_id: int
        :return: None
        """

        r = self._post(self.api_url + "/dash_tile_template_assessment_model/",
                       {"dash_tile_template_id": dash_tile_template_id,
                        "assessment_model_id": assessment_model_id})
        if r.status_code == 200:
            return

        raise Exception(f"Unable to link template {r.status_code}")

    def link_query_prototype_assessment_model(self, query_prototype_id, assessment_model_id):
        """
        Link query prototype with assessment model

        :param query_prototype_id:
        :param assessment_model_id:
        :type query_prototype_id: int
        :type assessment_model_id: int
        :return: None
        """

        r = self._post(self.api_url + "/query_template_assessment_model/",
                       {"query_prototype_id": query_prototype_id,
                        "assessment_model_id": assessment_model_id})
        if r.status_code == 200:
            return

        raise Exception(f"Unable to link template {r.status_code}")

    def link_dash_tile_query_prototype(self, dash_tile_template_id , query_prototype_id):
        """
        Link query prototype with assessment model

        :param dash_tile_template_id:
        :param query_prototype_id:
        :type dash_tile_template_id: int
        :type query_prototype_id: int
        :return: None
        """

        r = self._post(self.api_url + "/dash_tile_template_query_prototype/",
                       {"dash_tile_template_id": dash_tile_template_id,
                        "query_prototype_id": query_prototype_id})
        if r.status_code == 200:
            return

        raise Exception(f"Unable to link template {r.status_code}")

    def upload_geojson(self, geojson, project_id, name="casestudyarea"):
        """
        Upload a geojson file and return id

        :param geojson: geojson file
        :param project_id: project the node will be assigned to
        :param name: added option to set name of geojson file default is set to casestudyarea
        :type geojson: str
        :type name: str
        :type project_id: int
        :return: geojson id
        :rtype: int
        """

        if 'name' in geojson:
            del geojson['name']
        r = self._post(self.api_url + "/geojson/", {"project_id": project_id, "geojson": geojson, "name": name})

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to upload file {r.status_code}, {r.json()}")

    def create_datasource(self,  project_id, name, source_type="file", upload_id=None):
        """
        Upload a geojson file and return id

        :param geojson: geojson file
        :param project_id: project the node will be assigned to
        :param name: added option to set name of geojson file default is set to casestudyarea
        :type geojson: str
        :type name: str
        :type project_id: int
        :return: geojson id
        :rtype: int
        """

        r = self._post(self.api_url + "/data_source/",
                       {"project_id": project_id,
                        "source_type": source_type,
                        "upload_id": upload_id,
                        "name": name})

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to create datasource {r.status_code}, {r.json()}")

    def upload_file(self, project_id, file):
        """
        Upload a  file and return id

        :param file: path to file
        :param project_id: project the file will be assigned to
        :type file: str
        :type name: str
        :type project_id: int
        :rtype: int
        """

        if not self.authenticated or self.token is None:
            raise Exception(f"User not authenticated, {url}")

        headers = {"Authorization": "Bearer " + self.token}

        files = {'file': open(file, 'rb')}
        r = requests.post(self.api_url + f"/upload/{project_id}", headers=headers, files=files)

        if r.status_code == 200:
            return r.json()["id"]

        raise Exception(f"Unable to upload file {r.status_code}, {r.json()}")


    def get_region(self, region_name: str) -> int:
        """
        Returns region currently supported is Melbourne

        :param region_name: region id
        :return: region id
        """

        r = self._get(self.api_url + "/regions/")
        if not r.status_code == 200:
            raise Exception(f"Unable to get region {r.status_code}, {r.json()}")
        regions = r.json()
        melbourne_region_id = None
        for region in regions:
            if region["name"].lower() == region_name:
                melbourne_region_id = region["id"]
                break

        if melbourne_region_id is None:
            raise Exception(f"Could not find ' {region_name}")

        return melbourne_region_id

    def get_regions(self) -> requests.Response:
        return self._get(self.api_url + "/regions/")

    def execute_scenario(self, scenario: int, queue="default") -> requests.Response:
        """

        :param scenario: id of scenario to be executed
        :param queue: optional parameter to define queue
        :rtype: int
        :rtype: str
        """
        r = self._post(f'{self.api_url}/scenario/{scenario}/execute?queue={queue}')
        if r.status_code != 200:
            raise Exception(f"Unable to execute scenario {r.status_code}, {r.json()}")

    def get_geojsons(self, project: int):
        return self._get(self.api_url + "/geojson/" + str(project))

    def check_status(self, scenario: int):
        """
        Return status of current simulation.

        returns:

        .. code-block::

            {
               status: status code (int),
               status_text: status description
            }

            // CREATED = 1
            // BASE_IN_QUEUE = 2
            // BASE_RUNNING = 3
            // BASE_COMPLETE = 4
            // PA_IN_QUEUE = 5
            // PA_RUNNING = 6
            // PA_COMPLETE = 7
            // COMPLETE = 8

        :param scenario: scenario id
        :type scenario: int
        :return: scenario status
        :rtype: dict

        """
        r = self._get(self.api_url + "/scenario/" + str(scenario) + "/status")
        if r.status_code != 200:
            raise Exception(f"Unable to get status {r.status_code}, {r.json()}")
        return r.json()

    def get_scenario(self, scenario: int):
        return self._get(self.api_url + "/scenario/" + str(scenario))

    def get_simulations(self, scenario: int):
        return self._get(self.api_url + "/scenario/" + str(scenario) + "/simulations")

    def upload_dynamind_model(self, name: str, filename: str) -> int:
        """
        Uploads a new model to the server

        :param name: model name
        :param filename: dynamind file
        :type str
        :return: model_id
        :rtype: int
        """
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')

        r = self.add_model(name, data)

        model_id = r.json()["model_id"]

        return model_id

    def show_node_versions(self, node_id: int):
        return self._get(self.api_url + "/sm_node/" + str(node_id))

    def create_node(self, filename, model_id=None, access_level=AccessLevel.SUPERADMIN.value):
        """
        Create a new node

        :param filename: point to json file containing the node description
        :param model_id: model id in json file will be replaced by this. If not set model_id from json file
        :param access_level: access level of node
        :type str
        :type int
        :type int
        :return: node_id
        :rtype: int
        """
        with open(filename) as json_file:
            node_data = json.load(json_file)

        if model_id is not None:
            node_data["models"][0]["id"] = model_id
            node_data["access_level"] = access_level
        r = self.add_node(node_data)

        if r.status_code == 200:
            result = r.json()
            return result["node_id"]
        raise Exception(f"Unable to add node {r.status_code}, {r.json()}")

    def update_node(self, node_id, filename, model_id=None, access_level=AccessLevel.SUPERADMIN.value):
        """
        Update an existing node

        :param node_id: id of node
        :param filename: point to json file containing the node description
        :param model_id: model id in json file will be replaced by this. If not set model_id from json file
        :param access_level: access level of node
        :type str
        :type str
        :type int
        :type int
        :return: node_id
        :rtype: int
        """
        with open(filename) as json_file:
            node_data = json.load(json_file)

        if model_id is not None:
            node_data["models"][0]["id"] = model_id
            node_data["access_level"] = access_level
        r = self.update_sm_node(node_id, node_data)

        if r.status_code == 200:
            result = r.json()
            return result["node_version_id"]
        raise Exception(f"Unable to update node {r.status_code}, {r.json()}")

    def set_node_access_level(self, node_id, access_level):
        """
        Set the access level of the parent node

        :param node_id: node id
        :param access_level: access level (see enum)
        :type node_id: int
        :type access_level: int
        """
        r = self._post(f"{self.api_url}/sm_node/{node_id}", {"access_level": access_level})
        if r.status_code == 200:
            return
        raise Exception(f"Could not update access level node {r.status_code}, {r.json()}")

    def set_node_properties(self, node_id, properties):
        """
        Set the access level of the parent node

        :param node_id: node id
        :param properties: dict
        :type node_id: int
        :type properties: dict

          .. code-block::

            {
               "active": true or false,
               "access_level": see enum,
               "tags": '["urban from", ...]' // Array as string with tags
               "description": "node description"
               "version_tag": "0.0.1" // Version Tag
            }

        returns:

        """
        r = self._post(f"{self.api_url}/sm_node/{node_id}", properties)
        if r.status_code == 200:
            return
        raise Exception(f"Could not update node properties node {r.status_code}, {r.json()}")

    def set_model_access_level(self, node_id, access_level):
        """
        Set the access level of the performance assessment model

        :param node_id: model id
        :param access_level: access level (see enum)
        :type node_id: int
        :type access_level: int
        """
        r = self._post(f"{self.api_url}/assessment_models/{node_id}", {"access_level": access_level})
        if r.status_code == 200:
            return
        raise Exception(f"Could not update access level performance assessment model {r.status_code}")

    def deactivate_node(self, node_id):
        """
        Deactivate node

        :param node_id: node id
        :type node_id: int
        """
        r = self._post(f"{self.api_url}/sm_node/{node_id}", {"active": False})
        if r.status_code == 200:
            return
        raise Exception(f"Could not deactivate node {r.status_code}, {r.json()}")

    def deactivate_assessment_model(self, node_id):
        """
        Deactivate assessment model

        :param node_id: node id
        :type node_id: int
        """
        r = self._post(f"{self.api_url}/assessment_models/{node_id}", {"active": False})
        if r.status_code == 200:
            return
        raise Exception(f"Could not deactivate assessment model {r.status_code}, {r.json()}")

    def get_baseline(self, project_id):
        """
        Get a projects baseline scenario id

        :param project_id: Project ID
        :type project_id: int
        :return: baseline scenario id
        :rtype: int
        """
        r = self.get_project(project_id)
        scenarios = r.json()["scenarios"]
        scene = next(item for item in scenarios if item["parent"] is None)
        baseline_id = scene["id"]
        return baseline_id

    def get_city_boundray(self, project_id):
        """
        Return a cities geojson boundary id

        :param project_id: project ID
        :type project_id: int
        :return: geojson boundary id
        :rtype: int
        """

        r = self.get_geojsons(project_id)
        geojsons = r.json()
        geojson_city_id = geojsons["geojsons"][0]["id"]
        return geojson_city_id

    def show_nodes(self):
        """
        Prints list of available nodes

        """
        r = self.get_scenario_workflow_nodes()
        if not r.status_code == 200:
            raise Exception(f"Could not get scenario workflow nodes")

        smnodes = r.json()["scenario_maker_nodes"]
        for node in smnodes:
            print(node["id"], node["name"])

    def get_nodes(self):
        """
        Return list of available nodes

        :return: returns a dict of all scenario
        :rtype: dict
        """
        r = self.get_scenario_workflow_nodes()
        if not r.status_code == 200:
            raise Exception(f"Could not get scenario workflow nodes")

        smnodes = r.json()["scenario_maker_nodes"]

        return smnodes

    def show_scenarios(self, project_id):
        """
        Prints a list of the scenarios in a project

        :param project_id: project id
        :type project_id: int
        """
        r = self.get_project(project_id)
        if not r.status_code == 200:
            raise Exception(f"Could not get scenario workflow nodes {r.status_code}, {r.json()}")

        scenarios = r.json()["scenarios"]
        for s in scenarios:
            print(s["id"], s["status"], s["name"])

    def get_scenarios(self, project_id):
        """
        Get a list of scenarios in a project

        :param project_id: project ID
        :type int
        :return: returns a dict of all scenario
        :rtype: dict
        """
        r = self.get_project(project_id)
        if not r.status_code == 200:
            raise Exception(f"Could not get scenario workflow nodes {r.status_code}, {r.json()}")

        scenarios = r.json()["scenarios"]
        return scenarios

    def download_geojson(self, scenario_id, layer_name):
        """
        Download layer as geojson file

        :param scenario_id: scenario id
        :param layern_name:
        :type int
        :type string
        :return: geojson string
        """

        r = self._get(self.api_url + "/scenario/" + str(scenario_id) + "/layer/" + str(layer_name))
        if not r.status_code == 200:
            raise Exception(f"Could not download result {r.status_code}, {r.json()}")

        return r.text

    def show_log(self, scenario_id):
        """
        Print scenario log file

        :param scenario_id: scenario id
        :type scenario_id: int
        """
        r = self.get_simulations( scenario_id)

        if not r.status_code == 200:
            raise Exception(f"Could not get scenario log {r.status_code}, {r.json()}")

        sims = r.json()

        for s in sims["simulations"]:
            database_id = json.loads(s)["id"]

        for s in sims["simulation_instances"]:
            print(json.loads(s)["id"], json.loads(s)["progress"], json.loads(s)["heartbeat"], json.loads(s)["log"])

        return database_id

    def get_node_id(self, name, owner_id=None):
        """
        Return node id to be used in simulation. If multiple nodes with the same id are identified the first node
        belonging to the user is returned first. If owner_id is set only the node owned by the user is returned

        :param name: node name
        :param owner_id: user_id
        :type name: str
        :type owner_id: int
        :return: node_id
        :rtype int
        """
        nodes = self.get_nodes()
        filtered_nodes = []
        for n in nodes:
            if n['name'] == name:
                if owner_id and n['creator'] == owner_id:
                    filtered_nodes.append(n)
                elif not owner_id:
                    filtered_nodes.append(n)
        if len(filtered_nodes) == 0:
            raise Exception(f"Node  {name} not found")

        if len(filtered_nodes) == 1:
            return filtered_nodes[0]["id"]
        # if multiple nodes return the one the user owns
        for n in filtered_nodes:
            if n["creator"] == self.get_my_status()["user_id"]:
                return n["id"]

        return filtered_nodes[0]["id"]

    def create_assessment_model(self, filename, model_id=None):
        """
        Creates a new assessment model and a default version tagged as 0.0.1
        the data must be of the shape:

        :param filename: filename of json file (see below)
        :param model_id: dynamind model id
        :type filename: str
        :type model_id: int

        .. code-block::

            {
               name: "some name",
               description: "some desc",

               //optionally add assessment model stage of development
               //1 = ALPHA
               //2 = BETA
               //3 = UNDER DEVELOPMENT
               //default is 3
               stage: 2
               //must specify one of:
               model_id: <model_id> //by default will use the active version of this model
               model_version_id: <model_version_id> //if present will use this model version id
            }

        returns:

        .. code-block::

            {
              assessment_model_id: <the id of the new assessment model>,
              assessment_model_version_id: <id of the new default version>
            }

        """

        with open(filename) as json_file:
            node_data = json.load(json_file)

        if model_id is not None:
            node_data["model_id"] = model_id

        r = self._post(self.api_url + "/assessment_models", node_data)

        if r.status_code == 200:
            result = r.json()
            return result["assessment_model_id"]
        raise Exception(f"Unable to create assessment model {r.status_code}, {r.json()}")



    def update_assessment_model(self, assessment_model_id, filename, model_id):
        """
        Creates a new assessment model and a default version tagged as 0.0.1
        the data must be of the shape:

        :param assessment_model_id: assessment model id to be updated
        :param filename: filename of json file (see below)
        :param model_id: dynamind model id
        :type assessment_model_id: int
        :type filename: str
        :type model_id: int

        .. code-block::

            {
               name: "some name",
               description: "some desc",

               //optionally add assessment model stage of development
               //1 = ALPHA
               //2 = BETA
               //3 = UNDER DEVELOPMENT
               //default is 3
               stage: 2
               //must specify one of:
               model_id: <model_id> //by default will use the active version of this model
               model_version_id: <model_version_id> //if present will use this model version id
            }

        returns:

        .. code-block::

            {
              assessment_model_id: <the id of the new assessment model>,
              assessment_model_version_id: <id of the new default version>
            }

        """
        with open(filename) as json_file:
            node_data = json.load(json_file)

        if model_id is not None:
            node_data["model_id"] = model_id

        r = self._post(f"{self.api_url}/assessment_models/{assessment_model_id}/versions", node_data)
        if r.status_code == 200:
            result = r.json()
            return result["assessment_model_version_id"]
        raise Exception(f"Unable to update assessment model {r.status_code}, {r.json()}")

    def get_project_databases(self, project_id, folder=".", scenario_id=None):
        """
        Download project databases. Databases will be downloaded into folder/project_id.zip
        For larger projects it is recommended to defined the scenario_id to be downloaded. Otherwise the download might fail

        :param project_id: project id
        :param folder: folder
        :param scenario_id: scenario_id
        :type project_id: int
        :type folder: str
        :type scenario_id: int
        """

        if scenario_id:
            r = self._get(f"{self.api_url}/projects/{project_id}/data?scenario={scenario_id}")
        else:
            r = self._get(f"{self.api_url}/projects/{project_id}/data")
        if r.status_code == 200:
            if scenario_id:
                open(f"{folder}/{project_id}-{scenario_id}.zip", 'wb').write(r.content)
            else:
                open(f"{folder}/{project_id}.zip", 'wb').write(r.content)
            return
        raise Exception(f"Something went wrong while downloading the folder {r.status_code} {r.json()}")

    def get_my_status(self):
        """
        Get user status

        :return: dict with project status
        """

        r = self._get(f"{self.api_url}/user/status/")
        if r.status_code == 200:
            return r.json()

        raise Exception(f"Something when downloading status {r.status_code} {r.json()}")

    def get_default_parameter_dict(self, node_id: int) -> dict:
        """
        Returns default parameter dict for a node

        :param node_id:
        :type node_id: int
        :return: Parameter dict
        :rtype dict
        """
        nodes = self.get_nodes()
        parameter_dict = {}
        for n in nodes:
            if node_id != n['id']:
                continue
            versions = [(idx, v['id']) for idx, v in enumerate(n['versions'])]
            latest_version = max(versions, key=lambda t: t[1])
            version = n['versions'][latest_version[0]]
            for m in version["models"]:
                for p in m['parameter_description']:
                    if 'fields' in p:
                        for f in p['fields']:
                            parameter_dict[f['parameter']] = f['default']
                    if 'parameter' in p:
                        parameter_dict[p['parameter']] = p['default']
            return parameter_dict
        raise Exception(f"Node not found")

    def show_assessment_models(self) -> None:
        """
        List available assessment models

        :return: None
        """
        models = self.get_assessment_models()
        for m in models['assessment_models']:
            print(m['name'])

