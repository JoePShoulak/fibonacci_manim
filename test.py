from manim import *

class Test(Scene):
  def constrcut(self):
    s = Square()
    s.foo = True
    print(s.foo)
    self.add(s)
    if s.foo:
      print("Test")
