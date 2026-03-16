# Obfuscrypt — Project Documentation (LLM Reference)

> **Purpose of this file**: Dense, self-contained reference for LLMs. Covers every module, class, function, data contract, and design decision so the entire project can be understood without reading source code.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Name** | Obfuscrypt |
| **Type** | Research prototype / proof-of-concept |
| **Goal** | Modular code obfuscation framework — transform source code semantics-preservingly while hiding logic and implementation |
| **Primary language** | Python |
| **Secondary language** | PowerShell (parser exists, no transformation pipeline) |
| **Status** | Not production-ready; experimental tooling |
| **Dependencies** | `antlr4-python3-runtime==4.13.1`, `pytest==7.4.3` |
| **Test runner** | pytest |
| **Entry point (parser)** | `pyparser/main.py::parse_python()` |
| **Entry point (pipeline)** | `POC.py::rewrite_and_test()` |
| **Entry point (vectorizer)** | `vectorizer/vectorize_poc.py` (run directly) |

---

## 2. Repository Layout

```
obfuscrypt/
├── POC.py                          # Main obfuscation + verification pipeline (self-contained)
├── README.md                       # High-level overview
├── DOCUMENTATION.md                # This file
├── requirements.txt                # antlr4-python3-runtime, pytest
├── trajectory.csv                  # Sample vectorizer output (gittracked artifact)
├── obfuscrypt_base/
│   ├── __init__.py                 # Empty
│   ├── ast_nodes.py                # Language-agnostic custom AST node class library
│   └── ast_object.py               # Wrapper for AST analysis and variable gathering
├── pyparser/
│   ├── PythonParser.g4             # ANTLR parser grammar for Python 2/3 (387 lines)
│   ├── PythonLexer.g4              # ANTLR lexer grammar for Python
│   ├── PythonParser.py             # ANTLR-generated parser (do not edit)
│   ├── PythonLexer.py              # ANTLR-generated lexer (do not edit)
│   ├── PythonParserVisitor.py      # ANTLR-generated base visitor (do not edit)
│   ├── PythonParserListener.py     # ANTLR-generated listener (do not edit)
│   ├── PythonParserBase.py         # Python 2/3 version-checking superclass for parser
│   ├── PythonLexerBase.py          # Indent/dedent logic superclass for lexer
│   ├── python_ast_visitor.py       # Custom visitor: parse tree → custom AST nodes
│   ├── main.py                     # parse_python() entry point; reads input/, writes output/
│   ├── input/input.py              # Sample Python source for the parser
│   └── output/output.json          # JSON AST output from the parser
├── powerparser/
│   ├── PowerExp.g4                 # ANTLR grammar for PowerShell (261 lines)
│   ├── PowerExpParser.py           # ANTLR-generated parser
│   ├── PowerExpLexer.py            # ANTLR-generated lexer
│   ├── PowerExpVisitor.py          # ANTLR-generated base visitor
│   ├── PowerExpListener.py         # ANTLR-generated listener
│   ├── visitor.py                  # Custom visitor stub for PowerShell AST
│   └── main_power_parser.py        # PowerShell parser entry point (stub)
├── vectorizer/
│   └── vectorize_poc.py            # Maps JSON AST → multidimensional execution trajectory
└── tests/
    ├── tests_pyparser/
    │   ├── test_functions.py       # 3 pytest cases for function parsing
    │   └── test_ifstatements.py    # 5 pytest cases for if/elif/else parsing
    └── tests_base/                 # Empty (reserved for obfuscrypt_base tests)
```

---

## 3. End-to-End Data Flow

```
Python source code (string)
        │
        ▼  [ANTLR: PythonLexer + PythonParser]
  ANTLR Parse Tree (antlr4.ParserRuleContext)
        │
        ▼  [PythonASTVisitor.visit()]
  Custom AST (obfuscrypt_base.ast_nodes objects)
        │
        ▼  [.to_dict() on root Module node]
  JSON dict  ──────────────────────────────────────────────────────┐
        │                                                           │
        ▼  [POC.py: json_to_ast()]                                  ▼ [vectorize_poc.py]
  Python stdlib ast.AST                               ExecutionTrajectory (VectorSpace)
        │                                                           │
        ▼  [VariableImportanceAnalyzer.visit()]                     ▼ [trajectory_to_table()]
  importance_scores: dict[str, int]                  2D table of float coordinates
        │                                                           │
        ▼  [deepcopy + AST transformers]                            ▼ [save_csv()]
  Obfuscated ast.AST                                 trajectory.csv
        │
        ▼  [ast.unparse()]
  Obfuscated Python source (string)
        │
        ▼  [exec() in isolated namespace]
  fn_orig, fn_rewr (callable functions)
        │
        ▼  [monte_carlo_equivalence()]
  Equivalence Report (dict)
```

