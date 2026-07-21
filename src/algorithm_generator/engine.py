import ast
import types
from typing import Any, Dict, List, Optional, Union

class ASTAlgorithmEngine:
    """
    Autonomous metaprogramming engine for generating, mutating,
    and synthesizing Python Abstract Syntax Trees (AST).
    """
    def __init__(self):
        self._mutation_rate: float = 0.15

    def build_mathematical_node(self, func_name: str, params: List[str], expr_ast: ast.expr) -> ast.Module:
        """
        Synthesizes a complete Python module AST containing a single function definition.
        """
        arguments = [ast.arg(arg=p, annotation=None) for p in params]
        args_schema = ast.arguments(
            posonlyargs=[],
            args=arguments,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        
        return_stmt = ast.Return(value=expr_ast)
        func_def = ast.FunctionDef(
            name=func_name,
            args=args_schema,
            body=[return_stmt],
            decorator_list=[],
            returns=None
        )
        
        module = ast.Module(body=[func_def], type_ignores=[])
        ast.fix_missing_locations(module)
        return module

    def mutate_operator(self, tree: ast.AST) -> ast.AST:
        """
        Traverses an AST and randomly transforms arithmetic operations
        to generate algorithmic variants.
        """
        class OperatorMutator(ast.NodeTransformer):
            def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
                self.generic_visit(node)
                # Swap Addition and Multiplication dynamically
                if isinstance(node.op, ast.Add):
                    node.op = ast.Mult()
                elif isinstance(node.op, ast.Mult):
                    node.op = ast.Add()
                return node

        mutated_tree = OperatorMutator().visit(tree)
        ast.fix_missing_locations(mutated_tree)
        return mutated_tree

    def compile_and_extract(self, module_ast: ast.Module, func_name: str) -> types.FunctionType:
        """
        Compiles an AST module directly into memory and extracts the executable function object.
        """
        byte_code = compile(module_ast, filename="<algorithm_generator>", mode="exec")
        namespace: Dict[str, Any] = {}
        exec(byte_code, namespace)
        
        if func_name not in namespace:
            raise NameError(f"Function '{func_name}' was not found in compiled AST namespace.")
            
        return namespace[func_name]
