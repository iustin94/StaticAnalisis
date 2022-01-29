import ast
import collections
import os


class TestTerminologyCallsHaveAnswers(object):
    class _GetTermCallMapper(ast.NodeVisitor):
        def __init__(self):
            self.ctx = []
            self.funct_name = "get_term"
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

    # This might need to run before the sanity check ? Or What would be the order between the terminologies?
    def test_calls_have_answers(self):
        # Might be an issue in the migrations file?
        # paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk("../../../") for f in filenames if
        #           os.path.splitext(f)[1] == '.py']
        paths = ["../../../../hazardlog/base/models.py"]
        missing_keys = set()

        for file in paths:
            mapper = TestTerminologyCallsHaveAnswers._GetTermCallMapper()
            mapper.process(file)
            found = []
            for node, calls in mapper.calls.items():
                for method, arguments_list_collection in calls.items():
                    if method == "get_term": #TODO make regex to match exactly
                        for values in arguments_list_collection:
                                if DEFAULT_TERM.get(values[0]) is None:
                                    missing_keys.add(values[0])
        assert len(missing_keys) == 0
