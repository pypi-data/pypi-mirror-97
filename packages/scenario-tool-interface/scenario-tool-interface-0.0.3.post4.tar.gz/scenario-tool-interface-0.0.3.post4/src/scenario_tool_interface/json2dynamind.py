from lxml import etree as ET

import uuid
import json

class Json2DynaMindXML:

    def __init__(self):
        pass

    def _write_gui_node(self, gui_nodes, uuid, pos_x, pos_y = 0 ):
        node = ET.SubElement(gui_nodes, 'GUI_Node')

        ET.SubElement(node, 'GUI_UUID').attrib["value"] = uuid
        ET.SubElement(node, 'GUI_PosX').attrib["value"] = str(pos_x * 300)
        ET.SubElement(node, 'GUI_PosY').attrib["value"] = str(pos_y)
        ET.SubElement(node, 'GUI_Mini').attrib["value"] = str(0)

    def _write_node(self, nodes, group_uuid, n_dict=None):

        node = ET.SubElement(nodes, 'Node')


        class_name = ET.SubElement(node, 'ClassName')
        class_name.attrib["value"] = n_dict['class_name']


        uuid = ET.SubElement(node, 'UUID')
        uuid.attrib["value"] = n_dict['uuid']

        name = ET.SubElement(node, 'Name')
        name.attrib["value"] = n_dict['name']

        group = ET.SubElement(node, 'GroupUUID')
        group.attrib["value"] = group_uuid


        if "parameters" in n_dict:
            for p, val in n_dict["parameters"].items():
                param = ET.SubElement(node, 'parameter')
                param.attrib["name"] = p
                param.text = val

        if "filter" in n_dict:

            filter_view = "".join(n_dict["filter"]["filter_view"])
            attribute_filter = "".join(n_dict["filter"]["attribute_filter"])
            spatial_filter = "".join(n_dict["filter"]["spatial_filter"])

            filter = ET.SubElement(node, 'Filter')
            view_name = ET.SubElement(filter, 'view_name')
            view_name.text = filter_view

            af = ET.SubElement(filter, 'attribtue_filter')
            af.text = attribute_filter

            sf = ET.SubElement(filter, 'spatial_filter')
            sf.text = spatial_filter


    def _write_link(self, links, node_from, node_to):

        link = ET.SubElement(links, 'Link')

        ET.SubElement(link, 'BackLink').attrib["value"] = "0"

        inport = ET.SubElement(link, 'InPort')
        ET.SubElement(inport, 'UUID').attrib["value"] = node_to
        ET.SubElement(inport, 'PortName').attrib["value"] = "city"
        ET.SubElement(inport, 'PortType').attrib["value"] = "0"

        outport = ET.SubElement(link, 'OutPort')
        ET.SubElement(outport, 'UUID').attrib["value"] = node_from
        ET.SubElement(outport, 'PortName').attrib["value"] = "city"
        ET.SubElement(outport, 'PortType').attrib["value"] = "0"


    def _write_headers(self, dynamind):

        info = ET.SubElement(dynamind, 'Info')
        info.attrib["Version"] = "0.5"

        dynamind_core = ET.SubElement(dynamind, 'DynaMindCore')
        dynamind_gui = ET.SubElement(dynamind, 'DynaMindGUI')
        dynamind_gui_nodes = ET.SubElement(dynamind_gui, 'GUI_Nodes')

        settings = ET.SubElement(dynamind_core, 'Settings')

        epsg = ET.SubElement(settings, 'EPSG')
        epsg.attrib["value"] = '3857'

        workdir = ET.SubElement(settings, 'WorkingDir')
        workdir.attrib["value"] = '/tmp'

        keep_sys = ET.SubElement(settings, 'KeepSystems')
        keep_sys.attrib["value"] = '0'

        nodes = ET.SubElement(dynamind_core, 'Nodes')

        node = ET.SubElement(nodes, 'RootNode')
        uuid = ET.SubElement(node, 'UUID')
        uuid.attrib["value"] = '0'


        links = ET.SubElement(dynamind_core, 'Links')

        return nodes, links, dynamind_gui_nodes

    def _write_to_file(self, root, file_name):
        with open(file_name, 'w')as dynamind_file:
            xml_str = ET.tostring(root, pretty_print=True).decode('utf-8')
            dynamind_file.write(xml_str)

    def _create_group_nodes(self, nodes, links, gui_nodes, group_uuid, group):

        n_prev = None
        elements_pos = 0
        for n in group["nodes"]:
            next_uuid = str(uuid.uuid4())
            if not n_prev and group_uuid != "0":
                n_prev = group_uuid
            if "group" in n:
                self._write_node(nodes, group_uuid, self._create_default_group(n, next_uuid))
                self._create_group_nodes(nodes, links, gui_nodes, next_uuid, n)

            else:
                n["uuid"] = next_uuid
                self._write_node(nodes, group_uuid, n)
            if (n_prev):
                self._write_link(links, n_prev, next_uuid)
            self._write_gui_node(gui_nodes, next_uuid, elements_pos)

            elements_pos+=1
            n_prev = next_uuid

        # Last Link
        if (n_prev and group_uuid != "0"):
            self._write_link(links, next_uuid, group_uuid)

    def _create_default_group(self, n, next_uuid):
        g = {}
        g["uuid"] = next_uuid
        g["class_name"] = "DMLoopGroup"
        g["name"] = n["group"]
        s = {}
        s["writeStreams"] = "city*|*"
        s["readStreams"] = ""
        g["parameters"] = s
        return g

    def dump(self, input_file, output_file):
        root = ET.Element('DynaMind')
        with open(input_file) as json_file:
            data_structure = json.load(json_file)
        nodes, links, dynamind_gui_nodes = self._write_headers(root)
        self._create_group_nodes(nodes, links, dynamind_gui_nodes, "0", data_structure[0])
        self._write_to_file(root, output_file)












