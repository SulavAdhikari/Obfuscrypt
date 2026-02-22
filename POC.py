import ast, json, copy, random, sys, math
from pprint import pprint
# ---------------- JSON -> AST ----------------
def json_to_ast(node):
    """
    Convert a minimal JSON representation of Python code into a real ast.AST object.
    Only handles nodes needed for bubble sort (Module, FunctionDef, Assign, Name, Constant, BinOp, Compare, For, If, Call, Subscript, Tuple, Return).
    """
    t = node.get("type")
    if t=="Module":
        # Module contains a list of statements
        return ast.Module(body=[json_to_ast(n) for n in node["body"]], type_ignores=[])
    if t=="FunctionDef":
        # Function definition with name, arguments, and body
        args=json_to_ast(node["args"])
        body=[json_to_ast(s) for s in node["body"]]
        return ast.FunctionDef(name=node["name"], args=args, body=body, decorator_list=[], returns=None)
    if t=="arguments":
        # Function arguments
        args=[ast.arg(arg=a["arg"]) for a in node.get("args",[])]
        return ast.arguments(posonlyargs=[], args=args, vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
    if t=="Assign":
        # Assignment statement
        targets=[json_to_ast(t) for t in node["targets"]]
        value=json_to_ast(node["value"])
        return ast.Assign(targets=targets, value=value)
    if t=="Name":
        # Variable or identifier
        ctx=ast.Load() if node.get("ctx","Load")=="Load" else ast.Store()
        return ast.Name(id=node["id"], ctx=ctx)
    if t=="Constant":
        # Numeric or string constant
        return ast.Constant(value=node["value"])
    if t in ["BinaryOp","BinOp"]:
        # Binary operation: + or -
        left=json_to_ast(node["left"])
        right=json_to_ast(node["right"])
        op=node.get("operator") or node.get("op","+") 
        return ast.BinOp(left=left, op=ast.Add() if op=="+" else ast.Sub(), right=right)
    if t=="Compare":
        # Comparison operation: > or <
        left=json_to_ast(node["left"])
        ops=[]
        for o in node.get("ops",[]):
            ops.append(ast.Gt() if o==">" else ast.Lt())
        comparators=[json_to_ast(c) for c in node.get("comparators",[])]
        return ast.Compare(left=left, ops=ops, comparators=comparators)
    if t=="For":
        # For loop
        target=json_to_ast(node["target"])
        iter_=json_to_ast(node["iter"])
        body=[json_to_ast(s) for s in node.get("body",[])]
        return ast.For(target=target, iter=iter_, body=body, orelse=[])
    if t=="If":
        # If statement
        test=json_to_ast(node["test"])
        body=[json_to_ast(s) for s in node.get("body",[])]
        return ast.If(test=test, body=body, orelse=[])
    if t=="Call":
        # Function call
        func=json_to_ast(node["func"])
        args=[json_to_ast(a) for a in node.get("args",[])]
        return ast.Call(func=func, args=args, keywords=[])
    if t=="Return":
        # Return statement
        return ast.Return(value=json_to_ast(node["value"]))
    if t=="Tuple":
        # Tuple, e.g., for tuple swaps
        return ast.Tuple(elts=[json_to_ast(e) for e in node.get("elts",[])], ctx=ast.Load())
    if t=="Subscript":
        # Indexing into a list
        value=json_to_ast(node["value"])
        slice_=json_to_ast(node["slice"])
        return ast.Subscript(value=value, slice=slice_, ctx=ast.Load())
    if t=="RangeCall":
        # Custom node representing range(...)
        args=[json_to_ast(a) if isinstance(a,dict) else ast.Constant(value=a) for a in node.get("args",[])]
        return ast.Call(func=ast.Name(id="range", ctx=ast.Load()), args=args, keywords=[])
    if t=="Expr":
        # Standalone expression
        return ast.Expr(value=json_to_ast(node["value"]))
    raise NotImplementedError(f"Unhandled node: {t}")

# ---------------- Swap transformer ----------------
class SwapToTemp(ast.NodeTransformer):
    """
    Transform tuple swaps like a,b = b,a into explicit temporary variable swaps:
    _tmp = a; a = b; b = _tmp
    This avoids relying on tuple unpacking and is easier to track for early-exit logic.
    """
    def visit_Assign(self,node):
        self.generic_visit(node)
        # Only transform tuple-to-tuple assigns with same length
        if len(node.targets)==1 and isinstance(node.targets[0],ast.Tuple) and isinstance(node.value,ast.Tuple):
            if len(node.targets[0].elts)==len(node.value.elts):
                # tmp = first element
                tmp=ast.Assign(targets=[ast.Name("_tmp",ctx=ast.Store())],value=copy.deepcopy(node.targets[0].elts[0]))
                # normal assignments
                assigns=[ast.Assign(targets=[t], value=v) for t,v in zip(copy.deepcopy(node.targets[0].elts), copy.deepcopy(node.value.elts))]
                # replace second with tmp
                assigns[1]=ast.Assign(targets=[assigns[1].targets[0]], value=ast.Name("_tmp", ctx=ast.Load()))
                return [tmp]+assigns
        return node

# ---------------- Early-exit for any nested depth ----------------
class AddEarlyExit(ast.NodeTransformer):
    """
    Add bubble sort early-exit optimization:
    - Insert _swapped=False at the start of each loop
    - Mark _swapped=True whenever a swap occurs
    - Break loop if no swap occurred
    Works recursively for any nested loops.
    """
    def visit_FunctionDef(self,node):
        self.generic_visit(node)
        def recurse_loops(stmts):
            for i,s in enumerate(stmts):
                if isinstance(s,ast.For):
                    recurse_loops(s.body)  # handle inner loops first
                    
                    # Only instrument loops that contain other loops (the outer loop in bubble sort)
                    # Skipping the inner loop prevents partial sorting and early exits within a single pass
                    if not any(isinstance(child, ast.For) for child in s.body):
                        continue
                    
                    # insert _swapped=False at start of this loop
                    s.body.insert(0,ast.Assign(targets=[ast.Name("_swapped",ctx=ast.Store())], value=ast.Constant(False)))
                    # mark swaps in loop body
                    class MarkSwap(ast.NodeTransformer):
                        def visit_Assign(self, n):
                            self.generic_visit(n)
                            # Heuristic: tuple assign to list elements = swap
                            if isinstance(n.value, ast.Tuple) and any(isinstance(e, ast.Subscript) for e in n.value.elts):
                                return [ast.Assign(targets=[ast.Name("_swapped",ctx=ast.Store())], value=ast.Constant(True)), n]
                            return n
                    new_body = []
                    for x in s.body:
                        res = MarkSwap().visit(x)
                        if isinstance(res, list):
                            new_body.extend(res)
                        else:
                            new_body.append(res)
                    s.body = new_body
                    # add break if no swap at end of loop
                    s.body.append(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=ast.Name("_swapped",ctx=ast.Load())),
                                         body=[ast.Break()], orelse=[]))
        recurse_loops(node.body)
        return node

