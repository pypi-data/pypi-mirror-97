# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
import hashlib
import sys
try:
    from XmindToTestlink import read_xml
except ImportError:
    import read_xml

class DictToXml(object):
    def __init__(self):
        self.update = 0
        self.case_tag = {
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
                "val":"value"
            }
        self.req_tag = {
                "root":"requirement-specification",
                "rqs":"req_spec",
                "rq":"requirement",
                "id":"docid",
                "title":"title",
                "cfs":"custom_fields",
                "cf":"custom_field",
                "nm":"name",
                "val":"value",
                "dt":"scope",
                "sm":"description",
                "reqs":"requirements",
                "rst":"req_spec_title",
                "did":"doc_id",
                "rqt":"title"
                }

    def get_md5(self, src):
        md5_create = hashlib.md5()
        md5_create.update(src.encode('utf-8'))
        return md5_create.hexdigest()

    def cdata(self, element, content):
        '''
        添加xml中的cdata标签
        '''
        #if isinstance(content, int):
        #    element.text = str(content)
        #elif content:
        #    content = content.replace("\n", "<br />")  # replace new line for *nix system
        #    #element.append(ET.Comment(' --><![CDATA[<p>' + content + '</p>]]><!-- '))
        #    element.append(ET.Comment(' --><![CDATA[' + content + ']]><!-- '))
        if isinstance(content, int):
            content = str(content)
        content = content.replace("\n", "<br />")  # replace new line for *nix system
        element.append(ET.Comment(' --><![CDATA[' + content + ']]><!-- '))
    
    
    def indent(self, elem, level=0):
        '''
        添加xml文件的换行符,增强可读性
        '''
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def get_case_req_xml(self, case_list, node, auto_id, root_id, \
            pre_path='', id_count=1):
        '''
        解析输入字典，按照需求格式,生成xml
        '''
        for case in case_list:
            if auto_id:
                path = pre_path + '/' + case['title']
                req_id = self.get_md5(path)
            else:
                req_id = root_id
            tc = ET.SubElement(node, self.req_tag['rq'])            
            tt = ET.SubElement(tc, self.req_tag['title'])
            self.cdata(tt, case['title'])
            rid = ET.SubElement(tc, self.req_tag['id'])
            self.cdata(rid, req_id)
            if case[self.case_tag['sm']] != '':
                sm = ET.SubElement(tc, self.req_tag['sm'])
                self.cdata(sm, case[self.case_tag['sm']])
            if case[self.req_tag['cf']] != '':
                cfs = ET.SubElement(tc, self.req_tag['cfs'])
                for custom_field in  case[self.req_tag['cf']]:
                    cf = ET.SubElement(cfs, self.req_tag['cf'])
                    for k,v in custom_field.items():
                        nm = ET.SubElement(cf, self.req_tag['nm'])
                        self.cdata(nm, k)
                        val = ET.SubElement(cf, self.req_tag['val'])
                        self.cdata(val, v)

    def get_req_xml(self, in_dict, node, auto_id, root_id, \
            pre_path='', id_count=1, chipcase = ''):
        '''
        解析输入字典，按照需求格式,生成xml
        '''
        if "title" in in_dict.keys():
            #添加需求规约
            if auto_id:
                path = pre_path + '/' + in_dict['title']
                tmp_path = path
                reqs_id = self.get_md5(path)
            #elif self.update:
            #    path = pre_path + '/' + in_dict['title']
            #    tmp_path = path
            #    if path in self.id_dict:
            #        reqs_id = self.id_dict[path]
            #    else:
            #        pre_suite = "/".join(path.split("/")[:-1])
            #        if pre_suite in self.suite_id:
            #            id_msg = self.suite_id[pre_suite].split(".")
            #            reqs_id = ".".join(id_msg[:-1]) + "." + str(int(id_msg[-1]) + 1)
            #            self.suite_id[path] = reqs_id + ".0"
            #            #self.suite_id[pre_path] = reqs_id
            #    print(path, self.suite_id[path])
            else:
                reqs_id = root_id
            if chipcase:
                if in_dict['title'] == '模块测试' or in_dict['title'] == '功能测试':
                    replace_title = in_dict['title'].replace('测试', '特性')
                    #ts = ET.SubElement(node, self.req_tag['rqs'], attrib = {"title" : replace_title, "doc_id" :reqs_id})
                    ts = ET.SubElement(node, self.req_tag['rqs'], attrib = {"title" : in_dict['title'], "doc_id" :reqs_id})
                else:
                    ts = ET.SubElement(node, self.req_tag['rqs'], attrib = {"title" : in_dict['title'], "doc_id" :reqs_id})
            else:
                ts = ET.SubElement(node, self.req_tag['rqs'], attrib = {"title" : in_dict['title'], "doc_id" :reqs_id})
            if reqs_id.startswith('<'):
                reqs_id = reqs_id.strip('<>')
            if "detail" in in_dict.keys() and in_dict['detail'] != '':
                dt = ET.SubElement(ts, self.req_tag['dt'])
                self.cdata(dt, in_dict['detail'])
        if "cases" in in_dict.keys() and in_dict['cases'] != []:
            #添加需求
            for case in in_dict['cases']:
                if auto_id:
                    path = tmp_path + '/' + case['title']
                    req_id = self.get_md5(path)
                elif self.update:
                    path = tmp_path + '/' + case['title']
                    if path in self.id_dict:
                        req_id = self.id_dict[path]
                    else:
                        pre_suite = "/".join(path.split("/")[:-1])
                        if pre_suite in self.suite_id:
                            id_msg = self.suite_id[pre_suite].split(".")
                            req_id = ".".join(id_msg[:-1]) + "." + str(int(id_msg[-1]) + 1)
                            self.suite_id[pre_suite] = req_id
                        else:
                            pass
                else:
                    req_id = reqs_id + "." +  str(id_count)
                    id_count += 1
                tc = ET.SubElement(ts, self.req_tag['rq'])            
                tt = ET.SubElement(tc, self.req_tag['title'])
                self.cdata(tt, case['title'])
                rid = ET.SubElement(tc, self.req_tag['id'])
                self.cdata(rid, req_id)
                if case[self.case_tag['sm']] != '':
                    sm = ET.SubElement(tc, self.req_tag['sm'])
                    self.cdata(sm, case[self.case_tag['sm']])
                if case[self.req_tag['cf']] != '':
                    cfs = ET.SubElement(tc, self.req_tag['cfs'])
                    for custom_field in  case[self.req_tag['cf']]:
                        cf = ET.SubElement(cfs, self.req_tag['cf'])
                        for k,v in custom_field.items():
                            nm = ET.SubElement(cf, self.req_tag['nm'])
                            self.cdata(nm, k)
                            val = ET.SubElement(cf, self.req_tag['val'])
                            self.cdata(val, v)
        if "suites" in in_dict.keys() and in_dict['suites'] != []:
            #递归，遍历嵌套的需求规约
            for suite in in_dict['suites']:
                if suite['title'] == "xminddelete":
                    continue
                if auto_id:
                    path = pre_path + '/' + in_dict['title']
                    self.get_req_xml(suite, ts, auto_id, root_id, path)
                #elif self.update:
                #    path = pre_path + '/' + in_dict['title']
                #    if path in self.id_dict:
                #        root_id = self.id_dict[path]
                #    else:
                #        pre_suite = "/".join(path.split("/")[:-1])
                #        if pre_suite in self.suite_id:
                #            id_msg = self.suite_id[pre_suite].split(".")
                #            req_id = ".".join(id_msg[:-1]) + "." + str(int(id_msg[-1]) + 1)
                #            self.suite_id[path] = req_id + ".1"
                #    self.get_req_xml(suite, ts, auto_id, root_id, path)
                else:
                    root_id = reqs_id + "." + str(id_count)
                    id_count += 1
                    self.get_req_xml(suite, ts, auto_id, root_id, chipcase = chipcase)

    def get_suite_id(self, id_dict):
        suite_id = {}
        for path, pid in id_dict.items():
            if path in self.only_reqs_id_dict:
                if path not in suite_id:
                    suite_id[path] = pid + ".0"
                elif pid.split(".")[-1].isdigit():
                    old_count = int(suite_id[path].split(".")[-1])
                    now_count = int(pid.split(".")[-1])
                    if old_count < now_count:
                        suite_id[path] = pid
            msg = path.split('/')
            pre_path = "/".join(msg[:-1])
            if pre_path in id_dict:
                if pre_path not in suite_id:
                    suite_id[pre_path] = pid
                else:
                    old_count = int(suite_id[pre_path].split(".")[-1])
                    now_count = int(pid.split(".")[-1])
                    if old_count < now_count:
                        suite_id[pre_path] = pid
        return suite_id

    def enable_update(self):
        self.update = 1

    def read_req_id_dict(self, req_xml_path, update=''):
        #update参数，给xml_update用的
        if update == 'update':
            self.id_dict = read_xml.read_req_id_xml(req_xml_path, skip_first_leval = 0)
            self.only_reqs_id_dict = read_xml.read_only_reqs_id_xml(req_xml_path)
            self.suite_id = self.get_suite_id(self.id_dict)
        else:
            self.id_dict = read_xml.read_req_id_xml(req_xml_path, skip_first_leval = 1)
        #print(self.id_dict)
    
    def get_case_xml(self, in_dict, node = '', api = False, argv = '',\
            auto_id=True, name='', sms = '', chipcase = ''):
        '''
        解析输入字典，按照用例格式，生成xml
        '''
        if "title" in in_dict.keys():
            if chipcase:
                in_dict['title'] = in_dict['title'].replace('支持', '测试')
            #添加测试集
            if api == True:
                argv += "<li>" + in_dict['title'] + "</li>"
            ts = ET.SubElement(node, self.case_tag['ts'], attrib = {"name" : in_dict['title']})
            if "detail" in in_dict.keys() and in_dict['detail'] != '':
                if api == True:
                    sms += in_dict['detail'] + '\n'
                dt = ET.SubElement(ts, self.case_tag['dt'])
                self.cdata(dt, in_dict['detail'])
        if "cases" in in_dict.keys() and in_dict['cases'] != []:
            for case in in_dict['cases']:
                #添加测试用例
                if chipcase:
                    case['title'] = case['title'].replace('支持', '测试')
                tc = ET.SubElement(ts, self.case_tag['tc'], attrib = {"name":case['title']})            
                sm = ET.SubElement(tc, self.case_tag['sm'])
                msg = ''
                need_notes = 0
                if case[self.case_tag['pc']] != '':
                    #添加前提
                    pc = ET.SubElement(tc, self.case_tag['pc'])
                    self.cdata(pc, case[self.case_tag['pc']])
                if case[self.case_tag['sm']] != '' or api == True:
                    #添加摘要
                    #sm = ET.SubElement(tc, self.case_tag['sm'])
                    msg = case[self.case_tag['sm']]
                    if api == True:
                        final_argv = case['title'].split("~")[-1]
                        #case_argv = argv + "<li>" + case['title'] + "</li>"
                        case_argv = argv + "<li>" + final_argv + "</li>"
                        msg = sms + msg + "\n\n参数设置: \n" + "<ul>" + case_argv + "</ul>"
                    need_notes = 1
                    #self.cdata(sm, msg)
                if case[self.case_tag['ip']] != '':
                    #添加优先级
                    ip = ET.SubElement(tc, self.case_tag['ip'])
                    self.cdata(ip, case[self.case_tag['ip']])
                if case[self.case_tag['et']] != '':
                    #添加执行方式
                    et = ET.SubElement(tc, self.case_tag['et'])
                    self.cdata(et, case[self.case_tag['et']])
                if case[self.case_tag['st']] != '':
                    #添加步骤
                    sts = ET.SubElement(tc, self.case_tag['sts'])
                    for n in range(len(case[self.case_tag['st']])):
                        step = case[self.case_tag['st']][n]
                        st = ET.SubElement(sts, self.case_tag['st'])
                        #for k,v in step.items():
                        sn = ET.SubElement(st, self.case_tag['sn'])
                        self.cdata(sn,n+1)
                        ac = ET.SubElement(st, self.case_tag['ac'])
                        self.cdata(ac,step['action'])
                        ep = ET.SubElement(st, self.case_tag['ep'])
                        self.cdata(ep,step['expect'])
                        et = ET.SubElement(st, self.case_tag['et'])
                        self.cdata(et,2)
                        #if 'notes' in step and step['notes'] != '':
                        #    msg += "\n步骤" + str(n + 1) + ": " + step['notes']
                        #    need_notes = 1
                if need_notes == 1:
                    self.cdata(sm, msg)
                if case[self.case_tag['cf']] != '':
                    #添加自定义字段
                    cfs = ET.SubElement(tc, self.case_tag['cfs'])
                    for custom_field in  case[self.case_tag['cf']]:
                        cf = ET.SubElement(cfs, self.case_tag['cf'])
                        for k,v in custom_field.items():
                            if k == "绑定":
                                pass
                            nm = ET.SubElement(cf, self.case_tag['nm'])
                            self.cdata(nm, k)
                            val = ET.SubElement(cf, self.case_tag['val'])
                            self.cdata(val, v)
                if 'reqband' in case and case['reqband'] != '' and self.update == 0:
                    #绑定需求
                    reqs = ET.SubElement(tc, self.req_tag['reqs'])
                    for k,v in case['reqband'].items():
                        if auto_id:
                            doc_id = self.get_md5("/" + k)
                        else:
                            try:
                                if name != '':
                                    if chipcase:
                                        doc_id = self.id_dict["/" + k]
                                    else: 
                                        doc_id = self.id_dict["/" + name + "/" + k]
                                else:
                                    doc_id = self.id_dict["/" + k]
                            except:
                                print(self.id_dict)
                                print("/" + k)
                                sys.exit()
                        #if v == "":
                        #    v = self.id_dict['root_req_spec']
                        #rst = ET.SubElement(req, self.req_tag['rst'])
                        #self.cdata(rst, v)
                        req = ET.SubElement(reqs, self.req_tag['rq'])
                        did = ET.SubElement(req, self.req_tag['did'])
                        self.cdata(did, doc_id)
                        rqt = ET.SubElement(req, self.req_tag['rqt'])
                        self.cdata(rqt, k.split('/')[-1])
                if 'old_band' in case and self.update == 1:
                    # xml_update 使用
                    reqs = ET.SubElement(tc, self.req_tag['reqs'])
                    for old_req in  case["old_band"]:
                        req = ET.SubElement(reqs, self.req_tag['rq'])
                        for k,v in old_req.items():
                            did = ET.SubElement(req, self.req_tag['did'])
                            self.cdata(did, k)
                            rqt = ET.SubElement(req, self.req_tag['rqt'])
                            self.cdata(rqt, v)

        if "suites" in in_dict.keys() and in_dict['suites'] != []:
            #递归，遍历嵌套的测试集
            for suite in in_dict['suites']:
                if suite['title'] == "xminddelete":
                    continue
                self.get_case_xml(suite, ts, api, argv, auto_id, name, sms, chipcase)
