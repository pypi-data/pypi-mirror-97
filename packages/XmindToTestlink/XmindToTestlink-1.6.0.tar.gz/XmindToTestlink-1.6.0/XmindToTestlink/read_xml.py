import xml.etree.ElementTree as ET

tag = {
    "ts":"testsuite",
    "tc":"testcase",
    "dt":"details",
    "sm":"summary",
    "cfs":"custom_fields",
    "cf":"custom_field",
    "sts":"steps",
    "st":"step",
    "sn":"step_number",
    "ac":"actions",
    "ep":"expectedresults",
    "pc":"preconditions",
    "ip":"importance",
    "et":"execution_type",
    "nm":"name",
    "val":"value",
    "reqs":"requirements",
    "req":"requirement",
    "rst":"req_spec_title",
    "did":"doc_id",
    "rqt":"title"
}

def get_suite(name, suite_detail = ''):
    suite = {
            'title':'',
            'detail':'',
            'suites':[],
            'cases':[]
            }
    suite['title'] = name
    suite['detail'] = suite_detail
    return suite

def get_cdata(elem, path):
    #cdata = elem.findtext(path).strip("<p></p>\t\n")
    #cdata = elem.findtext(path).replace('\t','').replace('\n','').strip("<p></p>")
    cdata = elem.findtext(path)
    return cdata

def clean_data(msg):
    return msg.replace('<p>','').replace('</p>','').replace('<br />','\n').strip(" \n")
    #return msg

def get_case(elem, band_msg):
    case = {
            'title':'',
            'summary':'',
            'preconditions':'',
            'importance':'2',
            'execution_type':'',
            'custom_field':'',
            'step':''
            }

    if elem.attrib != {}:
        case['title'] = elem.attrib['name']
    if elem.find(tag['sm']) != None:
        case['summary'] = clean_data(get_cdata(elem, tag['sm']))
    if elem.find(tag['pc']) != None:
        case['preconditions'] = get_cdata(elem, tag['pc'])
    if elem.find(tag['et']) != None:
        case['execution_type'] = get_cdata(elem, tag['et'])
    if elem.find(tag['ip']) != None:
        case['importance'] = get_cdata(elem, tag['ip'])
    if elem.find(tag['sts']) != None:
        case['step'] = []
        for step in elem.findall(tag['sts'] + "/" + tag['st']):
            case['step'].append({
                'action':get_cdata(step, tag['ac']),
                'expect':get_cdata(step, tag['ep']),
                'notes':'',
                })
    if elem.find(tag['cfs']) != None:
        case['custom_field'] = []
        for custom in elem.findall(tag['cfs'] + "/" + tag['cf']):
            if custom.findtext(tag['val']) != '' :
                case['custom_field'].append({custom.findtext(tag['nm']): custom.findtext(tag['val'])})
        if case['custom_field'] == []:
            case['custom_field'] = ''
    if band_msg:
        if elem.find(tag['reqs']) != None:
            case['old_band'] = []
            for req in elem.findall(tag['reqs'] + "/" + tag['req']):
                case['old_band'].append({req.findtext(tag['did']):req.findtext(tag['rqt'])})
    return case

def get_case_dict(elem, out_dict, band_msg):
    if elem.tag == "testsuite":
        suite_name = elem.attrib['name']
        if elem.find(tag['dt']) != None:
            suite_detail = clean_data(get_cdata(elem, tag['dt']))
        else :
            suite_detail = ''
        suite = get_suite(suite_name, suite_detail)
        out_dict['suites'].append(suite)
        out_dict = suite
        for child in elem:
            if child.tag == 'details':
                pass
            elif child.tag == 'testcase':
                out_dict['cases'].append(get_case(child, band_msg))
            elif child.tag == 'testsuite':
                get_case_dict(child, out_dict, band_msg)

def read_req_id(elem):
    if elem.find("docid") != None:
        req_id = get_cdata(elem, 'docid')
    if elem.find("title") != None:
        tmp_name = get_cdata(elem, 'title')
    return req_id, tmp_name



def get_req_id_dict(elem, pre_name = ''):
    id_dict = {}
    tmp_name = elem.attrib['title']
    req_id = elem.attrib['doc_id']
    req_name = pre_name + "/" + tmp_name
    pre_name = req_name
    id_dict[req_name] = req_id
    for child in elem:
        if child.tag == 'requirement':
            req_id, tmp_name = read_req_id(child)
            req_name = pre_name + "/" + tmp_name
            id_dict[req_name] = req_id
        elif child.tag == 'req_spec':
            id_dict.update(get_req_id_dict(child, pre_name))
    return id_dict

