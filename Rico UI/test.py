import json
from anytree import AnyNode, RenderTree

def recursively_build_tree(node_data, parent=None):
    # Create a dictionary of node attributes, filtering out 'children' as it's handled recursively
    node_attrs = {k: v for k, v in node_data.items() if k != "children"}
    node = AnyNode(parent=parent, **node_attrs)

    # Recursively add children if they exist
    for child_data in node_data.get("children", []):
        recursively_build_tree(child_data, parent=node)
    return node

# Assuming the JSON data is stored in a file called 'tree.json'
with open('tree.json', 'r') as file:
    json_data = json.load(file)

# The root of the JSON is under the key 'activity' -> 'root'
root_activity = json_data.get("activity", {}).get("root", None)
if root_activity:
    root = recursively_build_tree(root_activity)

    # Now you can work with the `root` object which is an `AnyNode` representing the root of the tree
    # To visualize the tree structure in the console
    for pre, _, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.class_)
        print(treestr.ljust(8), node.bounds)
else:
    print("The JSON structure does not contain an 'activity' -> 'root' key.")