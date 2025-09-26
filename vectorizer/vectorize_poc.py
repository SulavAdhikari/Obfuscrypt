# --- Vector space classes ---
class VectorSpace:
    def __init__(self):
        self.dimensions = []

    def add_dimension(self, dimension):
        self.dimensions.append(dimension)

    def get_dimension_by_name(self, name):
        for dim in self.dimensions:
            if dim.name == name:
                return dim
        new_dim = Dimension(name=name)
        self.add_dimension(new_dim)
        return new_dim

class VectorCordinate:
    def __init__(self, vector_space, execution_position):
        self.vector_space = vector_space
        self.execution_position = execution_position

    def set_dimension_value(self, dim_name, value):
        dim = self.vector_space.get_dimension_by_name(dim_name)
        dim.values[self.execution_position] = value

class Dimension:
    def __init__(self, name, dim_type="variable"):
        self.name = name
        self.dim_type = dim_type
        self.values = {}

class ExecutionTrajectory(VectorSpace):
    pass

# --- JSON AST evaluator ---
def json_ast_to_vector_space_eval(json_ast):
    vs = ExecutionTrajectory()
    exec_pos = 0
    env = {}

    def eval_node(node):
        nonlocal exec_pos

        ntype = node.get("type")

        if ntype == "Constant":
            val = float(node["value"])
            coord = VectorCordinate(vs, exec_pos)
            coord.set_dimension_value("Const", val)
            exec_pos += 1
            return val

        elif ntype == "Name":
            val = env.get(node["id"], 0)
            coord = VectorCordinate(vs, exec_pos)
            coord.set_dimension_value(f"Var_{node['id']}", val)
            exec_pos += 1
            return val

        elif ntype == "BinaryOp":
            left = eval_node(node["left"])
            right = eval_node(node["right"])
            op = node["operator"]
            if op == "+":
                val = left + right
            elif op == "-":
                val = left - right
            elif op == "*":
                val = left * right
            elif op == "/":
                val = left / right
            else:
                val = 0
            coord = VectorCordinate(vs, exec_pos)
            coord.set_dimension_value("Return", val)
            exec_pos += 1
            return val

        elif ntype == "Call":
            args = [eval_node(arg) for arg in node["args"]]
            for val in args:
                coord = VectorCordinate(vs, exec_pos)
                coord.set_dimension_value("Arg", val)
                exec_pos += 1

            if node["identifier"]["type"] == "Name":
                fname = node["identifier"]["id"]
                if fname in env:
                    fnode = env[fname]["node"]
                    params = env[fname]["params"]
                    local_env = env.copy()
                    for p, v in zip(params, args):
                        local_env[p] = v
                    return eval_function_body(fnode["body"], local_env)
                else:
                    # built-in simulated functions
                    if fname == "sum":
                        return sum(args)
                    elif fname == "average_of_three":
                        return sum(args)/len(args)
            return 0

        elif ntype == "Assign":
            val = eval_node(node["value"])
            for target in node["targets"]:
                if target["type"] == "Name":
                    env[target["id"]] = val
                    coord = VectorCordinate(vs, exec_pos)
                    coord.set_dimension_value(f"Var_{target['id']}", val)
                    exec_pos += 1
            return val

        elif ntype == "FunctionDef":
            # only track definition, do NOT traverse body
            env[node["name"]] = {
                "node": node,
                "params": [d["name"] for d in node["args"]["defaults"]]
            }
            coord = VectorCordinate(vs, exec_pos)
            func_dim = vs.get_dimension_by_name("Op_FunctionDef")
            val = func_dim.values.get(exec_pos, 0) + 1
            coord.set_dimension_value("Op_FunctionDef", val)
            exec_pos += 1
            return None

        elif ntype == "Return":
            val = eval_node(node["value"])
            coord = VectorCordinate(vs, exec_pos)
            coord.set_dimension_value("Return", val)
            exec_pos += 1
            return val

        elif ntype == "Module":
            for stmt in node.get("body", []):
                eval_node(stmt)
            return None

        else:
            for child in node.values():
                if isinstance(child, dict):
                    eval_node(child)
                elif isinstance(child, list):
                    for c in child:
                        if isinstance(c, dict):
                            eval_node(c)
            return 0

    def eval_function_body(stmts, local_env):
        old_env = env.copy()
        env.update(local_env)
        ret = 0
        for stmt in stmts:
            if stmt["type"] == "Return":
                ret = eval_node(stmt["value"])
        env.clear()
        env.update(old_env)
        return ret

    eval_node(json_ast)
    return vs

# --- Tabulate ---
def trajectory_to_table(vs):
    max_pos = 0
    for dim in vs.dimensions:
        if dim.values:
            max_pos = max(max_pos, max(dim.values.keys()) + 1)
    table = []
    for i in range(max_pos):
        row = []
        for dim in vs.dimensions:
            row.append(dim.values.get(i, 0))
        table.append(row)
    headers = [dim.name for dim in vs.dimensions]
    return table, headers

# --- CSV ---
def save_csv(filename, table, headers):
    with open(filename, "w") as f:
        f.write(",".join(headers) + "\n")
        for row in table:
            f.write(",".join(str(x) for x in row) + "\n")

# --- Final coordinate ---
def final_coordinate_sum(vs):
    final_coord = {}
    for dim in vs.dimensions:
        final_coord[dim.name] = sum(dim.values.values()) if dim.values else 0
    return final_coord

# --- Example usage with your JSON ---
import json
from pprint import pprint

with open("pyparser/output/output.json", "r") as f:
    json_ast = json.load(f)

vs = json_ast_to_vector_space_eval(json_ast)
table, headers = trajectory_to_table(vs)
save_csv("trajectory.csv", table, headers)
final_coord = final_coordinate_sum(vs)

print("Final coordinate (sum of all steps per dimension):")
pprint(final_coord)
print("CSV saved as trajectory.csv")
