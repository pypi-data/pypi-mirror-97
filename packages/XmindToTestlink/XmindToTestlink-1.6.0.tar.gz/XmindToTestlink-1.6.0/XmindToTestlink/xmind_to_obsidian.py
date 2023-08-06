import os
import sys
import json
import copy
try:
    from XmindToTestlink import xmind_to_dict
    from XmindToTestlink import preprocess
    from XmindToTestlink import css
except ImportError:
    import xmind_to_dict
    import preprocess
    import css

#xmind_file = 'file/ACPU_MTC.xmind'
print(sys.argv[2])
xmind_file = sys.argv[2]

pp = preprocess.PreProcess()
xd = xmind_to_dict.XmindToDict()
js_dict = pp.start(xmind_file)
root_name = xd.get_root(js_dict)
root = xd.create_suite(root_name)



obs_output = 'obs/'

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

def get_path_title(in_dict, path_list):
    path_key = {}
    for dpath in path_list:
        path_key[dpath] = get_delem(in_dict, dpath, 'title')
    return path_key

def transfer_path(in_dict, dpath):
    path = dpath.strip('/').split('/')
    cnpath = ''
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
            cnpath += eval("in_dict" + msg)['title'] + "||"
        else:
            msg += "[\'"  + i + "\']"
    return cnpath

def create_path(path):
    #path = path.replace('(','\(').replace(')','\)')
    if os.path.exists(path):
        pass
    else:
        os.system('mkdir -p "' + path + '"')
        #os.system('mkdir -p ' + path)

def create_register(r_dict):
    dpath_list = get_dpath(r_dict)
    suite_path_list, case_path_list = get_suite_case_path_list(dpath_list)
    reg_writed = []
    list_writed = []
    reg_dict = {}
    for i in case_path_list:
        cn_path = transfer_path(r_dict, i)
        tmp = cn_path.strip('||').split('||')
        if len(tmp) == 4:
            create_path(obs_output + '/'.join(tmp[0:2]))
            if 1:
                list_file = obs_output + '/'.join(tmp[0:3]) + '.md'
                #print(list_file)
                os.system('echo "## ' + tmp[3] + '" >> "' + list_file + '"')
                reg_writed.append(tmp[3])
            if tmp[1] not in reg_writed:
                list_file = obs_output + '/'.join(tmp[0:2]) + '/' + tmp[1] + '.md'
                os.system('echo "- [[' + tmp[2] + ']]" >> "' + list_file + '"')
                reg_writed.append(tmp[1])
                reg_dict[tmp[1]] = []
            else:
                if tmp[2] not in reg_dict[tmp[1]]:
                    list_file = obs_output + '/'.join(tmp[0:2]) + '/' + tmp[1] + '.md'
                    os.system('echo "- [[' + tmp[2] + ']]" >> "' + list_file + '"')
                    reg_dict[tmp[1]].append(tmp[2])
        if len(tmp) == 2:
            create_path(obs_output + tmp[0])
            reg = get_delem(r_dict, i)
            os.system('echo "' + reg['summary'] + '" > "' + obs_output + '/'.join(tmp) + '.md"')
        if tmp[1] not in list_writed:
            list_file = obs_output + tmp[0] + '/regslist.md'
            os.system('echo "- [[' + tmp[1] + ']]" >> "' + list_file + '"') 
            list_writed.append(tmp[1])

def create_req(req_dict):
    tmp_dpath_list = get_dpath(req_dict)
    dpath_list = []
    req_writed = []
    for i in tmp_dpath_list:
        cn_path = transfer_path(req_dict, i)
        if cn_path.startswith('模块测试||') or cn_path.startswith('功能测试||'):
            dpath_list.append(i)
    suite_path_list, case_path_list = get_suite_case_path_list(dpath_list)
    for i in case_path_list:
        cn_path = transfer_path(req_dict, i)
        tmp = cn_path.strip('||').split('||')
        create_path(obs_output + '/'.join(tmp[:-1]))
        req_file = obs_output + '/'.join(tmp[:-1]) + '/feature_' + tmp[-1] + '.md'
        fd = open(req_file, 'w')
        req = get_delem(req_dict, i)
        tmp_summary = req['summary'].strip('\n').split('\n')
        for s in tmp_summary:
            if s.startswith('reg_conf:'):
                tmp_s = s[10:-1].split('/')
                if len(tmp_s) >= 2:
                    reg_format = "#".join(tmp_s[-2:])
                    fd.write('  [[' + reg_format + ']]' + '\n')
                else:
                    fd.write('  [[' + s[10:-1] + ']]' + '\n')
            else:
                fd.write('  ' + s + '\n')
        if len(tmp) >= 3:
            list_file = obs_output + '/'.join(tmp[:-1]) + '/' + tmp[-2] + '.md'
            os.system('echo "    - [[feature_' + tmp[-1] + ']]" >> "' + list_file + '"')

        if tmp[-1] not in req_writed:
            list_file = obs_output + tmp[0] + '/featureslist.md'
            if tmp[1] not in req_writed:
                os.system('echo "### ' + tmp[1] + '" >> ' + list_file)
                req_writed.append(tmp[1])
            for j in range(len(tmp[2:-1])):
                if tmp[j+2] not in req_writed:
                    os.system('echo "' + '  '*(j+1) + '- ' + tmp[j+2] + '" >> ' + list_file)
                    req_writed.append(tmp[j+2])
        os.system('echo "' + '  '*(len(tmp[2:-1]) + 1) + '- [[feature_' + tmp[-1] + ']]" >> "' \
                + list_file + '"')

        

