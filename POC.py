import ast, json, copy, random

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
                tmp=ast.Assign(targets=[ast.Name("_tmp",ctx=ast.Store())],value=node.targets[0].elts[0])
                # normal assignments
                assigns=[ast.Assign(targets=[t], value=v) for t,v in zip(node.targets[0].elts, node.value.elts)]
                # replace second with tmp
                assigns[1]=ast.Assign(targets=[node.targets[0].elts[1]], value=ast.Name("_tmp", ctx=ast.Load()))
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
                    s.body=[MarkSwap().visit(x) for x in s.body]
                    # add break if no swap at end of loop
                    s.body.append(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=ast.Name("_swapped",ctx=ast.Load())),
                                         body=[ast.Break()], orelse=[]))
        recurse_loops(node.body)
        return node

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

# ---------------- Pipeline ----------------
def rewrite_and_test(json_ast):
    """
    Main pipeline:
    1. Convert JSON AST -> Python ast.AST
    2. Apply SwapToTemp and AddEarlyExit transformations
    3. Unparse to source code
    4. Execute both original and rewritten functions
    5. Fuzz-test for correctness
    6. Return sample execution trajectories and final output
    """
    # 1. Convert JSON AST -> AST
    tree=json_to_ast(json_ast)
    ast.fix_missing_locations(tree)

    # 2. Deepcopy and transform
    tree2=copy.deepcopy(tree)
    tree2=SwapToTemp().visit(tree2)
    tree2=AddEarlyExit().visit(tree2)
    ast.fix_missing_locations(tree2)

    # 3. Produce source code
    src_orig=ast.unparse(tree)
    src_rewr=ast.unparse(tree2)

    # 4. Execute both
    ns1,ns2={},{}
    exec(src_orig, ns1)
    exec(src_rewr, ns2)
    fn_orig=ns1[next(k for k in ns1 if k!="__builtins__")]
    fn_rewr=ns2[next(k for k in ns2 if k!="__builtins__")]

    # 5. Fuzz-test
    for _ in range(300):
        arr=[random.randint(-30,30) for _ in range(random.randint(0,12))]
        if fn_orig(arr[:])!=fn_rewr(arr[:]) or fn_orig(arr[:])!=sorted(arr):
            return dict(pass=False, arr=arr, out1=fn_orig(arr[:]), out2=fn_rewr(arr[:]), src_orig=src_orig, src_rewr=src_rewr)

    # 6. Sample trajectory
    sample=[5,2,9,1,5,6]
    t1,t2=TracedList(sample[:]), TracedList(sample[:])
    out1,out2=fn_orig(t1), fn_rewr(t2)
    return dict(pass=True, src_orig=src_orig, src_rewr=src_rewr, traj_orig=t1.deltas(), traj_rewr=t2.deltas(), out=out1)