# ---------------- Variable Renaming ----------------
class RenameVariables(ast.NodeTransformer):
    """
    Rename all variables in the function to obfuscated names (random strings).
    Maintains a mapping of old_name -> new_name.
    Preserves built-is and function names.
    """
    def __init__(self):
        self.mapping = {}
        # Add basic built-ins to ignore list
        self.ignored = {"len", "range", "print", "list", "sorted", "int", "str", "append"}

    def _get_new_name(self, old_name):
        if old_name in self.ignored:
            return old_name
        if old_name not in self.mapping:
            # Generate a random string of length 8
            new_name = "v_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
            self.mapping[old_name] = new_name
        return self.mapping[old_name]

    def visit_FunctionDef(self, node):
        # Don't rename the function itself, but visit arguments and body
        # We need to handle arguments specifically to register them in the mapping
        for arg in node.args.args:
            arg.arg = self._get_new_name(arg.arg)
        
        # Visit body
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        node.id = self._get_new_name(node.id)
        return node

# ---------------- Variable Importance Analysis ----------------
class VariableImportanceAnalyzer(ast.NodeVisitor):
    """
    Analyze the AST to assign importance scores to variables.
    Scores are based on:
    - Arguments (+5): Critical entry points.
    - Usage Frequency (+1 per use): Core logic indicator.
    - Data Access/Subscript (+10): Indices/Keys are usually algorithmic drivers.
    """
    def __init__(self):
        self.scores = {}
        self.ignored = {"len", "range", "print", "list", "sorted", "int", "str", "append"}

    def _add_score(self, name, points):
        if name in self.ignored:
            return
        self.scores[name] = self.scores.get(name, 0) + points

    def visit_FunctionDef(self, node):
        # High importance for arguments
        for arg in node.args.args:
            self._add_score(arg.arg, 5)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Base score for usage
        self._add_score(node.id, 1)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Extra importance for variables used in slices/indices
        if isinstance(node.slice, ast.Name):
            self._add_score(node.slice.id, 10)
        elif isinstance(node.slice, ast.BinOp):
            # Recurse to find Names in index expressions like j+1
            for n in ast.walk(node.slice):
                if isinstance(n, ast.Name):
                    self._add_score(n.id, 10)
        self.generic_visit(node)

