import ast
from pathlib import Path

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_visitor import ProfanityVisitor


class ProfanityAnalyzer:

    @classmethod
    def analyze_source(cls, source: str, profanity_checker: ProfanityChecker):
        profanity_visitor = ProfanityVisitor(profanity_checker)
        profanity_visitor.visit(ast.parse(source))
        return profanity_visitor.reports_list

    @classmethod
    def analyze_file(cls, path: Path, profanity_checker: ProfanityChecker):
        with open(path, mode="r") as pd:
            source = pd.read()
        return cls.analyze_source(source, profanity_checker)
