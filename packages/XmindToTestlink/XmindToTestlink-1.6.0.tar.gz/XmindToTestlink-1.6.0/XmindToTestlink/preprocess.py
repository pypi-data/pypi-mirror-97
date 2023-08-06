# -*- coding: utf-8 -*-

import json
from zipfile import  ZipFile
import copy

class PreProcess(object):
    def __init__(self):
        pass

    def open_xmind(self, file_path):
        '''
        打开xmind文件，返回其中的内容
        '''
        target_file = "content.json"
        with ZipFile(file_path) as xmind:
            for f in xmind.namelist():
                if f == target_file:
                    return (xmind.open(f).read().decode('utf-8'))

    def get_rules(self, branch):
        rules = []
        if "notes" in branch.keys():
            summery = branch["notes"]["plain"]["content"].split('\n')
            tmp = []
            for msg in summery:
                if msg.find("xmindrepeat:") >= 0:
                    scope = msg.replace("xmindrepeat:", "")
                    if scope.find("(") >= 0:
                        rules.append({"range":scope})
                    if scope.find("[") >= 0:
                        rules.append({"list":scope})
                else:
                    tmp.append(msg)
            branch["notes"]["plain"]["content"] = "\n".join(tmp)
        if rules == []:
            return 0
        else:
            return rules

    def use_rule(self, rule, attach, branch, rules, summary):
        argv = branch['title']
        if "list" in rule:
            msg = rule['list']
            target = msg.split("=")
            if target[0].find("[") >= 0:
                scope = target[0].strip(" []").split(",")
            else:
                scope = target[1].strip(" []").split(",")
                argv = target[0]
            for k in scope:
                case_msg = (argv + "=" +  str(k)).replace(' ','')
                branch['title'] = "xmindrepeat-" + case_msg
                branch["notes"]["plain"]["content"] = case_msg + "\n" + summary
                attach.append(copy.deepcopy(branch))
                tmp_rules = copy.copy(rules)
                if tmp_rules != []:
                    next_rule = tmp_rules.pop(0)
                    tmp_smy = copy.copy(summary)
                    if 'children' not in branch or branch['children'] == {}:
                        attach[-1]['children'] = {"attached":[]}
                    new_attach = attach[-1]['children']['attached']
                    self.use_rule(next_rule, new_attach, branch, tmp_rules,\
                            case_msg + "\n"+ tmp_smy)
        if "range" in rule:
            target = rule['range'].split("=")
            if target[0].find("(") >= 0:
                msg = target[0].strip(" ()").split(",")
            else:
                msg = target[1].strip(" ()").split(",")
                argv = target[0]
            start = int(msg[0])
            end = int(msg[1]) + 1
            for k in range(start, end):
                case_msg = (argv + "=" +  str(k)).replace(' ','')
                branch['title'] = "xmindrepeat-" + case_msg
                branch["notes"]["plain"]["content"] = case_msg + "\n" + summary
                attach.append(copy.deepcopy(branch))
                tmp_rules = copy.copy(rules)
                if tmp_rules != []:
                    next_rule = tmp_rules.pop(0)
                    tmp_smy = copy.copy(summary)
                    if 'children' not in branch or branch['children'] == {}:
                        attach[-1]['children'] = {"attached":[]}
                    new_attach = attach[-1]['children']['attached']
                    self.use_rule(next_rule, new_attach, branch, tmp_rules, \
                            case_msg + "\n"+ tmp_smy)

    def run_process(self, attach):
        new_attach = []
        for branch in attach :
            if "children" in branch and branch['children'] != {}:
                branch['children']['attached'] = \
                        self.run_process(branch['children']['attached'])
            rules =  self.get_rules(branch)
            if rules != 0:
                rule = rules.pop(0)
                #print(rule)
                summary = copy.copy(branch["notes"]["plain"]["content"])
                self.use_rule(rule, new_attach, branch, rules, summary)
                #self.use_rule(rule, new_attach, branch, rules)
            else:
                new_attach.append(branch)
        return new_attach

    def start(self, xmind_file):
        js_str = str(self.open_xmind(xmind_file)).replace(' ', '')
        js_dict = json.loads(js_str)
        js_dict[0]['rootTopic']['children']['attached'] = \
                self.run_process(js_dict[0]['rootTopic']['children']['attached'])
        return js_dict

if __name__ == "__main__":
    pp = PreProcess()
    #(pp.start('repeatdemo.xmind'))
    (pp.start('multi.xmind'))
    #js_file = "content.json"
    #with open(js_file) as jf:
    #    js_dict = json.load(jf)
    #xd = XmindToDict()
    #root_dict = {}
    #root_name = xd.get_root(js_dict)
    #root = xd.create_suite(root_name)
    #xd.get_req_dict(js_dict[0]['rootTopic'],root)
    #print(root['suites'][0])
