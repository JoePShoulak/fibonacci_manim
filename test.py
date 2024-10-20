from manim import *
from music import *
from music import NoteTypes as NT

class Test(Scene):
  def construct(self):
    # m1 = Measure([NT.HALF, NT.QUARTER, NT.QUARTER]).scale(0.3).shift(LEFT * 4)
    # m2 = Measure([NT.QUARTER, NT.HALF, NT.QUARTER]).scale(0.3).shift(LEFT * 4)
    # m3 = Measure([NT.QUARTER, NT.QUARTER, NT.HALF]).scale(0.3).shift(LEFT * 4)
    # m4 = Measure([NT.HALF, NT.HALF]).scale(0.3).shift(LEFT * 4)
    # m5 = Measure([NT.QUARTER, NT.QUARTER, NT.QUARTER, NT.QUARTER]).scale(0.3).shift(LEFT * 4)
    # m6 = Measure([]).scale(0.3).shift(LEFT * 4)

    # ms = VGroup(m1, m2, m3, m4, m5, m6).arrange(DOWN).center().scale_to_fit_height(7)
    # self.add(ms)

    # self.add(Measure([NT.WHOLE]).scale(3))
    # self.add(Measure([NT.QUARTER, NT.QUARTER, NT.QUARTER, NT.QUARTER]).scale(3))
    self.add(Measure([NT.QUARTER, NT.HALF, NT.QUARTER]).scale(3))
    self.add(Measure([NT.QUARTER, NT.QUARTER], signature=[4, 8]).scale(3))
    # self.add(Measure([NT.QUARTER, NT.QUARTER, NT.QUARTER, NT.QUARTER], signature=[8, 8]).scale(3))
