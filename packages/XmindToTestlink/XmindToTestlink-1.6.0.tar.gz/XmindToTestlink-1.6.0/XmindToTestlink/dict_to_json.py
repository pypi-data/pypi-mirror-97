from __future__ import unicode_literals
import zipfile
import os
import codecs
import json
try:
    from XmindToTestlink import read_xml
except ImportError:
    import read_xml

class DictToJson(object):
    def __init__(self):
        self.root = [{
                'class':'sheet',
                'title':'导图1',
                'topicPositioning':'fixed',
                'rootTopic':'',
                }]
        
        self.topic = {
                "class":"topic",
                "title":"",
                "structureClass":"org.xmind.ui.map.unbalanced",
                "children":''
                } 
        self.theme = {
                "subTopic":{
                    "properties":{
                        "for:text-agign":"left"
                        }
                    }
                }
    def create_attach(self, in_dict):
        attach = {
                "children":{},
                }
        attach['title'] = in_dict['title']
        if 'summary' in in_dict and in_dict['summary'] != '':
            attach['notes'] = {"plain":{"content":in_dict['summary']}}
        if 'custom_field' in in_dict and in_dict['custom_field'] != '':
            if 'attached' not in attach['children']:
                attach['children']['attached'] = []
            attach['children']['attached'].append(self.create_attach({'title':'属性'}))
            k_tmp = attach['children']['attached'][0]['children']
            k_tmp['attached'] = []
            for custom in in_dict['custom_field']:
                for k,v in custom.items():
                    k_tmp['attached'].append(self.create_attach({'title':k}))
                    v_tmp = k_tmp['attached'][-1]['children']
                    v_tmp['attached'] = []
                    v_tmp['attached'].append(self.create_attach({'title':v}))
        if 'step' in in_dict and in_dict['step'] != '':
            if 'attached' not in attach['children']:
                attach['children']['attached'] = []
            attach['children']['attached'].append(self.create_attach({'title':'步骤'}))
            k_tmp = attach['children']['attached'][0]['children']
            k_tmp['attached'] = []
            for step in in_dict['step']:
                for k,v in step.items():
                    k_tmp['attached'].append(self.create_attach({'title':k}))
                    v_tmp = k_tmp['attached'][-1]['children']
                    v_tmp['attached'] = []
                    v_tmp['attached'].append(self.create_attach({'title':v}))
        return attach

    def get_json(self, in_dict, out_dict):
        if "title" in in_dict.keys():
            pass
        if "cases" in in_dict.keys() and in_dict['cases'] != []:
            if 'attached' not in out_dict:
                out_dict['attached'] = []
            for case in in_dict['cases']:
                out_dict['attached'].append(self.create_attach(case))
        if "suites" in in_dict.keys() and in_dict['suites'] != []:
            if 'attached' not in out_dict:
                out_dict['attached'] = []
            for suite in in_dict['suites']:
                out_dict['attached'].append(self.create_attach(suite))
                if suite['detail'] != '':
                    out_dict['attached'][-1]['notes'] = {"plain":{"content":suite['detail']}}
                self.get_json(suite, out_dict['attached'][-1]["children"])

    def start(self, total_dict):
        self.root[0]['rootTopic'] = self.topic
        #self.root[0]['theme'] = self.theme
        self.topic['title'] = total_dict['title']
        #del total_dict['title']

        children = {}
        self.get_json(total_dict, children)
        self.topic['children'] = children
        #print(self.root)
        return self.root

if __name__ == "__main__":
    #dict1 = read_xml.read_req_xml("./demux.xml")
    dj = DictToJson()
    js_dict = dj.start(dict1)
    json_str = json.dumps(js_dict, ensure_ascii=False)
    of = codecs.open("./zip_need/content.json","w",'utf-8')
    of.write(json_str)
    of.close()
    xmind_name = "aaa.xmind"
    z = zipfile.ZipFile(xmind_name, 'w')
    for d in os.listdir("./zip_need"):
        z.write("./zip_need" + os.sep + d, d)
    z.close()
    #print(json_str)
