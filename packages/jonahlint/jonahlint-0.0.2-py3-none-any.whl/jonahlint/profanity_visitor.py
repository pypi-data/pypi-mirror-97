import ast
from typing import Any, Union

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_ast_checker import (
    FunctionNameChecker, FunctionVariableNameChecker, ClassNameChecker
)


class ProfanityVisitor(ast.NodeVisitor):

    def __init__(self, profanity_checker: ProfanityChecker):
        self.reports_list = []
        self.function_name_checker = FunctionNameChecker(
            profanity_checker=profanity_checker
        )
        self.function_variable_name_checker = FunctionVariableNameChecker(
            profanity_checker=profanity_checker
        )
        self.class_name_checker = ClassNameChecker(
            profanity_checker=profanity_checker
        )
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        return self.visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        return self.visit_function(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.reports_list.extend(self.class_name_checker.check(node))
        return self.generic_visit(node)

    def visit_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        self.reports_list.extend(self.function_name_checker.check(node))
        self.reports_list.extend(self.function_variable_name_checker.check(node))
        return self.generic_visit(node)

    def clear_reports_list(self):
        self.reports_list.clear()
