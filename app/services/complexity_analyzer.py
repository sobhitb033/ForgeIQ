import ast


class ComplexityAnalyzer(ast.NodeVisitor):

    def __init__(self):

        self.complexity = 1

    def visit_If(self, node):

        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):

        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):

        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):

        self.complexity += len(node.handlers)
        self.generic_visit(node)

    def visit_BoolOp(self, node):

        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Match(self, node):

        self.complexity += len(node.cases)
        self.generic_visit(node)

    @staticmethod
    def analyze(function_node):

        analyzer = ComplexityAnalyzer()

        analyzer.visit(function_node)

        return analyzer.complexity