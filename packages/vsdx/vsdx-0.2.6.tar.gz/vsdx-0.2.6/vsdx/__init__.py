from __future__ import annotations
import zipfile
import shutil
import os

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import xml.dom.minidom as minidom   # minidom used for prettyprint

namespace = "{http://schemas.microsoft.com/office/visio/2012/main}"  # visio file name space


# utility functions
def to_float(val: str):
    try:
        if val is None:
            return
        return float(val)
    except ValueError:
        return 0.0


class VisioFile:
    def __init__(self, filename):
        self.filename = filename
        self.directory = f"./{filename.rsplit('.', 1)[0]}"
        self.pages = dict()   # populated by open_vsdx_file()
        self.page_objects = list()  # list of Page objects
        self.page_max_ids = dict()  # maximum shape id, used to add new shapes with a unique Id
        self.open_vsdx_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_vsdx()

    @staticmethod
    def get_elements_by_tag(xml: Element, tag: str):
        items = list()
        for e in xml.iter():
            if e.tag == tag:
                items.append(e)
        return items

    @staticmethod
    def pretty_print_element(xml: Element) -> str:
        return minidom.parseString(ET.tostring(xml)).toprettyxml()

    def open_vsdx_file(self) -> dict:  # returns a dict of each page as ET with filename as key
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(self.directory)

        # load each page file into an ElementTree object
        self.pages = self.load_pages()

        # todo: is this needed? remove
        #for filename, page in self.pages.items():
        #    p = VisioFile.Page(page, filename, 'no name', self)

        return self.pages

    def load_pages(self):
        rel_dir = '{}/visio/pages/_rels/'.format(self.directory)
        page_dir = '{}/visio/pages/'.format(self.directory)

        rels = file_to_xml(rel_dir + 'pages.xml.rels').getroot()
        #print(VisioFile.pretty_print_element(rels))  # rels contains map from filename to Id
        relid_page_dict = {}
        #relid_page_name = {}
        for rel in rels:
            rel_id=rel.attrib['Id']
            page_file = rel.attrib['Target']
            relid_page_dict[rel_id] = page_file
            #relid_page_name[rel_id] = page_name

        pages = file_to_xml(page_dir + 'pages.xml').getroot()  # this contains a list of pages with rel_id and filename
        #print(VisioFile.pretty_print_element(pages))  # pages contains Page name, width, height, mapped to Id
        page_dict = {}  # dict with filename as index

        for page in pages:  # type: Element
            rel_id = page[1].attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            page_name = page.attrib['Name']

            page_filename = relid_page_dict.get(rel_id, None)
            page_path = page_dir + page_filename
            page_dict[page_path] = file_to_xml(page_path)
            self.page_max_ids[page_path] = 0  # initialise page_max_ids dict for each page

            self.page_objects.append(VisioFile.Page(file_to_xml(page_path), page_path, page_name, self))

        return page_dict

    def get_page(self, n: int):
        try:
            # todo: also add get_page_by_name()
            return self.page_objects[n]
        except IndexError:
            return None

    def get_page_names(self):
        return [p.name for p in self.page_objects]

    def get_page_by_name(self, name: str):
        for p in self.page_objects:
            if p.name == name:
                return p

    def get_shapes(self, page_path) -> ET:
        page = self.pages[page_path]  # type: Element
        shapes = None
        # takes pages as an ET and returns a ET containing shapes
        for e in page.getroot():  # type: Element
            if 'Shapes' in e.tag:
                shapes = e
                for shape in e:  # type: Element
                    id = int(self.get_shape_id(shape))
                    max_id = self.page_max_ids[page_path]
                    if id > max_id:
                        self.page_max_ids[page_path] = id
        return shapes

    def get_sub_shapes(self, shape: Element, nth=1):
        for e in shape:
            if 'Shapes' in e.tag:
                nth -= 1
                if not nth:
                    return e

    @staticmethod
    def get_shape_location(shape: Element) -> (float, float):
        x, y = 0.0, 0.0
        for cell in shape:  # type: Element
            if 'Cell' in cell.tag:
                if cell.attrib.get('N'):
                    if cell.attrib['N'] == 'PinX':
                        x = float(cell.attrib['V'])
                    if cell.attrib['N'] == 'PinY':
                        y = float(cell.attrib['V'])
        return x, y

    @staticmethod
    def set_shape_location(shape: Element, x: float, y: float):
        for cell in shape:  # type: Element
            if 'Cell' in cell.tag:
                if cell.attrib.get('N'):
                    if cell.attrib['N'] == 'PinX':
                        cell.attrib['V'] = str(x)
                    if cell.attrib['N'] == 'PinY':
                        cell.attrib['V'] = str(y)

    @staticmethod
    def get_shape_text(shape: ET) -> str:
        text = None
        for t in shape:  # type: Element
            if 'Text' in t.tag:
                if t.text:
                    text = t.text
                else:
                    text = t[0].tail
        return text if text else ""

    @staticmethod
    def set_shape_text(shape: ET, text: str):
        for t in shape:  # type: Element
            if 'Text' in t.tag:
                if t.text:
                    t.text = text
                else:
                    t[0].tail = text

    # context = {'customer_name':'codypy.com', 'year':2020 }
    # example shape text "For {{customer_name}}  (c){{year}}" -> "For codypy.com (c)2020"
    @staticmethod
    def apply_text_context(shapes: Element, context: dict):
        for shape in shapes:  # type: Element
            if 'Shapes' in shape.tag:  # then this is a Shapes container
                VisioFile.apply_text_context(shape, context)  # recursive call
            if 'Shape' in shape.tag:
                # check text against all context keys
                for key in context.keys():
                    text = VisioFile.get_shape_text(shape)
                    r_key = "{{" + key + "}}"
                    if r_key in text:
                        new_text = text.replace(r_key, str(context[key]))
                        VisioFile.set_shape_text(shape, new_text)

    @staticmethod
    def get_shape_id(shape: ET) -> str:
        return shape.attrib['ID']

    def copy_shape(self, shape: Element, page: ET, page_path: str) -> ET:
        # insert shape into first Shapes tag in page
        new_shape = ET.fromstring(ET.tostring(shape))
        for shapes_tag in page.getroot():  # type: Element
            if 'Shapes' in shapes_tag.tag:
                id_map = self.increment_shape_ids(shape, page_path)
                self.update_ids(new_shape, id_map)
                shapes_tag.append(new_shape)
        return new_shape

    def insert_shape(self, shape: Element, shapes: Element, page: ET, page_path: str) -> ET:
        # insert shape into shapes tag, and return updated shapes tag
        id_map = self.increment_shape_ids(shape, page_path)
        self.update_ids(shape, id_map)
        shapes.append(shape)
        return shapes

    def increment_shape_ids(self, shape: Element, page_path: str, id_map: dict=None):
        if id_map is None:
            id_map = dict()
        self.set_new_id(shape, page_path, id_map)
        for e in shape:  # type: Element
            if 'Shapes' in e.tag:
                self.increment_shape_ids(e, page_path, id_map)
            if 'Shape' in e.tag:
                self.set_new_id(e, page_path, id_map)
        return id_map

    def set_new_id(self, element: Element, page_path: str, id_map: dict):
        if element.attrib.get('ID'):
            current_id = element.attrib['ID']
            max_id = self.page_max_ids[page_path] + 1
            id_map[current_id] = max_id  # record mappings
            element.attrib['ID'] = str(max_id)
            self.page_max_ids[page_path] = max_id
        else:
            print(f"no ID attr in {element.tag}")

    def update_ids(self, shape: Element, id_map: dict):
        # update: <ns0:Cell F="Sheet.15! replacing 15 with new id using prepopulated id_map
        # cycle through shapes looking for Cell tag inside a Shape tag, which may be inside a Shapes tag
        for e in shape:
            if 'Shapes' in e.tag:
                self.update_ids(e, id_map)
            if 'Shape' in e.tag:
                # look for Cell elements
                for c in e:  # type: Element
                    if 'Cell' in c.tag:
                        if c.attrib.get('F'):
                            f = str(c.attrib['F'])
                            if f.startswith("Sheet."):
                                # update sheet refs with new ids
                                id = f.split('!')[0].split('.')[1]
                                new_id = id_map[id]
                                new_f = f.replace(f'Sheet.{id}',f'Sheet.{new_id}')
                                c.attrib['F'] = new_f
        return shape

    def close_vsdx(self):
        try:
            # Remove extracted folder
            shutil.rmtree(self.directory)
        except FileNotFoundError:
            pass

    def save_vsdx(self, new_filename=None):
        # write the pages to file
        #for key in self.pages.keys():
        #    xml_to_file(self.pages[key], key)

        for page in self.page_objects:  # type: VisioFile.Page
            xml_to_file(page.xml, page.filename)

        # wrap up files into zip and rename to vsdx
        base_filename = self.filename[:-5]  # remove ".vsdx" from end
        print(f"self.directory={self.directory} new_filename={new_filename}")
        if new_filename.find(os.sep) > 0:
            directory = new_filename[0:new_filename.find(os.sep)]
            if directory:
                print(f"directory={directory}")
                if not os.path.exists(directory):
                    os.mkdir(directory)
        shutil.make_archive(base_filename, 'zip', self.directory)
        if not new_filename:
            shutil.move(base_filename + '.zip', base_filename + '_new.vsdx')
        else:
            if new_filename[-5:] != '.vsdx':
                new_filename += '.vsdx'
            print(f"save_vsdx() move from {base_filename+'.zip'} to {new_filename}")
            shutil.move(base_filename + '.zip', new_filename)
        self.close_vsdx()

    class Cell:
        def __init__(self, xml: Element, shape: VisioFile.Shape):
            self.xml = xml
            self.shape = shape

        @property
        def value(self):
            return self.xml.attrib.get('V')

        @value.setter
        def value(self, value: str):
            self.xml.attrib['V'] = str(value)

        @property
        def name(self):
            return self.xml.attrib.get('N')

        @property
        def func(self):  # assume F stands for function, i.e. F="Width*0.5"
            return self.xml.attrib.get('F')

        def __repr__(self):
            return f"Cell: name={self.name} val={self.value} func={self.func}"

    class Shape:  # or page
        def __init__(self, xml: Element, parent_xml: Element, page: VisioFile.Page):
            self.xml = xml
            self.parent_xml = parent_xml
            self.tag = xml.tag
            self.ID = xml.attrib['ID'] if xml.attrib.get('ID') else None
            self.type = xml.attrib['Type'] if xml.attrib.get('Type') else None
            self.page = page

            # get Cells in Shape
            self.cells = dict()
            for e in self.xml:
                if e.tag == namespace+"Cell":
                    cell = VisioFile.Cell(xml=e, shape=self)
                    self.cells[cell.name] = cell

        def __repr__(self):
            return f"<Shape tag={self.tag} ID={self.ID} type={self.type} text='{self.text}' >"

        def cell_value(self, name: str):
            cell = self.cells.get(name)
            return cell.value if cell else None

        def set_cell_value(self, name: str, value: str):
            cell = self.cells.get(name)
            if cell:  # only set value of existing item
                cell.value = value

        @property
        def x(self):
            return to_float(self.cell_value('PinX'))

        @x.setter
        def x(self, value: float or str):
            self.set_cell_value('PinX', str(value))

        @property
        def y(self):
            return to_float(self.cell_value('PinY'))

        @y.setter
        def y(self, value: float or str):
            self.set_cell_value('PinY', str(value))

        @property
        def begin_x(self):
            return to_float(self.cell_value('BeginX'))

        @begin_x.setter
        def begin_x(self, value: float or str):
            self.set_cell_value('BeginX', str(value))

        @property
        def begin_y(self):
            return to_float(self.cell_value('BeginY'))

        @begin_y.setter
        def begin_y(self, value: float or str):
            self.set_cell_value('BeginY', str(value))

        @property
        def end_x(self):
            return to_float(self.cell_value('EndX'))

        @end_x.setter
        def end_x(self, value: float or str):
            self.set_cell_value('EndX', str(value))

        @property
        def end_y(self):
            return to_float(self.cell_value('EndY'))

        @end_y.setter
        def end_y(self, value: float or str):
            self.set_cell_value('EndY', str(value))

        def move(self, x_delta: float, y_delta: float):
            self.x = self.x + x_delta
            self.y = self.y + y_delta

        @property
        def height(self):
            return to_float(self.cell_value('Height'))

        @height.setter
        def height(self, value: float or str):
            self.set_cell_value('Height', str(value))

        @property
        def width(self):
            return to_float(self.cell_value('Width'))

        @width.setter
        def width(self, value: float or str):
            self.set_cell_value('Width', str(value))

        @staticmethod
        def get_all_text_from_xml(x: Element, s: str = None) -> str:
            if s is None:
                s = ''
            if x.text:
                s += x.text
            if x.tail:
                s += x.tail
            for i in x:
                s = VisioFile.Shape.get_all_text_from_xml(i, s)
            return s

        @staticmethod
        def clear_all_text_from_xml(x: Element):
            x.text = ''
            x.tail = ''
            for i in x:
                VisioFile.Shape.clear_all_text_from_xml(i)

        @property
        def text(self):
            text = None
            for t in self.xml:  # type: Element
                if 'Text' in t.tag:
                    if t.text:
                        text = t.text
                    if not text:
                        text = self.get_all_text_from_xml(t)
            return text.replace('\n','') if text else ""

        @text.setter
        def text(self, value):
            for t in self.xml:  # type: Element
                if 'Text' in t.tag:
                    VisioFile.Shape.clear_all_text_from_xml(t)
                    t.text = value

        def sub_shapes(self):
            shapes = list()
            # for each shapes tag, look for Shape objects
            for e in self.xml:  # type: Element
                if e.tag == namespace+'Shapes':
                    for shape in e:  # type: Element
                        if shape.tag == namespace+'Shape':
                            shapes.append(VisioFile.Shape(shape, e, self.page))
                if e.tag == namespace+'Shape':
                    shapes.append(VisioFile.Shape(e, self.xml, self.page))
            return shapes

        def find_shape_by_id(self, shape_id: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.ID == shape_id:
                    return shape
                if shape.type == 'Group':
                    found = shape.find_shape_by_id(shape_id)
                    if found:
                        return found

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    return shape
                if shape.type == 'Group':
                    found = shape.find_shape_by_text(text)
                    if found:
                        return found

        def find_shapes_by_text(self, text: str, shapes: list[VisioFile.Shape] = None) -> list[VisioFile.Shape]:
            # recursively search for shapes by text and return all matches
            if not shapes:
                shapes = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    shapes.append(shape)
                if shape.type == 'Group':
                    found = shape.find_shapes_by_text(text)
                    if found:
                        shapes.extend(found)
            return shapes

        def apply_text_filter(self, context: dict):
            # check text against all context keys
            for key in context.keys():
                text = self.text
                r_key = "{{" + key + "}}"
                if r_key in text:
                    new_text = text.replace(r_key, str(context[key]))
                    self.text = new_text
            for s in self.sub_shapes():
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            # find and replace text in this shape and sub shapes
            text = self.text
            self.text = text.replace(old, new)

            for s in self.sub_shapes():
                s.find_replace(old, new)

        def remove(self):
            self.parent_xml.remove(self.xml)

        def append_shape(self, append_shape: VisioFile.Shape):
            # insert shape into shapes tag, and return updated shapes tag
            id_map = self.page.vis.increment_shape_ids(append_shape.xml, self.page.filename)
            self.page.vis.update_ids(append_shape.xml, id_map)
            self.xml.append(append_shape.xml)

        @property
        def connects(self):
            # get list of connect items linking shapes
            connects = list()
            for c in self.page.connects:
                if self.ID in [c.shape_id, c.connector_shape_id]:
                    connects.append(c)
            return connects

        @property
        def connected_shapes(self):
            # return a list of connected shapes
            shapes = list()
            for c in self.connects:
                if c.connector_shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.connector_shape_id))
                if c.shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.shape_id))
            return shapes

    class Connect:
        def __init__(self, xml: Element):
            self.xml = xml
            self.from_id = xml.attrib.get('FromSheet')  # ref to the connector shape
            self.connector_shape_id = self.from_id
            self.to_id = xml.attrib.get('ToSheet')  # ref to the shape where the connector terminates
            self.shape_id = self.to_id
            self.from_rel = xml.attrib.get('FromCell')  # i.e. EndX / BeginX
            self.to_rel = xml.attrib.get('ToCell')  # i.e. PinX

        def __repr__(self):
            return f"Connect: from={self.from_id} to={self.to_id} connector_id={self.connector_shape_id} shape_id={self.shape_id}"

    class Page:
        def __init__(self, xml: ET.ElementTree, filename: str, page_name: str, vis: VisioFile):
            self._xml = xml
            self.filename = filename
            self.name = page_name
            self.vis = vis
            self.connects = self.get_connects()

        def __repr__(self):
            return f"<Page name={self.name} file={self.filename} >"

        @property
        def xml(self):
            return self._xml

        @property
        def shapes(self):
            # list of Shape objects in Page
            page_shapes = list()
            for shape in self.xml.getroot():
                if shape.tag in [namespace + 'Shape', namespace + 'Shapes']:
                    page_shapes.append(VisioFile.Shape(shape, self.xml, self))
            return page_shapes

        def get_connects(self):
            connects = list()
            elements = VisioFile.get_elements_by_tag(self.xml, namespace+'Connect')
            for e in elements:
                connects.append(VisioFile.Connect(e))
            return connects

        def get_connectors_between(self, shape_a_id: str='', shape_a_text: str='',
                                  shape_b_id: str='', shape_b_text: str=''):
            shape_a = self.find_shape_by_id(shape_a_id) if shape_a_id else self.find_shape_by_text(shape_a_text)
            shape_b = self.find_shape_by_id(shape_b_id) if shape_b_id else self.find_shape_by_text(shape_b_text)
            connector_ids = set(a.ID for a in shape_a.connected_shapes).intersection(
                set(b.ID for b in shape_b.connected_shapes))

            connectors = set()
            for id in connector_ids:
                connectors.add(self.find_shape_by_id(id))
            return connectors

        def apply_text_context(self, context: dict):
            for s in self.shapes:
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            for s in self.shapes:
                s.find_replace(old, new)

        def find_shape_by_id(self, shape_id) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_id(shape_id)
                if found:
                    return found

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_text(text)
                if found:
                    return found

        def find_shapes_by_text(self, text: str) -> list[VisioFile.Shape]:
            shapes = list()
            for s in self.shapes:
                found = s.find_shapes_by_text(text)
                if found:
                    shapes.extend(found)
            return shapes


def file_to_xml(filename: str) -> ET.ElementTree:
    tree = ET.parse(filename)
    return tree


def xml_to_file(xml: ET.ElementTree, filename: str):
    xml.write(filename)