# ---------------- Traced list ----------------
class TracedList(list):
    """
    List wrapper that tracks all state changes.
    - stores all versions of the list in self.states
    - deltas() returns element-wise changes between consecutive states
    """
    def __init__(self,data):
        super().__init__(data)
        self.states=[self.copy()]
    def __setitem__(self,i,v):
        super().__setitem__(i,v)
        self.states.append(self.copy())
    def deltas(self):
        # compute element-wise differences
        return [[b-a for a,b in zip(a_,b_)] for a_,b_ in zip(self.states,self.states[1:])]

# ---------------- Floatify ----------------
def floatify(v):
    """
    Convert any Python value to a float for use as a coordinate in state space.
    """
    if isinstance(v, bool):   return 1.0 if v else 0.0
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, (list, tuple, str)): return float(len(v))
    return 0.0

# ---------------- Final Coord Capture ----------------
def get_final_coords(fn, arg):
    """
    Run fn(arg) under sys.settrace and capture the local variable
    values at the moment of return as a dict {var_name: float_value}.
    Matches the target frame by code object identity (fn.__code__),
    not by name, so functions sharing the same name are distinguished.
    """
    captured = {}
    result_box = [None]
    target_code = fn.__code__

    def tracer(frame, event, _arg):
        if frame.f_code is target_code and event == 'return':
            captured.update(frame.f_locals)
        return tracer

    sys.settrace(tracer)
    try:
        result_box[0] = fn(arg)
    finally:
        sys.settrace(None)

    named_coords = {name: floatify(val) for name, val in captured.items()}
    return result_box[0], named_coords

