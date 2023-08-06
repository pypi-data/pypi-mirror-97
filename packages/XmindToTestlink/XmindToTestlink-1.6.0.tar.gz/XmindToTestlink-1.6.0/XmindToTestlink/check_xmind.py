from __future__ import unicode_literals
import zipfile
import os
import sys
import re
import codecs
import json
import argparse
try:
    from XmindToTestlink import xmind_to_dict
except ImportError:
    import xmind_to_dict

register_list = []
reg_conf_list = []
other_conf_list = []

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

def get_suite_case_path_list(path_list):
    suite_path_list = []
    case_path_list = []
    for path in path_list:
        if path.find('cases') >= 0:
            case_path_list.append(path)
        else:
            suite_path_list.append(path)
    return suite_path_list,case_path_list

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

def transfer_path(in_dict, dpath):
    path = dpath.strip('/').split('/')
    cnpath = ''
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
            cnpath += eval("in_dict" + msg)['title'] + "/"
        else:
            msg += "[\'"  + i + "\']"
    return cnpath.strip("/").replace("：", ':')
    #return '/'.join(cnpath.split('/')[1:])

def check_reg(reg_conf):
    #print("reg_conf: " + reg_conf)
    global register_list
    global reg_conf_list
    global other_conf_list
    find = 0

    for reg in register_list:
        if reg.endswith(reg_conf):
            find = 1
            reg_conf_list.append(reg)
            register_list.remove(reg)
            break
    if not find:
        for creg in reg_conf_list:
            if creg.endswith(reg_conf):
                find = 1
                break
    if not find:
        other_conf_list.append(reg_conf)


def check_xmind(xmind_file = '', is_module = 0):
    show_conf = False
    if not is_module:
        parser = argparse.ArgumentParser(description = "") 
        parser.add_argument('-f', '--file', dest='file', metavar='File', nargs="+", \
                required = True, help='file')
        parser.add_argument('-c', '--conf', dest='show_conf', action='store_const', const = True, \
                default = False, help='按照conf格式显示')
        args = parser.parse_args()
        #print(args)
        test_file_list = args.file
        show_conf = args.show_conf

        xmind_file = test_file_list[0]
    xmind_type = "checkxmind"

    xd = xmind_to_dict.XmindToDict(xmind_type)
    root_dict, register_dict = xd.get_register_msg(xmind_file)
    path_list = get_dpath(register_dict)
    suite_path_list, case_path_list = get_suite_case_path_list(path_list)
    global register_list
    global reg_conf_list
    global other_conf_list
    no_case_req = []
    #print(root_dict)

    for i in case_path_list:
        register_list.append(transfer_path(register_dict, i))
    #for rr in register_list:
    #    print(rr)
    path_list = get_dpath(root_dict)
    suite_path_list, case_path_list = get_suite_case_path_list(path_list)
    for i in suite_path_list:
        case_summary = get_delem(root_dict, i, key = "detail")
        lines = case_summary.split('\n')
        for line in lines:
            if line.find("reg_conf") >= 0:
                b = [substr.start() for substr in re.finditer(']', line)]
                print(line)
                print(b)
                reg_conf = line[:b[-1]].replace(" ",'').replace("：",":").split("reg_conf:[")[1]
                #print(reg_conf)
                check_reg(reg_conf)
    for i in case_path_list:
        cn_path = transfer_path(root_dict, i)
        if cn_path.find("用例") <= 0:
            no_case_req.append(cn_path)
        case_summary = get_delem(root_dict, i, key = "summary")
        lines = case_summary.split('\n')
        for line in lines:
            if line.find("reg_conf") >= 0:
                b = [substr.start() for substr in re.finditer(']', line)]
                reg_conf = line[:b[-1]].replace(" ",'').replace("：",":").split("reg_conf:[")[1]
                #print(reg_conf)
                check_reg(reg_conf)

    if len(register_list) > 0:
        print("\nXmind_file: " + xmind_file)
        print('\033[1;31m%s: \033[0m'%"下列寄存器未配置")
        if not show_conf:
            for i in register_list:
                print("\t" + i)
        else:
            register_list.sort()
            for i in register_list:
                show = '/'.join(i.split('/')[2:])
                print("\treg_conf:[" + show + "]")
    if len(other_conf_list) > 0:
        print("\nXmind_file: " + xmind_file)
        print('\033[1;33m%s: \033[0m'%"下列配置不在寄存器中")
        for i in other_conf_list:
            print("\t" + i)
    if len(no_case_req) > 0:
        print("\nXmind_file: " + xmind_file)
        print('\033[1;31m%s: \033[0m'%"下列需求没有用例")
        for i in no_case_req:
            print("\t" + i)
    #for ff in reg_conf_list:
    #    print(ff)
    print("")

if __name__ == "__main__":
    check_xmind()
