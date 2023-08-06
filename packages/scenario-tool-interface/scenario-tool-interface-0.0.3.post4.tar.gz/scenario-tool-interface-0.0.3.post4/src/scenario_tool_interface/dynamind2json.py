import xml.etree.ElementTree as ET
import json
import copy

class DynaMindXML2Json:

    def __init__(self):
        self._nodes = {}

    def _init_data_structure(self, file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()

        dm_nodes = root.find("DynaMindCore/Nodes")
        dm_links = root.find("DynaMindCore/Links")

        links = {}
        for l in dm_links:
            if l.find('OutPort').find('UUID').get("value") in links:
                vec = links[l.find('OutPort').find('UUID').get("value")]
                vec.append(l.find('InPort').find('UUID').get("value"))
                links[l.find('OutPort').find('UUID').get("value")] = vec
                continue
            links[l.find('OutPort').find('UUID').get("value")] = [l.find('InPort').find('UUID').get("value")]

        self._nodes = {}
        group_uuids = set()

        for n in dm_nodes:
            node = {}
            if n.find('UUID').get("value") == "0":
                continue
            node["name"] = n.find('Name').get("value")
            node["class_name"] = n.find('ClassName').get("value")
            node["uuid"] = n.find('UUID').get("value")
            node["group_uuid"] = n.find('GroupUUID').get("value")

            filter = n.find('Filter')
            if filter:
                filter_view = [e.text.strip() for e in filter.findall("filter_view")]
                attribtue_filter = [e.text.strip() for e in filter.findall("attribtue_filter")]
                spatial_filter = [e.text.strip() for e in filter.findall("spatial_filter")]
                node_filter = {}
                node_filter["filter_view"] = filter_view
                node_filter["attribute_filter"] = attribtue_filter
                node_filter["spatial_filter"] = spatial_filter
                node["filter"] = node_filter
                # print(node["name"], node_filter)
            group_uuids.add(node["group_uuid"])
            node["parameters"] = self._generate_parameters(n)
            self._nodes[n.find('UUID').get("value")] = node

        for uuid_in in links.keys():
            node =self._nodes[uuid_in]
            node["link_to"] = links[uuid_in]

    def _generate_parameters(self, node):
        parameters = {}
        ps = node.findall('parameter')
        for p in ps:
            parameters[p.get("name")] = p.text.strip()
        return parameters

    def _start_in_group(self, uuid):
        group_nodes = []
        linked_nodes = []
        start_nodes = []
        for k, n in self._nodes.items():
            if n["group_uuid"] != uuid:
                continue
            group_nodes.append(k)
            if "link_to" not in n:
                continue
            for l in n["link_to"]: # Check if it links to same group level
                if self._nodes[l]["group_uuid"] != uuid:
                    continue
                linked_nodes.append(l)
        for id in group_nodes:
            if id not in linked_nodes:
                start_nodes.append(id)

        return start_nodes

    def _is_group(self, uuid):
        if self._nodes[uuid]["class_name"] == "DMLoopGroup":
            return True
        return False

    def _append_node(self, t, node):
        n = copy.deepcopy(node)
        keys = ['uuid', 'group_uuid', 'link_to']
        for k in keys:
            if k in n: del n[k]
        t.append(n)

        if self._is_group(node["uuid"]):
            branch = []
            keys = ['class_name', 'parameters', 'name']

            for k in keys:
                if k in n: del n[k]
            n["group"] = node["name"]
            n["nodes"] = branch
            return branch
        return t

    def _branch(self, tree, node, group_uuid, down=False):
        if not down:
            tree = self._append_node(tree, node)
        if "link_to" not in node:
            return

        for l in node["link_to"]:
            down = False
            if self._nodes[l]["group_uuid"] != group_uuid:
                continue
            if self._is_group(l):
                self._branch(tree, self._nodes[l], l)
                down = True
            self._branch(tree, self._nodes[l], group_uuid, down)

    def dump(self, file_name, output):
        self._init_data_structure(file_name)
        tree = []
        start_nodes = self._start_in_group("0")
        root_node = {}

        for s in start_nodes:
            # append_clean_node(t, nodes[s])
            root_node["name"] = "root"
            root_node["class_name"] = "DMLoopGroup"
            root_node["uuid"] = ""
            root_node["group_uuid"] = "root"
            root_node["parameters"] = ""
            root_node["uuid"] = "0"
            root_node["link_to"] = [s]
            self._nodes["0"] = root_node

            self._branch(tree, root_node, "0")

        with open(output, 'w') as fp:
            json.dump(tree, fp, indent=2, sort_keys=False)