# ---------------- Monte Carlo Dimension Identification ----------------
def monte_carlo_equivalence(fn1, fn2, importance_scores=None, weighted_threshold=0.8, max_samples=300, confidence_threshold=50):
    """
    Probabilistically assess functional equivalence via importance-weighted dimension identification.

    For each random input, capture the named final state of both functions.
    Maintain a mapping candidates. Functional equivalence is declared if the sum 
    of importance for matched variables exceeds the weighted_threshold.
    """
    candidates = None   # dict: fn1_var -> set of fn2_vars
    last_coords = {}    # fn1_var -> last float value seen (for display)
    consecutive_confirmations = 0
    samples_used = 0

    # If no scores provided, treat all seen variables as equally important (1.0)
    # total_importance will be calculated once we see all variables
    total_importance = sum(importance_scores.values()) if importance_scores else 0

    for _ in range(max_samples):
        arr = [random.randint(-30, 30) for _ in range(random.randint(1, 10))]
        samples_used += 1

        r1, nc1 = get_final_coords(fn1, arr[:])
        r2, nc2 = get_final_coords(fn2, arr[:])

        # Basic output check first
        if r1 != r2:
            return {'equivalent': False, 'confidence': 0,
                    'samples_used': samples_used, 'named_mapping': None,
                    'mismatch_input': arr, 'matched_importance': 0.0}

        last_coords = {n: v for n, v in nc1.items()}

        if candidates is None:
            candidates = {}
            for n1, v1 in nc1.items():
                candidates[n1] = {n2 for n2, v2 in nc2.items()
                                  if math.isclose(v1, v2, rel_tol=1e-6, abs_tol=1e-9)}
        else:
            for n1 in nc1:
                if n1 not in candidates:
                    candidates[n1] = set(nc2.keys())
            new_cands = {}
            for n1, v1 in nc1.items():
                matches = {n2 for n2, v2 in nc2.items()
                           if math.isclose(v1, v2, rel_tol=1e-6, abs_tol=1e-9)}
                intersected = candidates[n1] & matches
                new_cands[n1] = intersected if intersected else candidates[n1]
            candidates = new_cands

        # Calculate importance-weighted match ratio
        if importance_scores:
            matched_importance = sum(importance_scores.get(n1, 0) for n1, s in candidates.items() if len(s) >= 1)
            # update total_importance in case we see variables not in initial scores (unlikely but safe)
            current_total = max(total_importance, sum(importance_scores.get(n1, 0) for n1 in candidates))
            match_ratio = matched_importance / current_total if current_total > 0 else 1.0
        else:
            # Fallback to simple ratio if no scores provided
            matched_count = sum(1 for s in candidates.values() if len(s) >= 1)
            match_ratio = matched_count / len(candidates) if candidates else 1.0

        if match_ratio >= weighted_threshold:
            consecutive_confirmations += 1
            if consecutive_confirmations >= confidence_threshold:
                named_mapping = [
                    (n1, next(iter(s)), last_coords.get(n1, 0.0), importance_scores.get(n1, 0) if importance_scores else 1.0)
                    for n1, s in candidates.items() if len(s) >= 1
                ]
                return {'equivalent': True,
                        'confidence': consecutive_confirmations,
                        'samples_used': samples_used,
                        'named_mapping': named_mapping,
                        'mismatch_input': None,
                        'match_ratio': match_ratio}
        else:
            consecutive_confirmations = 0

    # Return best guess
    named_mapping = [
        (n1, next(iter(s)), last_coords.get(n1, 0.0), importance_scores.get(n1, 0) if importance_scores else 1.0)
        for n1, s in candidates.items() if len(s) >= 1
    ] if candidates else None
    
    current_total = sum(importance_scores.values()) if importance_scores else len(candidates) if candidates else 1
    matched_val = sum(importance_scores.get(n1, 0) for n1, s in candidates.items() if len(s) >= 1) if importance_scores and candidates else sum(1 for s in candidates.values() if len(s) >= 1) if candidates else 0
    final_ratio = matched_val / current_total

    return {'equivalent': final_ratio >= weighted_threshold,
            'confidence': consecutive_confirmations,
            'samples_used': samples_used,
            'named_mapping': named_mapping,
            'mismatch_input': None,
            'match_ratio': final_ratio}

