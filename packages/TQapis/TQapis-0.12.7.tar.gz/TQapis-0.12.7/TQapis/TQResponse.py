
import xml.etree.ElementTree as ET
import json

class ResponseClass:
    def __init__(self, focus='error', id='', cost=0, expiry_minutes=0, balance=0):
        self.focus = focus
        self.id = id
        self.cost = cost
        self.balance = balance
        self.expiry_minutes = expiry_minutes
        self.results = {}
        self.errors = {}
        self.logs = {}
        self.notes = []

    def fromXml(self, string_xml):
        """
        Parses GET/POST resposne XML-content &
        extract TQ Response-attributes (focus, id, cost, balance, expiry_minutes, results, errors) &
        Update TQ Response Instance with these values.
        """
        store_element = ET.fromstring(string_xml)
        response_element = store_element[0]
        self.cost = float(response_element.attrib['cost'])
        self.balance = float(response_element.attrib['balance'])
        self.focus = response_element.attrib['focus']
        self.id = response_element.attrib['id']
        self.expiry_minutes = float(response_element.attrib['expiry_minutes'])
        result_elements = store_element.findall('./Response/Results/Item')
        if result_elements is not None:
            for node in result_elements:
                tokens = node.text.split('=')
                self.results[tokens[0]] = tokens[1]

        error_elements = store_element.findall('./Response/Errors/Item')
        if error_elements is not None:
            for node in error_elements:
                tokens = node.text.split('=')
                self.errors[tokens[0]] = tokens[1]

        log_elements = store_element.findall('./Response/Logs/Item')
        if log_elements is not None:
            for node in log_elements:
                tokens = node.text.split('=')
                self.logs[tokens[0]] = tokens[1]

        error_elements = store_element.findall('./Response/Note/Item')
        if error_elements is not None:
            for node in error_elements:
                self.notes.append(node.text)
        return


    def toxml(self,store_element):
        response_element = ET.SubElement(store_element, 'Response')
        response_element.attrib['cost'] = "{:.2f}".format(float(self.cost))
        response_element.attrib['balance'] = "{:.2f}".format(float(self.balance))
        response_element.attrib['focus'] = self.focus
        response_element.attrib['id'] = self.id
        response_element.attrib['expiry_minutes'] = "{:.2f}".format(float(self.expiry_minutes))
        results_element = ET.SubElement(response_element, 'Results')
        for key, value in self.results.items():
            item = ET.SubElement(results_element, 'Item')
            item.text = key + "=" + value

        error_element = ET.SubElement(response_element, 'Errors')
        for key, value in self.errors.items():
            item = ET.SubElement(error_element, 'Item')
            item.text = key + "=" + value

        logs_element = ET.SubElement(response_element, 'Logs')
        for key, value in self.logs.items():
            item = ET.SubElement(logs_element, 'Item')
            item.text = key + "=" + value

        notes_element = ET.SubElement(response_element, 'Notes')
        for value in self.notes:
            item = ET.SubElement(notes_element, 'Item')
            item.text = value




    def fromJson(self, string_json):
        """
        Parses GET/POST resposne JSON-content &
        extract TQ Response-attributes (focus, id, cost, balance, expiry_minutes, results, errors) &
        Update TQ Response Instance with these values.
        """
        store_element=json.loads(string_json)
        response_element = store_element['Response']
        self.cost = float(response_element['cost'])
        self.balance = float(response_element['balance'])
        self.focus = response_element['focus']
        self.id = response_element['id']
        self.expiry_minutes = float(response_element['expiry_minutes'])

        result_elements = response_element['Results']
        if result_elements is not None:
            for key, value in result_elements.items():
                self.results[key] = value

        errors_elements = response_element['Errors']
        if errors_elements is not None:
            for key, value in errors_elements.items():
                self.errors[key] =value

        log_elements = response_element['Logs']
        if log_elements is not None:
            for key, value in log_elements.items():
                self.logs[key] = value

        notes_elements = response_element['Notes']
        if notes_elements is not None:
            for note in notes_elements:
                self.notes.append(note)
        return


    def toJson(self, store_node):
        store_node['Response'] =dict()
        response_node=store_node['Response']
        response_node['cost'] = "{:.2f}".format(float(self.cost))
        response_node['balance'] = "{:.2f}".format(float(self.balance))
        response_node['focus'] = self.focus
        response_node['id'] = self.id
        response_node['expiry_minutes'] = "{:.2f}".format(float(self.expiry_minutes))
        response_node['Results']=dict()
        results_node=response_node['Results']

        for key, value in self.results.items():
            results_node[key] = value

        response_node['Errors']=dict()
        errors_node=response_node['Errors']
        for key, value in self.errors.items():
            errors_node[key]=value

        response_node['Logs']=dict()
        logs_node=response_node['Logs']
        for key, value in self.logs.items():
            logs_node[key]= value

        response_node['Notes']=list()
        notes_node=response_node['Notes']

        for value in self.notes:
            notes_node.append(value)