def create_case(case_dict):
    dpath_list = get_dpath(case_dict)
    suite_path_list, case_path_list = get_suite_case_path_list(dpath_list)
    case_writed = []
    for i in case_path_list:
        cn_path = transfer_path(case_dict, i)
        case_type = cn_path.split('||')[0] #模块测试 or 功能测试
        if cn_path.find('||全功能测试||') >= 0:
            continue
        if not cn_path.find('||用例||') >= 0:
            continue
        case = get_delem(case_dict, i)
        create_path(obs_output + '/用例/' + case_type)
        tmp = cn_path.strip('||').split('||')
        case_file = obs_output + '/用例/' + case_type + '/' + 'case_' + tmp[-4] + '_' + \
                tmp[-2].strip('用例') + tmp[-1] + '.md'
        fd = open(case_file, 'w')
        fd.write('[[feature_'+tmp[-4] + ']]\n')
        for step in case['step']:
            fd.write('- ' + step['action'] + '\n')
            if 'notes' in step and step['notes'] != '':
                tmp_note = step['notes'].strip('\n').split('\n')
                for t in tmp_note:
                    if t.startswith('reg_conf:'):
                        tmp_t = t[10:-1].split('/')
                        if len(tmp_t) >= 2:
                            reg_format = "#".join(tmp_t[-2:])
                            fd.write('[[' + reg_format + ']]' + '\n')
                        else:
                            fd.write('[[' + t[10:-1] + ']]' + '\n')
                    else:
                            fd.write(t + '\n')
        fd.close()

        list_file = obs_output + '用例/' + case_type + '/caseslist.md'
        if tmp[1] not in case_writed:
            os.system('echo "### ' + tmp[1] + '" >> ' + list_file)
            case_writed.append(tmp[1])
        for j in range(len(tmp[2:-4])):
            if tmp[j+2] not in case_writed:
                os.system('echo "' + ' '*j + '- ' + tmp[j+2] + '" >> "' + list_file + '"')
                case_writed.append(tmp[j+2])
        os.system('echo "' + ' '*(len(tmp[2:-1])) + '- [[case_' + tmp[-4] + '_' + \
                tmp[-2].strip('用例') + tmp[-1] + ']]" >> "' + list_file + '"')

def create_css():
    with open('obs/obsidian.css', 'w') as fd:
        fd.write(css.css)

def main():
    r_dict = copy.deepcopy(root)
    req_dict = copy.deepcopy(root)
    case_dict = copy.deepcopy(root)
    dict1 = copy.deepcopy(root)
    dict2 = copy.deepcopy(root)
    have_function = 0
    
    xd.get_branch_dict(js_dict[0]['rootTopic'], r_dict,'register')
    r_dict = r_dict['suites'][0]
    
    xd.get_req_dict(js_dict[0]['rootTopic'], req_dict)
    req_dict = req_dict['suites'][0]
    
    xd.get_branch_dict(js_dict[0]['rootTopic'], dict1,'模块测试')
    case_dict = dict1['suites'][0]
    xd.get_branch_dict(js_dict[0]['rootTopic'], dict2,'功能测试')
    if dict2['suites'][0]['suites'] != []:
        have_function = 1
        case_dict['suites'].append(dict2['suites'][0]['suites'][0])

    create_register(r_dict)
    create_req(req_dict)
    create_case(case_dict)
    create_css()
    if have_function:
        os.system('mkdir -p obs/特性')
        os.system('mv obs/模块测试 obs/特性/模块特性')
        os.system('mv obs/功能测试 obs/特性/功能特性')
    else:
        os.system('mv obs/模块测试 obs/特性')
    os.system('mv obs/register obs/配置')

if __name__ == "__main__":
    main()
