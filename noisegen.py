import json, random, string, sys

def random_id(length=12):
    return ''.join(random.choices(string.ascii_letters, k=length))

def rename_identifiers(ast):
    rename_map = {}

    def rename(name):
        if name not in rename_map:
            rename_map[name] = random_id()
        return rename_map[name]

    def walk(node):
        if node["type"] == "function":
            node["name"] = rename(node["name"])
            node["args"] = [rename(arg) for arg in node["args"]]
            for stmt in node["body"]:
                walk(stmt)
        elif node["type"] == "call":
            node["func"] = rename(node["func"])
            node["args"] = [
                rename(arg) if isinstance(arg, str) and arg in rename_map else arg
                for arg in node["args"]
            ]
        elif node["type"] == "assign":
            node["var"] = rename(node["var"])
        return node

    return [walk(n) for n in ast]

def insert_noise(ast):
    for i in range(len(ast)):
        if random.random() < 0.4:
            ast.insert(i, {
                "type": random.choice(["assign", "call"]),
                "var": random_id(),
                "value": random.randint(0, 999),
                "func": "print",
                "args": [f"#{random_id(20)}"]
            })
    return ast

def to_python(ast):
    out = []

    def emit(n):
        if n["type"] == "function":
            out.append(f"def {n['name']}({', '.join(n['args'])}):")
            for stmt in n["body"]:
                out.append("    " + emit(stmt))
        elif n["type"] == "call":
            args = ", ".join(repr(a) if not isinstance(a, str) else a for a in n["args"])
            return f"{n['func']}({args})"
        elif n["type"] == "assign":
            return f"{n['var']} = {n['value']}"
        return ""

    for node in ast:
        line = emit(node)
        if line: out.append(line)
    return "\n".join(out)

# === MAIN ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python obfuscate_ast_json.py input.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        ast = json.load(f)

    ast = rename_identifiers(ast)
    ast = insert_noise(ast)
    code = to_python(ast)

    with open("obfuscated_output.py", "w") as f:
        f.write(code)

    print("[+] Obfuscated code written to obfuscated_output.py")
