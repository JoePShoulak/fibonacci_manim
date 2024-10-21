from manim import *

class Test(Scene):
  def constrcut(self):
    t = TexTemplate()
    t.add_to_preamble(r"\usepackage(wasysym)")

    m = MathTex(r"\male", tex_template=t)
    self.add(m)