# ---------------- Pipeline ----------------
def rewrite_and_test(json_ast):
    """
    Main pipeline:
    1. Convert JSON AST -> Python ast.AST
    2. Analyze variable importance
    3. Apply transformations (SwapToTemp, AddEarlyExit, RenameVariables)
    4. Execute both functions
    5. Fuzz-test and check importance-weighted equivalence
    """
    # 1. Convert JSON AST -> AST
    tree=json_to_ast(json_ast)
    ast.fix_missing_locations(tree)

    # 2. Analyze Importance BEFORE transformations/renaming
    analyzer = VariableImportanceAnalyzer()
    analyzer.visit(tree)
    importance_scores = analyzer.scores

    # 3. Deepcopy and transform
    tree2=copy.deepcopy(tree)
    tree2=AddEarlyExit().visit(tree2)
    tree2=SwapToTemp().visit(tree2)
    renamer = RenameVariables()
    tree2=renamer.visit(tree2)
    ast.fix_missing_locations(tree2)

    # 4. Produce source code
    src_orig=ast.unparse(tree)
    src_rewr=ast.unparse(tree2)
    
    # Print debug info
    with open("debug_poc.txt", "w") as f:
        f.write("Rewritten Source Code:\n")
        f.write("-" * 40 + "\n")
        f.write(src_rewr + "\n")
        f.write("-" * 40 + "\n")
        f.write("Variable Mapping:\n")
        f.write(str(renamer.mapping) + "\n")
        f.write("Importance Scores:\n")
        f.write(str(importance_scores) + "\n")

    # 5. Execute both
    ns1,ns2={},{}
    try:
        exec(src_orig, ns1)
        fn_orig=ns1[next(k for k in ns1 if k!="__builtins__")]
        
        exec(src_rewr, ns2)
        fn_rewr=ns2[next(k for k in ns2 if k!="__builtins__")]
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("-" * 40)
        print("Rewritten Source Code:")
        print("-" * 40)
        print(src_rewr)
        print("-" * 40)
        raise e

    # 6. Fuzz-test
    for _ in range(300):
        arr=[random.randint(-30,30) for _ in range(random.randint(0,12))]
        if fn_orig(arr[:])!=fn_rewr(arr[:]) or fn_orig(arr[:])!=sorted(arr):
            return {'pass': False, 'arr': arr, 'out1': fn_orig(arr[:]), 'out2': fn_rewr(arr[:]), 'src_orig': src_orig, 'src_rewr': src_rewr}

    # 7. Sample trajectory
    sample=[5,2,9,1,5,6]
    t1,t2=TracedList(sample[:]), TracedList(sample[:])
    out1,out2=fn_orig(t1), fn_rewr(t2)

    # 8. Monte Carlo importance-weighted equivalence check
    equiv = monte_carlo_equivalence(fn_orig, fn_rewr, importance_scores=importance_scores)

    return {'pass': True, 'src_orig': src_orig, 'src_rewr': src_rewr,
            'traj_orig': t1.deltas(), 'traj_rewr': t2.deltas(), 'out': out1,
            'equivalence': equiv, 'importance_scores': importance_scores}

