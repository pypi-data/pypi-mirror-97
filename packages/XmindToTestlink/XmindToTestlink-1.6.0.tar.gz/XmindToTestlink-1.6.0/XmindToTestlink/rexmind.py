from __future__ import unicode_literals
import zipfile
import os
import codecs
import json
import argparse
try:
    from XmindToTestlink import markdown_to_dict
    from XmindToTestlink import dict_to_json
    from XmindToTestlink import zip_need
    from XmindToTestlink import read_xml
except ImportError:
    import markdown_to_dict
    import dict_to_json
    import zip_need
    import read_xml

def get_dpath(in_dict, pre_path = ''):
    path_list = []
    for k in in_dict:
        l1_path = os.path.join(pre_path, k)
        if isinstance(in_dict[k], list):
            for n,v in enumerate(in_dict[k]):
                l2_path = os.path.join(l1_path, str(n))
                path_list.append(l2_path.strip("/"))
                if k != "cases":
                    path_list.extend(get_dpath(v, l2_path))
    return path_list

def get_delem(in_dict, dpath, key = ''):
    path = dpath.strip('/').split('/')
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
        else:
            msg += "[\'"  + i + "\']"
    if key != '':
        msg += "[\'"  + key + "\']"
    return eval("in_dict" + msg)

def get_suite_case_path_list(path_list):
    suite_path_list = []
    case_path_list = []
    for path in path_list:
        if path.find('cases') >= 0:
            case_path_list.append(path)
        else:
            suite_path_list.append(path)
    return suite_path_list,case_path_list

def clean_notes(down_dict):
    down_dpath = get_dpath(down_dict)
    suite_path_list,case_path_list = get_suite_case_path_list(down_dpath)
    for i in suite_path_list:
        suite = get_delem(down_dict, i)
        suite['detail'] = ''
    for i in case_path_list:
        suite = get_delem(down_dict, i)
        suite['summary'] = ''

def md_to_xmind():
    output_zip = "_xmind_output/zip_need"
    output_dir = "_xmind_output"
    if not os.path.exists(output_zip):
        os.makedirs(output_zip)

    parser = argparse.ArgumentParser(description = "") 
    parser.add_argument('-f', '--file', dest='file', metavar='File', nargs=1, \
            required = True, help='file')
    parser.add_argument('-t', '--type', dest='file_type', choices=['md','xml_req','xml_case'], \
            default='md', help='file type')
    parser.add_argument('-c', '--clean', dest='need_clean', action='store_const', \
            const = True, default = False, help="rexmind without case&req's notes")
    args = parser.parse_args()
    #print(args)
    test_file_list = args.file
    file_type = args.file_type
    need_clean = args.need_clean

    md_file = test_file_list[0]
    xmind_name = ".".join(os.path.basename(md_file).split(".")[:-1]) + ".xmind"

    md = markdown_to_dict.MarkdownToDict()
    dj = dict_to_json.DictToJson()

    if file_type == "md":
        re_dict = md.start(md_file)
    elif file_type == "xml_req":
        re_dict = read_xml.read_req_xml(md_file)
    elif file_type == "xml_case":
        re_dict = read_xml.read_case_xml(md_file)
    if need_clean:
        clean_notes(re_dict)

    js_dict = dj.start(re_dict)

    json_str = json.dumps(js_dict, ensure_ascii=False)
    of = codecs.open(os.path.join(output_zip,"content.json"),"w",'utf-8')
    of.write(json_str)
    of.close()

    json_str = json.dumps(zip_need.manifest, ensure_ascii=False)
    of = codecs.open(os.path.join(output_zip,"manifest.json"),"w",'utf-8')
    of.write(json_str)
    of.close()

    json_str = json.dumps(zip_need.metadata, ensure_ascii=False)
    of = codecs.open(os.path.join(output_zip,"metadata.json"),"w",'utf-8')
    of.write(json_str)
    of.close()

    z = zipfile.ZipFile(os.path.join(output_dir,xmind_name), 'w')
    for d in os.listdir(output_zip):
        z.write(os.path.join(output_zip, d), d)
    z.close()
    #print(json_str)
    print("\ncreate success\noutput : " + os.path.join(output_dir,xmind_name))

if __name__ == "__main__":
    md_to_xmind()
