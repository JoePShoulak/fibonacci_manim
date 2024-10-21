from manim import *

class Test(Scene):
  def constrcut(self):
    # t = TexTemplate()
    # t.add_to_preamble(r"\usepackage(marvosym)")

    self.Write(Square())

    self.wait()
