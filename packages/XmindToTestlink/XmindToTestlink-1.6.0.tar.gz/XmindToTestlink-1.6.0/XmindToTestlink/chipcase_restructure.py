import os
import copy
#import save_dict

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
    return cnpath

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

def get_father_delem(in_dict, dpath, key = ''):
    path = dpath.strip('/').split('/')
    path = dpath.strip('/').split('/')[:-2]
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
        else:
            msg += "[\'"  + i + "\']"
    if key != '':
        msg += "[\'"  + key + "\']"
    return eval("in_dict" + msg)

def delete_delem(in_dict, dpath):
    path = dpath.strip('/').split('/')
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
        else:
            msg += "[\'"  + i + "\']"
    #eval("in_dict" + msg + "['title'] = 'xminddelete'")
    eval("in_dict" + msg[:-3] + ".remove(in_dict" + msg + ")")

def get_suite_case_path_list(path_list):
    suite_path_list = []
    case_path_list = []
    for path in path_list:
        if path.find('cases') >= 0:
            case_path_list.append(path)
        else:
            suite_path_list.append(path)
    return suite_path_list,case_path_list

def select_case_type(in_dict, case_type, all_branch_list):
    new_dict = copy.deepcopy(in_dict)
    type_branch_list = all_branch_list[case_type]
    for br in type_branch_list:
        branch = get_delem(in_dict, br)
        father_branch = get_father_delem(new_dict, br)
        father_branch['cases'].extend(branch['cases'])
        father_branch['suites'].extend(branch['suites'])
    for t in all_branch_list:
        for old_br in all_branch_list[t]:
            new_elem = get_delem(new_dict, old_br)
            new_elem['title'] = "xminddelete"
    return new_dict


def restructure_dict(in_dict):
    #in_dict = save_dict.dict1
    dpath = get_dpath(in_dict)
    case_type = {}
    suite_path_list,case_path_list = get_suite_case_path_list(dpath)
    for i in suite_path_list:
        stitle = get_delem(in_dict, i, key = 'title')
        if stitle.endswith("用例") and stitle != "用例":
            if stitle not in case_type :
                case_type[stitle] = []
                case_type[stitle].append(i)
            else:
                case_type[stitle].append(i)
            #print(stitle)
    
    root = copy.deepcopy(in_dict)
    root['suites'][0]['suites'][0]['suites'] = []
    #root['suites'][0]['suites'].append({
    #    'title':'功能特性',
    #    'detail':'',
    #    'suites':[],
    #    'cases':[]
    #    })
    #print(case_type)
    for br in range(len(root['suites'][0]['suites'])):
        if root['suites'][0]['suites'][br]['title'] == '系统测试':
            continue
        root['suites'][0]['suites'][br]['suites'] = []
        for t in case_type:
            new_dict = select_case_type(in_dict, t, case_type)
            root['suites'][0]['suites'][br]['suites'].append({
                'title':t,
                'detail':'',
                'suites':[],
                'cases':[]
                })
            root['suites'][0]['suites'][br]['suites'][-1]['suites'].extend(new_dict['suites'][0]['suites'][br]['suites'])
            root['suites'][0]['suites'][br]['suites'][-1]['cases'].extend(new_dict['suites'][0]['suites'][br]['cases'])
    return root