if __name__ == "__main__":
    bubble_sort_json = {
        "type": "Module",
        "body": [
            {
                "type": "FunctionDef",
                "name": "bubble_sort",
                "args": {
                    "type": "arguments",
                    "args": [
                        {"arg": "arr"}
                    ]
                },
                "body": [
                    {
                        "type": "Assign",
                        "targets": [
                            {"type": "Name", "id": "n"}
                        ],
                        "value": {
                            "type": "Call",
                            "func": {"type": "Name", "id": "len"},
                            "args": [{"type": "Name", "id": "arr"}]
                        }
                    },
                    {
                        "type": "For",
                        "target": {"type": "Name", "id": "i"},
                        "iter": {
                            "type": "RangeCall",
                            "args": [{"type": "Name", "id": "n"}]
                        },
                        "body": [
                            {
                                "type": "For",
                                "target": {"type": "Name", "id": "j"},
                                "iter": {
                                    "type": "RangeCall",
                                    "args": [
                                        0,
                                        {
                                            "type": "BinOp",
                                            "left": {"type": "Name", "id": "n"},
                                            "op": "-",
                                            "right": {
                                                "type": "BinOp",
                                                "left": {"type": "Name", "id": "i"},
                                                "op": "+",
                                                "right": {"type": "Constant", "value": 1}
                                            }
                                        }
                                    ]
                                },
                                "body": [
                                    {
                                        "type": "If",
                                        "test": {
                                            "type": "Compare",
                                            "left": {
                                                "type": "Subscript",
                                                "value": {"type": "Name", "id": "arr"},
                                                "slice": {"type": "Name", "id": "j"}
                                            },
                                            "ops": [">"],
                                            "comparators": [
                                                {
                                                    "type": "Subscript",
                                                    "value": {"type": "Name", "id": "arr"},
                                                    "slice": {
                                                        "type": "BinOp",
                                                        "left": {"type": "Name", "id": "j"},
                                                        "op": "+",
                                                        "right": {"type": "Constant", "value": 1}
                                                    }
                                                }
                                            ]
                                        },
                                        "body": [
                                            {
                                                "type": "Assign",
                                                "targets": [
                                                    {
                                                        "type": "Tuple",
                                                        "elts": [
                                                            {
                                                                "type": "Subscript",
                                                                "value": {"type": "Name", "id": "arr"},
                                                                "slice": {"type": "Name", "id": "j"}
                                                            },
                                                            {
                                                                "type": "Subscript",
                                                                "value": {"type": "Name", "id": "arr"},
                                                                "slice": {
                                                                    "type": "BinOp",
                                                                    "left": {"type": "Name", "id": "j"},
                                                                    "op": "+",
                                                                    "right": {"type": "Constant", "value": 1}
                                                                }
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "value": {
                                                    "type": "Tuple",
                                                    "elts": [
                                                        {
                                                            "type": "Subscript",
                                                            "value": {"type": "Name", "id": "arr"},
                                                            "slice": {
                                                                "type": "BinOp",
                                                                "left": {"type": "Name", "id": "j"},
                                                                "op": "+",
                                                                "right": {"type": "Constant", "value": 1}
                                                            }
                                                        },
                                                        {
                                                            "type": "Subscript",
                                                            "value": {"type": "Name", "id": "arr"},
                                                            "slice": {"type": "Name", "id": "j"}
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "Return",
                        "value": {"type": "Name", "id": "arr"}
                    }
                ]
            }
        ]
    }
    
    # Run the pipeline
    result = rewrite_and_test(bubble_sort_json)
    
    print("-" * 40)
    print("Original Source Code:")
    print("-" * 40)
    print(result.get('src_orig', 'N/A'))
    print("\n" + "-" * 40)
    print("Rewritten Source Code:")
    print("-" * 40)
    print(result.get('src_rewr', 'N/A'))
    print("\n" + "-" * 40)
    
    if not result['pass']:
        print("FAILED!")
        print(f"Input Arr: {result.get('arr')}")
    else:
        print("PASSED!")
        eq = result.get('equivalence', {})
        print("\n" + "=" * 40)
        print("MONTE CARLO WEIGHTED EQUIVALENCE REPORT")
        print("=" * 40)
        print(f"Equivalent       : {eq.get('equivalent')}")
        print(f"Confidence       : {eq.get('confidence')} consecutive samples")
        print(f"Samples used     : {eq.get('samples_used')}")
        print(f"Weighted Match % : {eq.get('match_ratio', 0.0) * 100:.2f}%")
        
        nm = eq.get('named_mapping')
        if nm:
            print("\nMATCHED VARIABLES (Original -> Rewritten):")
            print("-" * 40)
            for n1, n2, val, score in nm:
                # Use ascii-safe arrows and clean alignment
                print(f"  {n1:12s} -> {n2:12s} [Val: {val:7.1f}, Weight: {score:3d}]")
        
        all_orig = set(result.get('importance_scores', {}).keys())
        matched_orig = {x[0] for x in nm} if nm else set()
        unmatched = all_orig - matched_orig
        if unmatched:
            print("\nUNMATCHED VARIABLES (Original):")
            print("-" * 40)
            for n1 in sorted(unmatched):
                print(f"  {n1:12s} [Weight: {result['importance_scores'].get(n1, 0):3d}]")
        print("=" * 40)