class StoreClass:
    def __init__(self, client_id='', session_id='', id='', version='', note='', source_id='', response=None):
        self.client_id = client_id
        self.session_id = session_id
        self.id = id
        self.version = version
        self.note = note
        self.source_id = source_id
        self.response = response
        if self.response is None:
            self.response=ResponseClass()

    def toxml(self):
        store_element = ET.Element('Store')
        store_element.attrib["client_id"] = self.client_id
        store_element.attrib["session_id"] = self.session_id
        store_element.attrib["id"] = self.id
        store_element.attrib["version"] = self.version
        store_element.attrib["note"] = self.note
        store_element.attrib["source_id"] = self.source_id
        self.response.toxml(store_element)

        return ET.tostring(store_element, encoding='utf8', method='xml')

    def fromXml(self, string_xml):
        """
        Parses GET/POST resposne XML-content &
        extract Store-attributes (client_id, source_id, session_id, id, version, note) &
        triggers extraction of TQ Response Class attributes.
        """
        store_element = ET.fromstring(string_xml)
        self.client_id=store_element.attrib["client_id"]
        self.session_id=store_element.attrib["session_id"]
        self.id=store_element.attrib["id"]
        self.version=store_element.attrib["version"]
        self.note=store_element.attrib["note"]
        self.source_id=store_element.attrib["source_id"]
        self.response.fromXml(string_xml)


    def toJson(self):
        """
        Parses GET/POST resposne JSON-content &
        extract Store-attributes (client_id, source_id, session_id, id, version, note) &
        triggers extraction of TQ Response Class attributes.
        """
        store_node=dict()
        store_element = ET.Element('Store')
        store_node["client_id"] = self.client_id
        store_node["session_id"] = self.session_id
        store_node["id"] = self.id
        store_node["version"] = self.version
        store_node["note"] = self.note
        store_node["source_id"] = self.source_id
        self.response.toJson(store_node)
        return json.dumps(store_node)

    def fromJson(self, string_json):
        """
        Parses GET/POST resposne JSON-content &
        extract Store-attributes (client_id, source_id, session_id, id, version, note) &
        triggers extraction of TQ Response Class attributes.
        """
        store_element = json.loads(string_json)
        self.client_id=store_element["client_id"]
        self.session_id=store_element["session_id"]
        self.id=store_element["id"]
        self.version=store_element["version"]
        self.note=store_element["note"]
        self.source_id=store_element["source_id"]
        self.response.fromJson(string_json)



# input = "<?xml version='1.0' encoding='utf8'?><Store client_id='00000836' session_id='na' id='29521836882698' version='1.0' note='na' source_id='217.42.124.18'><Response cost='0.35' balance='999.65' focus='results' id='29521836882698' expiry_minutes='0.49'><Results><Item>Price=0.185732291648</Item><Item>Currency=eur</Item></Results><Errors /><Logs><Item>save_as=File was saved as test_ir_swap.</Item></Logs><Notes /></Response></Store>"
#
# store= StoreClass()
# store.fromXml(input)
# json_string1=store.toJson()
# store.fromJson(json_string1)
# json_string2=store.toJson()
# store.fromJson(json_string2)
# print(store.toxml())
# ## now implement the JSON
#

