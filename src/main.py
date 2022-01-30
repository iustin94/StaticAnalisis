import ast
import collections
import os


class CallMapper(ast.NodeVisitor):
    def __init__(self):
        self.ctx = []
        self.funcs = []
        self.calls = collections.defaultdict(dict)

    def process(self, filename):
        self.ctx = [('M', os.path.basename(filename)[:-3])]
        tree = ast.parse(open(filename).read(), filename)
        self.visit(tree)
        self.ctx.pop()

    def visit_ClassDef(self, node):
        print('ClassDef', node.name, node.lineno, self.ctx)
        self.ctx.append(('C', node.name))
        self.generic_visit(node)
        self.ctx.pop()

    def visit_FunctionDef(self, node):
        print('FunctionDef', node.name, node.lineno, self.ctx)
        self.ctx.append(('F', node.name))
        self.funcs.append('.'.join([elt[1] for elt in self.ctx]))
        self.generic_visit(node)
        self.ctx.pop()

    def try_get_id(node):
        # TODO lacks a base case
        try:
            id = node.func.id
        except AttributeError:
            try:
                id = '*.' + node.func.attr
            except Exception as e:
                id = TestTerminologyCallsHaveAnswers._GetTermCallMapper.try_get_id(node.func)

        return id

    def visit_Call(self, node):
        print('Call', vars(node.func), node.lineno, self.ctx)

        id = TestTerminologyCallsHaveAnswers._GetTermCallMapper.try_get_id(node)
        values = [arg.value for arg in node.args if type(arg) == ast.Constant]
        module = '.'.join([elt[1] for elt in self.ctx])

        if self.calls[module].get(id) is None:
            self.calls[module][id] = []

        self.calls[module][id].append(values)
        self.generic_visit(node)

