"""Mechanical assertion preservation for literal test/evaluator code under -O."""
import ast,types,sys
class PreserveAssertions(ast.NodeTransformer):
 def visit_Assert(self,node):
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=self.visit(node.test)),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[self.visit(node.msg)] if node.msg else [],keywords=[]),cause=None)],orelse=[]),node)
def load(name,path):
 module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module
 tree=PreserveAssertions().visit(ast.parse(path.read_text(),filename=str(path)))
 exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),module.__dict__)
 return module