---

## 4. Module: `obfuscrypt_base/ast_nodes.py`

**Role**: Language-agnostic custom AST node type library. Used by `PythonASTVisitor` to build a structured AST that serializes cleanly to JSON. Not used by `POC.py` (which uses Python's stdlib `ast`).

### 4.1 Enums and Utility Types

| Class | Description |
|---|---|
| `NodeType` (Enum) | String identifiers for all node types. Values like `"Module"`, `"FunctionDef"`, `"BinaryOp"`, etc. Used as `node_type` field on every node. |
| `Position` (dataclass) | `line: int, column: int` — source-code location |
| `Location` (dataclass) | `start: Position, end: Position` |

### 4.2 Base Hierarchy

```
ASTNode          (base: node_type: NodeType, location: Optional[Location], to_dict())
  ├── Statement  (marker subclass for statement nodes)
  └── Expression (marker subclass for expression nodes)
```

Every concrete node inherits from one of these and **overrides `to_dict()`** to add its specific fields. The serialized dict always begins with `{"type": NodeType.value, ...}`.

### 4.3 Statement Nodes

| Class | NodeType value | Key fields |
|---|---|---|
| `Module` | `"Module"` | `body: List[Statement]` |
| `FunctionDef` | `"FunctionDef"` | `name: str`, `args: Arguments`, `body: List[Statement]`, `decorator_list: List[Decorator]`, `returns: Optional[Expression]`, `async_: bool` |
| `Assign` | `"Assign"` | `targets: List[Expression]`, `value: Expression`, `operator: str` (default `"="`) |
| `IfStmt` | `"IfStatement"` | `test: Expression`, `body: List[Statement]`, `elif_clauses: List[ElifStmt]`, `else_clause: Optional[ElseStmt]` |
| `ElifStmt` | `"ElifStatement"` | `test: Expression`, `body: List[Statement]` |
| `ElseStmt` | `"ElseStatement"` | `body: List[Statement]` |
| `WhileStmt` | `"WhileStatement"` | `test: Expression`, `body: List[Statement]`, `orelse: List[Statement]` |
| `ForStmt` | `"ForStatement"` | `target: Expression`, `iter: Expression`, `body: List[Statement]`, `orelse: List[Statement]`, `async_: bool` |
| `ReturnStmt` | `"Return"` | `value: Optional[Expression]` |
| `RaiseStmt` | `"Raise"` | `exc: Optional[Expression]`, `cause: Optional[Expression]` |
| `ImportStmt` | `"Import"` | `names: List[Alias]` |
| `ImportFromStmt` | `"ImportFrom"` | `module: Optional[str]`, `names: List[Alias]`, `level: Optional[int]` |
| `PassStmt` | `"Pass"` | *(Takes no arguments)* |
| `BreakStmt` | `"Break"` | *(Takes no arguments)* |
| `ContinueStmt` | `"Continue"` | *(Takes no arguments)* |

### 4.4 Expression Nodes

| Class | NodeType value | Key fields |
|---|---|---|
| `BinaryOp` | `"BinaryOp"` | `left: Expression`, `operator: str`, `right: Expression` |
| `UnaryOp` | `"UnaryOp"` | `operator: str`, `operand: Expression` |
| `Call` | `"Call"` | `identifier: Expression`, `args: List[Expression]` |
| `Constant` | `"Constant"` | `value: Any`, `dtype: Optional[str]` (e.g. `"NUMBER"`, `"STRING"`, `"BOOLEAN"`) |
| `Name` | `"Name"` | `id: str`, `ctx: str` (`"Load"` or `"Store"`) |
| `Attribute` | `"Attribute"` | `value: Expression`, `attr: str` |
| `Subscript` | `"Subscript"` | `value: Expression`, `slice: Expression` |
| `ListExpr` | `"List"` | `elts: List[Expression]` |
| `TupleExpr` | `"Tuple"` | `elts: List[Expression]` |
| `DictExpr` | `"Dict"` | `keys: List[Optional[Expression]]`, `values: List[Expression]` |
| `SetExpr` | `"Set"` | `elts: List[Expression]` |

### 4.5 Auxiliary Nodes

| Class | Description |
|---|---|
| `Arguments` | `args: List[Arg]`, `vararg: Optional[Arg]`, `kwarg: Optional[Arg]`, `defaults: List[Expression]`. Serialized as flat dict (not wrapped in `type`) |
| `Arg` | `name: str`, `annotation: Optional[Expression]`. Serialized as `{"name": ..., "annotation": ...}` |
| `Decorator` | `expression: Expression` |
| `Alias` | `name: str`, `asname: Optional[str]` — for import statements |

### 4.6 `ASTObject` (`obfuscrypt_base/ast_object.py`)

**Role**: Provides analysis and traversal capabilities by wrapping raw `ASTNode` instances into an object-oriented tree. Every node in `ast_nodes.py` provides a `.get_object()` method that returns an `ASTObject` for that node.

| Method/Property | Description |
|---|---|
| `__init__(node, parent, depth)` | Wraps a node, instantiates children as `ASTObject`s, and tracks parent pointers and depth. |
| `gather_variables()` | Recursively collects all variables (by name and depth) defined within this node and its children. |
| `is_state_mutation_node()` | Identifies assignments that mutate variable state. |
| `is_control_flow_node()` | Identifies loops, conditionals, and flow control (`If`, `While`, `Return`, `Break`, `Continue`, etc.). |
| `is_definition_node()` | Identifies function/class definitions and variable assignments. |
| `child_nodes` / `child_statements`| Lists of child `ASTObject`s for recursive traversal or transformation. |
| `distance_from_main_module` | Depth of the node in the AST hierarchy (0 for root layer). |

---

## 5. Module: `pyparser/`

**Role**: Parses Python source text into the custom AST JSON. Pipeline: source → ANTLR parse tree → custom AST objects → JSON dict.

### 5.1 Grammar (`PythonParser.g4`, `PythonLexer.g4`)

- Full Python 2 and 3 grammar (387 parser rules + lexer rules)
- Parser inherits from `PythonParserBase` which provides `CheckVersion(n)` and `SetVersion(n)` for disambiguation between Python 2 and 3 syntax at runtime
- Lexer inherits from `PythonLexerBase` which handles indent/dedent token injection (Python's whitespace-sensitive parsing)
- Key parser rules: `file_input`, `funcdef`, `typedargslist`, `suite`, `stmt`, `simple_stmt`, `small_stmt`, `expr_stmt`, `assign_part`, `if_stmt`, `elif_clause`, `else_clause`, `comparison`, `expr`, `atom`, `trailer`, `arguments`, `subscript`

### 5.2 `PythonASTVisitor` (`pyparser/python_ast_visitor.py`)

Extends ANTLR-generated `PythonParserVisitor`. Maps parse tree context objects to custom `ast_nodes` objects.

| Method | Input Context | Returns | Notes |
|---|---|---|---|
| `visitFile_input` | `File_inputContext` | `Module` | Iterates stmt children, collects non-None nodes |
| `visitFuncdef` | `FuncdefContext` | `FunctionDef` | Extracts name, args, suite, return type, async flag |
| `visitTypedargslist` | `TypedargslistContext` | `Arguments` | Handles `Named_parameter`, `Varargs`, `Varkwargs`, `Def_parameters` |
| `visitNamed_parameter` | `Named_parameterContext` | `Arg` | name + optional annotation |
| `visitVarargs` | `VarargsContext` | `Arg` | `*args` parameter |
| `visitVarkwargs` | `VarkwargsContext` | `Arg` | `**kwargs` parameter |
| `visitName` | name context | `Constant` or `Name` | Returns `Constant(True/False/BOOLEAN)` for `True`/`False`; `Name(id, ctx="Load")` otherwise |
| `visitSuite` | `SuiteContext` | `List[Statement]` | Handles inline suite (single stmt) and indented block |
| `visitStmt` | `StmtContext` | `Statement` | Dispatches to `simple_stmt` or `compound_stmt` |
| `visitSimple_stmt` | `Simple_stmtContext` | `Statement` | Visits first `small_stmt` only |
| `visitSmall_stmt` | mixed context | `Statement` | Dispatches: `expr_stmt`, `return_stmt`, `pass_stmt`, `break_stmt`, `continue_stmt` |
| `visitExpr_stmt` | `Expr_stmtContext` | `Assign` or expr | If `assign_part` present: builds `Assign`; otherwise falls through |
| `visitAssign_part` | assign context | `(operator: str, value)` | Returns tuple of operator string and value node |
| `visitReturn_stmt` | `Return_stmtContext` | `ReturnStmt` | Wraps `testlist` visit result |
| `visitAtom` | `AtomContext` | `Expression` | Handles `name`, `number`, `STRING` literals |
| `visitExpr` | `ExprContext` | `BinaryOp` or `Call` or child | 3-child → BinaryOp; trailer with arguments → Call; else visits child |
| `visitNumber` | `NumberContext` | `Constant` | Uses `eval()` on number text |
| `visitIf_stmt` | `If_stmtContext` | `IfStmt` | Collects test, body, elif_clauses, else_clause |
| `visitElif_clause` | `Elif_clauseContext` | `ElifStmt` | test + body |
| `visitElse_clause` | `Else_clauseContext` | `ElseStmt` | body only |
| `visitComparison` | `ComparisonContext` | `BinaryOp` or child | 3-child → BinaryOp with operator; else dispatches to children |
| `visitChildren` | any node | value or list | Fallback: collects non-None results; unwraps singleton lists |
| `visitWhile_stmt` | `While_stmtContext` | `WhileStmt` | Extracts `test`, `suite` mapping to `body`, and optional `else_clause` |
| `visitFor_stmt` | `For_stmtContext` | `ForStmt` | Extracts `target`, `iter`, `suite` mapping to `body`, and optional `else_clause` |
| `visitBreak_stmt` | `Break_stmtContext` | `BreakStmt` | Returns `BreakStmt` node directly |
| `visitContinue_stmt` | `Continue_stmtContext` | `ContinueStmt` | Returns `ContinueStmt` node directly |
| `visitPass_stmt` | `Pass_stmtContext` | `PassStmt` | Returns `PassStmt` node directly |
| `visitImport_stmt` | `Import_stmtContext` | `ImportStmt` | Extracts names and `asname` aliases from `dotted_as_names` |
| `visitFrom_stmt` | `From_stmtContext` | `ImportFromStmt` | Extracts module from `dotted_name` and handles `import_as_names` or wildcard |

**Important behaviours**:
- Decorators are **not yet implemented** (always empty list)
- `visitSimple_stmt` only visits the **first** small_stmt (semicolon-separated statements on one line are partially supported)
- `visitNumber` uses Python `eval()`, so number literals like `0x1F` and `3.14` work
- `visitAtom` for strings: concatenates adjacent string literals using `eval()` on each token

### 5.3 `parse_python(code: str) -> dict` (`pyparser/main.py`)

```python
# Usage
from pyparser.main import parse_python
result = parse_python("def foo(): return 1")
# => {"type": "Module", "body": [...]}
```

Steps:
1. `InputStream(code)` → `PythonLexer` → `CommonTokenStream`
2. `PythonParser(stream).file_input()` → parse tree
3. `PythonASTVisitor().visit(tree)` → `Module` object
4. `.to_dict()` → Python dict

**When run as `__main__`**: reads `pyparser/input/input.py`, writes `pyparser/output/output.json`.

---

## 6. Module: `powerparser/`

**Role**: ANTLR-based PowerShell parser. Currently a **parser-only** component — no transformation pipeline exists.

### 6.1 Grammar (`PowerExp.g4`)

Full PowerShell grammar (261 lines). Covers:
- Statements: `commandStatement`, `assignment`, `ifStatement`, `whileStatement`, `foreachStatement`, `doWhileStatement`, `forStatement`, `tryCatchStatement`, `switchStatement`, `functionDecl`, `paramBlock`, `flowControl`
- Expressions: pipeline → logical → bitwise → comparison → additive → multiplicative → unary → postfix → base
- Base atoms: `NUMBER`, `STRING`, `INTERP_STRING`, `HEREDOC`, `VARIABLE` (`$name`), `IDENTIFIER`, arrays `@(...)`, hashtables `@{...}`
- Operators: PowerShell style (`-eq`, `-ne`, `-gt`, `-lt`, `-and`, `-or`, etc.)
- Comments: `# line comment`, `<# block comment #>`

### 6.2 `Visitor` (`powerparser/visitor.py`)

Extends `PowerExpVisitor`. Maps PowerShell parse tree nodes to `Structure` objects (from `obfuscrypt.obfuscrypt_base` — note: **this import path appears to be a legacy/broken reference**; the actual package is `obfuscrypt_base`).

| Method | Returns |
|---|---|
| `visitScript` | `Structure(class_type="CodeBlock", parameters=[...])` |
| `visitIdentifier` | `Structure("Identifier", value=query)` |
| `visitFunctionCall` | `Structure("Function", function_name=..., parameters=[...])` |
| `visitCommandStatement` | `Structure("Operation", value="CommandExecution", parameters=[...])` |
| `visitCodeBlock` | `Structure("CodeBlock", parameters=[...])` |
| `visitFunctionDecl` | `Structure("Operation", value="FunctionDefinition", parameters=[...])` |

**Note**: `visitFunctionCall` is defined **twice** with different implementations (duplicate method — later definition overrides the first in Python).

---

## 7. Module: `POC.py` (Main Pipeline)

**Role**: Self-contained proof-of-concept pipeline. Uses Python's **stdlib `ast` module** (not the custom nodes) to parse, transform, and verify a bubble sort function given as a JSON AST.

> Key distinction: `POC.py` operates on `ast.AST` objects (Python's built-in), NOT on `obfuscrypt_base.ast_nodes`. JSON is the bridge between the two systems.

### 7.1 `json_to_ast(node: dict) -> ast.AST`

Recursively converts a JSON dict (as output by `parse_python()`) into a Python `ast.AST` object tree. Supported node types:

| JSON `"type"` | Produces |
|---|---|
| `"Module"` | `ast.Module(body=[...], type_ignores=[])` |
| `"FunctionDef"` | `ast.FunctionDef(name, args, body, decorator_list=[], returns=None)` |
| `"arguments"` | `ast.arguments(posonlyargs=[], args=[ast.arg(arg=...)], ...)` |
| `"Assign"` | `ast.Assign(targets=[...], value=...)` |
| `"Name"` | `ast.Name(id=..., ctx=ast.Load()/ast.Store())` |
| `"Constant"` | `ast.Constant(value=...)` |
| `"BinaryOp"` / `"BinOp"` | `ast.BinOp(left, op=ast.Add()/ast.Sub(), right)` |
| `"Compare"` | `ast.Compare(left, ops=[ast.Gt()/ast.Lt()], comparators=[...])` |
| `"For"` / `"ForStatement"` | `ast.For(target, iter, body, orelse=[])` |
| `"If"` | `ast.If(test, body, orelse=[])` |
| `"WhileStatement"` | `ast.While(test, body, orelse=[])` |
| `"Break"` | `ast.Break()` |
| `"Continue"` | `ast.Continue()` |
| `"Pass"` | `ast.Pass()` |
| `"Call"` | `ast.Call(func, args, keywords=[])` |
| `"Return"` | `ast.Return(value=...)` |
| `"Tuple"` | `ast.Tuple(elts=[...], ctx=ast.Load())` |
| `"Subscript"` | `ast.Subscript(value, slice, ctx=ast.Load())` |
| `"RangeCall"` | `ast.Call(func=ast.Name("range"), args=[...])` |
| `"Expr"` | `ast.Expr(value=...)` |

**Limitation**: Only handles types needed for bubble sort; other node types raise `NotImplementedError`.

### 7.2 `SwapToTemp` (ast.NodeTransformer)

**Transforms**: `a, b = b, a` → `_tmp = a; a = b; b = _tmp`

**Logic**:
- Triggers on `Assign` where target is a `Tuple` and value is a `Tuple` of equal length
- Creates `_tmp = first_target`; then regular assignments; replaces second assignment's value with `_tmp`
- Returns a **list** of 3 `Assign` nodes (ANTLR visitor pattern: returning list from visit_* replaces node with multiple nodes)

**Why**: Tuple swaps are hard to track for the early-exit optimization and for the trajectory system.

### 7.3 `AddEarlyExit` (ast.NodeTransformer)

**Transforms**: Adds bubble sort early-exit optimization to the **outer** loop only.

**Logic** (applied per `FunctionDef`):
1. Uses inner `recurse_loops(stmts)` to find all `For` loops recursively
2. Only instruments loops that **contain another `For` loop** in their body (skips inner loops)
3. For each eligible outer loop:
   - Inserts `_swapped = False` at start of loop body
   - Uses inner `MarkSwap` transformer: if an `Assign` whose value is a `Tuple` containing any `Subscript` → marks as a swap by prepending `_swapped = True`
   - Appends `if not _swapped: break` at end of loop body

**Result**: Optimized bubble sort that exits early when no swaps occur in a pass.

### 7.4 `RenameVariables` (ast.NodeTransformer)

**Transforms**: Renames all user-defined identifiers to `v_` + 8 random alphanumeric characters.

**Logic**:
- Maintains `self.mapping: dict[str, str]` (old → new name)
- `self.ignored`: set of built-ins (`len`, `range`, `print`, `list`, `sorted`, `int`, `str`, `append`)
- `visit_FunctionDef`: renames function arguments first (registering them), then recurses
- `visit_Name`: maps any `Name.id` through `_get_new_name()`
- `_get_new_name()`: if in ignored set, returns original; otherwise generates new name if not yet mapped

**Note**: Function name itself is NOT renamed (only arguments and local variables).

### 7.5 `VariableImportanceAnalyzer` (ast.NodeVisitor)

**Purpose**: Assigns importance scores to variables based on their role in the code. Used to weight the Monte Carlo equivalence check.

**Scoring rules**:
| Event | Score added |
|---|---|
| Variable appears as a function argument | +5 |
| Variable used anywhere (Name node) | +1 |
| Variable appears as a subscript index (`arr[j]` → `j` gets +10) | +10 |
| Variable in binary index expression (`arr[j+1]` → for each Name in expression) | +10 |

Built-ins (`len`, `range`, etc.) are excluded.

**Output**: `self.scores: dict[str, int]` — e.g. `{"arr": 16, "j": 25, "n": 8, "i": 5}`.

### 7.6 `TracedList` (list subclass)

Wraps a list and records every mutation:
- `self.states: list[list]` — starts with initial copy; appends a copy on every `__setitem__`
- `deltas() -> list[list]`: returns element-wise differences between consecutive states as `[[b-a for a,b in zip(prev, curr)], ...]`

**Usage**: Run both original and obfuscated functions on the same `TracedList` to compare execution trajectories.

### 7.7 `floatify(v) -> float`

Converts any Python value to float for state-space use:
- `bool` → `1.0` / `0.0`
- `int/float` → `float(v)`
- `list/tuple/str` → `float(len(v))`
- Anything else → `0.0`

### 7.8 `get_final_coords(fn, arg) -> (result, named_coords: dict[str, float])`

Uses `sys.settrace()` to intercept the `return` event of exactly `fn` (matched by `fn.__code__` identity). At return, captures `frame.f_locals` (all local variables) and runs them through `floatify()`.

Returns:
- `result`: the actual return value of `fn(arg)`
- `named_coords`: `{var_name: float_value}` for all locals at return time

### 7.9 `monte_carlo_equivalence(fn1, fn2, importance_scores, weighted_threshold=0.8, max_samples=300, confidence_threshold=50) -> dict`

**Algorithm**:
1. For each random input (list of 1–10 random ints in [-30, 30]):
   - Run both `fn1` and `fn2` with `get_final_coords()`
   - If return values differ: immediately return `{equivalent: False}`
   - Build/refine `candidates: dict[fn1_var → set[fn2_vars]]` by intersecting sets of fn2 vars whose float value matches fn1 var's float value (via `math.isclose`)
   - Calculate **importance-weighted match ratio**: sum of importance scores for fn1 vars that have at least one candidate in fn2, divided by total importance
   - If ratio ≥ `weighted_threshold` for `confidence_threshold` consecutive samples → return `{equivalent: True}`

**Returns dict**:
```python
{
  "equivalent": bool,
  "confidence": int,           # consecutive confirmations achieved
  "samples_used": int,
  "named_mapping": [           # list of (fn1_var, fn2_var, last_value, importance_score)
      (str, str, float, int), ...
  ],
  "mismatch_input": list,      # input that caused failure, or None
  "match_ratio": float         # final weighted match ratio
}
```

**Fallback without `importance_scores`**: uses simple count ratio (matched / total candidates).

### 7.10 `rewrite_and_test(json_ast: dict) -> dict`

Master orchestrator. Steps:
1. `json_to_ast(json_ast)` + `ast.fix_missing_locations()`
2. `VariableImportanceAnalyzer().visit(tree)` → importance scores
3. Deep copy tree; apply `AddEarlyExit`, `SwapToTemp`, `RenameVariables` in sequence
4. `ast.fix_missing_locations()` on transformed tree
5. `ast.unparse()` both trees → source strings; dump to `debug_poc.txt`
6. `exec()` both source strings; extract function objects from namespaces
7. Fuzz test 300 random inputs: fail if outputs differ or differ from `sorted(arr)`
8. Run `TracedList` trajectory on sample `[5, 2, 9, 1, 5, 6]`
9. `monte_carlo_equivalence()` with importance scores
10. Return result dict with `pass`, `src_orig`, `src_rewr`, `traj_orig`, `traj_rewr`, `out`, `equivalence`, `importance_scores`

**`__main__` block**: defines a bubble sort as a hardcoded JSON AST dict, runs `rewrite_and_test()`, and prints the equivalence report including matched/unmatched variable mapping.

---

## 8. Module: `vectorizer/vectorize_poc.py`

**Role**: Alternate representation path. Given a JSON AST (output of `parse_python()`), evaluates it interpretively and records a multidimensional execution trajectory. Does NOT use `POC.py` or stdlib `ast`.

### 8.1 Core Classes

| Class | Fields | Purpose |
|---|---|---|
| `VectorSpace` | `dimensions: List[Dimension]` | Container; `add_dimension()`, `get_dimension_by_name()` (auto-creates) |
| `Dimension` | `name: str`, `dim_type: str`, `values: dict[int, float]` | One axis; `values[exec_pos] = float` |
| `VectorCordinate` | `vector_space`, `execution_position: int` | Point at step N; `set_dimension_value(dim_name, value)` |
| `ExecutionTrajectory` | inherits `VectorSpace` | The full program trace |

### 8.2 `json_ast_to_vector_space_eval(json_ast: dict) -> ExecutionTrajectory`

Recursively walks a JSON AST dict and simulates execution, recording into a `VectorSpace`:

| Node type | Action |
|---|---|
| `"Constant"` | Records float value under `"Const"` dimension |
| `"Name"` | Looks up identifier in `env` dict; records under `"Var_{id}"` dimension |
| `"BinaryOp"` | Evaluates left + right; records result under `"Return"` dimension |
| `"Call"` | Evaluates args (each recorded under `"Arg"`); calls user-defined fn or simulates `sum`, `average_of_three` |
| `"Assign"` | Evaluates value; stores in `env[target_id]`; records under `"Var_{id}"` dimension |
| `"FunctionDef"` | Stores function node in env; records `"Op_FunctionDef"` dimension counter |
| `"Return"` | Evaluates value; records under `"Return"` dimension |
| `"Module"` | Iterates body statements |

**`exec_pos`** is a global counter (nonlocal) that increments at each step, forming the time axis of the trajectory.

### 8.3 Supporting Functions

| Function | Signature | Description |
|---|---|---|
| `trajectory_to_table(vs)` | `→ (table: list[list], headers: list[str])` | Pivots dimensions × steps into a 2D list. Zero-fills missing positions. |
| `save_csv(filename, table, headers)` | `→ None` | Writes trajectory table as CSV |
| `final_coordinate_sum(vs)` | `→ dict[str, float]` | Sums all values per dimension; gives a single endpoint coordinate per axis |

**Main usage** (runs on import): loads `pyparser/output/output.json`, evaluates, saves `trajectory.csv`, prints final coordinate.

---

## 9. Module: `tests/`

All tests use `parse_python()` from `pyparser/main.py` and assert the full JSON AST output dict.

### `tests_pyparser/test_functions.py` — `TestFunctionDefinition`

| Test | Input code | What it verifies |
|---|---|---|
| `test_function_def_simple` | `def foo(): return 'bar'` | Module→FunctionDef→ReturnStmt→Constant(STRING). Also checks `args`, `decorator_list`, `returns`, `async` fields |
| `test_function_with_args_and_binary_op` | `def add(x, y): return x + y` | Args appear in `defaults` list (not `args`); BinaryOp with left/operator/right |
| `test_return_function_call` | `def caller(): return target(1, 2)` | Call node with identifier Name and args as Constant(NUMBER) |

### `tests_pyparser/test_ifstatements.py` — `TestIfStatements`

| Test | Input code | What it verifies |
|---|---|---|
| `test_simple_if` | `if True: x = 1` | IfStatement with Constant(BOOLEAN), Assign body, `ifelse: None`, `else: None` |
| `test_if_else` | `if True: x=1 else: x=2` | Adds `else: {type: "ElseStatement", body: [...], test: None}` |
| `test_if_elif_else` | `if True: ... elif False: ... else: ...` | `ifelse: [{type: "ElifStatement", test: Constant(False), body: [...]}]` |
| `test_nested_if` | `if True: if False: x=1` | Nested IfStatement inside body |
| `test_complex_conditions` | `if x > 1: y = 2` | BinaryOp with operator `">"` as `test` |

---

## 10. Key Data Contracts (JSON Shapes)

### 10.1 JSON AST — Module root
```json
{
  "type": "Module",
  "body": [ ...Statement dicts... ]
}
```

### 10.2 FunctionDef
```json
{
  "type": "FunctionDef",
  "name": "bubble_sort",
  "args": {
    "args": [],
    "vararg": null,
    "kwarg": null,
    "defaults": [{"name": "arr", "annotation": null}]
  },
  "body": [ ...Statement dicts... ],
  "decorator_list": [],
  "returns": null,
  "async": false
}
```
> Note: regular args appear in `defaults`, not `args`. This is a quirk of the current visitor implementation.

### 10.3 Assign
```json
{
  "type": "Assign",
  "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
  "operator": "=",
  "value": {"type": "Constant", "value": "1", "dtype": "NUMBER"}
}
```

### 10.4 IfStatement
```json
{
  "type": "IfStatement",
  "test": {"type": "Constant", "value": true, "dtype": "BOOLEAN"},
  "body": [...],
  "ifelse": [...ElifStatement dicts...] | null,
  "else": {"type": "ElseStatement", "body": [...]} | null
}
```

### 10.5 BinaryOp
```json
{
  "type": "BinaryOp",
  "left": {"type": "Name", "id": "x", "ctx": "Load"},
  "operator": "+",
  "right": {"type": "Name", "id": "y", "ctx": "Load"}
}
```

### 10.6 Call
```json
{
  "type": "Call",
  "identifier": {"type": "Name", "id": "target", "ctx": "Load"},
  "args": [{"type": "Constant", "value": "1", "dtype": "NUMBER"}]
}
```

### 10.7 Return
```json
{
  "type": "Return",
  "value": { ...Expression dict... }
}
```

### 10.8 Loops (WhileStatement & ForStatement)

#### WhileStatement
```json
{
  "type": "WhileStatement",
  "test": { ...Expression dict... },
  "body": [ ...Statement dicts... ],
  "orelse": [ ...Statement dicts... ] | []
}
```

#### ForStatement
```json
{
  "type": "ForStatement",
  "target": { ...Expression (Name) dict... },
  "iter": { ...Expression dict... },
  "body": [ ...Statement dicts... ],
  "orelse": [ ...Statement dicts... ] | [],
  "async": false
}
```

---

## 11. Design Decisions and Known Quirks

1. **Two separate AST systems**: `obfuscrypt_base/ast_nodes.py` is used by the pyparser pipeline and produces JSON. `POC.py` uses Python's stdlib `ast` for the live obfuscation/verification pipeline. JSON is the interchange format between them.

2. **Function args quirk**: In `PythonASTVisitor.visitTypedargslist`, normal named parameters are returned via `visitDef_parameters` which calls `visitNamed_parameter`; these end up in `defaults` rather than `args` in the serialized dict. This is a known implementation simplification.

3. **POC only handles bubble sort's JSON shape**: `json_to_ast()` in `POC.py` raises `NotImplementedError` for node types beyond its hardcoded list. Extending it requires adding new `if t == "TypeName"` branches.

4. **Duplicate `visitFunctionCall`** in `powerparser/visitor.py`: Python will silently use only the second definition. The first definition (lines 28–36) is dead code.

5. **`vectorize_poc.py` runs on import**: The main block at the bottom executes immediately when the module is imported. This is intentional for the POC but will cause errors if `pyparser/output/output.json` does not exist.

6. **`trajectory.csv` shape**: Rows = execution steps; Columns = named dimensions (`Op_FunctionDef`, `Const`, `Arg`, `Var_par1`, `Var_a`, `Var_b`, `Return`, etc.). Most cells are 0 (sparse).

7. **`_swapped` and `_tmp` are injected names**: `AddEarlyExit` injects `_swapped`; `SwapToTemp` injects `_tmp`. These exist in the obfuscated code's local scope and will appear in `get_final_coords()` output.

8. **Monte Carlo candidates can be non-injective**: If two fn1 variables have identical float values across all samples, they may share the same fn2 candidate. The algorithm uses set intersection per variable, not a global bijection.

9. **Importance scores computed before transformation**: `VariableImportanceAnalyzer` runs on the *original* AST before renaming. After `RenameVariables`, old names no longer exist — but the importance dict uses old names as keys. `monte_carlo_equivalence` matches against fn1's local variable names at return time (which are the *new* obfuscated names), so the importance scores are only used for the *fn1* side's variables whose new names appear in `named_coords`.

---

## 12. Extension Points

| What to extend | Where | How |
|---|---|---|
| Support more Python AST node types in POC | `POC.py::json_to_ast()` | Add `if t == "NewType":` branch returning appropriate `ast.*` node |
| Support more Python syntax in the visitor | `pyparser/python_ast_visitor.py` | Add `visitXxx()` method for the grammar rule |
| Add a new obfuscation primitive | `POC.py` | Create new `ast.NodeTransformer` subclass; add to transformer sequence in `rewrite_and_test()` |
| Support a new language | `powerparser/` pattern | Write ANTLR grammar, generate parser, create `Visitor` subclass, map to `ast_nodes` |
| Add more vectorization dimensions | `vectorizer/vectorize_poc.py::json_ast_to_vector_space_eval()` | Add `elif ntype == "..."` blocks recording coordinates |
| Add new test cases | `tests/tests_pyparser/` | Add method to existing class or new file; use `parse_python(code)` and assert dict |
