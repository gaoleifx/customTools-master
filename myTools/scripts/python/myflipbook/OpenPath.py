import os
import hou

def openFilePath():
    
    path_names = ['file', 'sopoutput', '_path']

    for path_name in path_names:
        nodes = hou.selectedNodes()

        if len(nodes) == 0:
            print('没有选择节点')
            continue

        node = nodes[0]
       
        if node.parm(path_name) != None:
            full_path = node.parm(path_name).evalAsString()
            folder = os.path.dirname(full_path)
            os.startfile(folder)