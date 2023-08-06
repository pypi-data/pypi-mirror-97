# *** Tree representation ***
class Node(object):
    def __init__(self, title):
        self.title = title
        self.parent = None
        self.children = []
        self.detail = ''

    def add(self, child):
        self.children.append(child)
        child.parent = self

# *** Node insertion logic ***
class Inserter(object):
    def __init__(self, node, depth = 0):
        self.node = node
        self.depth = depth

    def __call__(self, title, depth):
        if depth == -2:
            self.node.detail = self.node.detail + title + "\n"
        else:
            newNode = Node(title)
            if (depth > self.depth):
                self.node.add(newNode)
                self.depth = depth
            elif (depth == self.depth):
                self.node.parent.add(newNode)
            else:
                parent = self.node.parent
                for i in range(0, self.depth - depth):
                    parent = parent.parent
                parent.add(newNode)
                self.depth = depth

            self.node = newNode

class MarkdownToDict(object):
    def __init__(self):
        pass

    def get_count(self, line):
        if line.lstrip('* ')[0] == ">":
            title = line[line.find(">")+2:]
            #print(title)
            return -2, title
        if line[0] == "#":
            num = line.split(' ')[0].count('#')
            title = line[line.find(' ')+1:]
        elif line[0] != ' ' and line[0] != "*":
            return '',''
        else:
            if line.find("* ") < 0:
                return 'add', line
            else:
                num = line.split('* ')[0].count(' ')/4 + 4
                title = line[line.find("* ")+2:]
        return int(num), title

    def get_tree_node(self, md_file):
        tree = Node("root")
        inserter = Inserter(tree, -1)
        end_line = "*XMind: ZEN - Trial Version*"
        
        fd = open(md_file,'r')
        last_title = ''
        last_tabs = 'init'
        while True:
            line = fd.readline()
            #print(line)
            if not line: 
                break
            line = line.strip('\n')
            if line == end_line:
                break
            if line == '':
                continue
            tabs, title = self.get_count(line)
            if tabs == '':
                continue
            if tabs == 'add':
                #print(11111111)
                last_title += '\n' + title
            else:
                if last_tabs != 'init':
                    #print(last_title, last_tabs)
                    inserter(last_title, last_tabs)
                last_title = title
                last_tabs = tabs
        fd.close()
        return tree

    def create_suite(self, name, suite_detail = ''):
        suite = { 
                'title':'',
                'detail':'',
                'suites':[],
                'cases':[]
                }
        suite['title'] = name
        suite['detail'] = suite_detail
        return suite

    def get_custom_fields(self, node):
        customs = []
        for child in node.children:
            custom = {}
            if child.children != []:
                custom[child.title] = child.children[0].title
            else:
                custom[child.title] = ''
            customs.append(custom)
        #print(customs)
        return customs

    def get_steps(self, node):
        steps = []
        for child in node.children:
            step = {}
            if child.children != []:
                step[child.title] = child.children[0].title
            else:
                step[child.title] = ''
            steps.append(step)
        #print(steps)
        return steps
    
    def create_case(self, node):
        case = { 
                'title':'',
                'summary':'',
                'preconditions':'',
                'importance':'',
                'execution_type':2,
                'custom_field':'',
                'step':'',
                'reqband':''
                }
        case['title'] = node.title
        case['summary'] = node.detail
        if node.children != []:
            for child in node.children:
                if child.title == "属性":
                    case['custom_field'] = self.get_custom_fields(child)
                elif child.title == "步骤":
                    case['step'] = self.get_steps(child)
        return case

    def is_case(self, node):
        case = 0
        for child in node.children:
            if child.title != "属性" and child.title != "步骤":
                case = 0
                break
            else:
                case = 1
        return case
    
    def check_suite_or_case(self, node):
        if node.children == [] or self.is_case(node):
            return "case"
        else:
            return "suite"

    def get_dict(self, node, out_dict):
        sc = self.check_suite_or_case(node)
        if sc == "case":
            case = self.create_case(node)
            out_dict['cases'].append(case)
            return 1
        elif sc == "suite":
            suite = self.create_suite(node.title, node.detail)
            out_dict['suites'].append(suite)
            out_dict = suite
        for i in node.children:
            self.get_dict(i, out_dict)

    def start(self, md_file):
        tree = self.get_tree_node(md_file)
        #self.show(tree)
        result_dict = self.create_suite(tree.title)
        self.get_dict(tree.children[0],result_dict)
        return result_dict['suites'][0]

    def show(self, node):
        print(node.title)
        print(node.detail)
        if node.children != []:
            #print("suite")
            for son_node in node.children:
                print(son_node.title)
                #self.show(son_node)

if __name__ == "__main__":
    md_file = "./smd2.md"
    md = MarkdownToDict()
    print(md.start(md_file))
    print("to be continue...")