def read_case_xml(xml_file, band_msg = True):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    out_dict = get_suite("最外层")
    get_case_dict(root, out_dict, band_msg)
    return out_dict['suites'][0]

def get_req(elem):
    case = {
            'title':'',
            'summary':'',
            'custom_field':'',
            }
    if elem.find('title') != None:
        case['title'] = get_cdata(elem, 'title')
    if elem.find('description') != None:
        case['summary'] = clean_data(get_cdata(elem, 'description'))
    if elem.find(tag['cfs']) != None:
        case['custom_field'] = []
        for custom in elem.findall(tag['cfs'] + "/" + tag['cf']):
            if custom.findtext(tag['val']) != '' :
                case['custom_field'].append({custom.findtext(tag['nm']): custom.findtext(tag['val'])})
        if case['custom_field'] == []:
            case['custom_field'] = ''
    return case


def get_req_dict(reqs):
    suite_name = reqs.attrib['title']
    if reqs.find('scope') != None:
        suite_detail = clean_data(get_cdata(reqs, 'scope'))
    else :
        suite_detail = ''
    suite = get_suite(suite_name, suite_detail)
    #out_dict['suites'].append(suite)
    #out_dict = suite
    for child in reqs:
        if child.tag == 'requirement':
            suite['cases'].append(get_req(child))
        elif child.tag == 'req_spec':
            suite['suites'].append(get_req_dict(child))
    return suite

def read_req_xml(xml_file):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    out_dict = get_suite("最外层")
    for child in root:
        if child.tag == "req_spec":
            out_dict['suites'].append(get_req_dict(child))
        if child.tag == 'requirement':
            out_dict['cases'].append(get_req(child))
    return out_dict['suites'][0]

def cdata(element, content):
    '''
    添加xml中的cdata标签
    '''
    if isinstance(content, int):
        content = str(content)
    content = content.replace("\n", "<br />")  # replace new line for *nix system
    element.append(ET.Comment(' --><![CDATA[' + content + ']]><!-- '))

def read_req_id_xml(xml_file, skip_first_leval = 0):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    if skip_first_leval:
        root = root[0]
    id_dict = {}
    req_out = ET.Element('requirements')
    for child in root:
        if child.tag == 'req_spec':
            if id_dict == {}:
                id_dict = get_req_id_dict(child)
            else:
                id_dict.update(get_req_id_dict(child))
        if child.tag == 'requirement':
            req_id, tmp_name = read_req_id(child)
            req_name = "/" + tmp_name
            id_dict[req_name] = req_id
            tc = ET.SubElement(req_out, 'requirement')
            tt = ET.SubElement(tc, 'title')
            cdata(tt, tmp_name)
            rid = ET.SubElement(tc, 'docid')
            cdata(rid, req_id)
    #id_dict['root_req_spec'] = child.attrib['title']
    if req_out.__len__() > 0:
        xml_path = xml_file.replace('req.xml','requirement.xml')
        w = ET.ElementTree(req_out)
        w.write(xml_path, 'utf-8', True)
    return id_dict

def get_only_reqs_id_dict(elem, pre_name = ''):
    id_dict = {}
    tmp_name = elem.attrib['title']
    req_id = elem.attrib['doc_id']
    req_name = pre_name + "/" + tmp_name
    pre_name = req_name
    id_dict[req_name] = req_id
    for child in elem:
        if child.tag == 'req_spec':
            id_dict.update(get_only_reqs_id_dict(child, pre_name))
    return id_dict

def read_only_reqs_id_xml(xml_file):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    id_dict = {}
    req_out = ET.Element('requirements')
    for child in root:
        if child.tag == 'req_spec':
            if id_dict == {}:
                id_dict = get_only_reqs_id_dict(child)
            else:
                id_dict.update(get_only_reqs_id_dict(child))
    return id_dict

def get_root_id(xml_file):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    for child in root:
        if child.tag == "req_spec":
            root_id = child.attrib["doc_id"]
            return  root_id

def get_root_name(xml_file):
    tree = ET.ElementTree(file = xml_file)
    root = tree.getroot()
    return root.attrib['name']

if __name__ == "__main__":
    #print(read_case_xml('./ddd.xml', False))
    #print(get_root_name("./ddd.xml"))
    #print(read_req_id_xml('./case_req.xml'))
    print(read_req_id_xml('./rrr.xml'))
    #print(read_req_xml('./chip_req.xml'))
