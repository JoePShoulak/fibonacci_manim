from manim import *
from music_score import *
from music_score import NoteTypes as NT

# class MeasureTest(Scene):
#   def construct(self):
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
    # self.add(Measure([NT.QUARTER, NT.HALF, NT.QUARTER]).scale(3))
    # self.add(Measure([NT.QUARTER, NT.QUARTER], signature=[4, 8]).scale(3))
    # self.add(Measure([NT.QUARTER, NT.QUARTER, NT.QUARTER, NT.QUARTER], signature=[8, 8]).scale(3))

# class Test(Scene):
#   def construct(self):
#     t = Tex(r"\genfrac{}{}{0pt}{}{1}{2}")
#     self.add(Write(t))

class Test2(Scene):
  def construct(self):
    # t = Tex("N", "+", "N", "=", "N")
    # self.add(t)
    
    # self.play(
    #   t[0].animate.become(Triangle().move_to(t[0].get_center()).scale_to_fit_width(t[0].width)),
    #   t[2].animate.become(Square().move_to(t[2].get_center()).scale_to_fit_width(t[2].width)),
    #   t[4].animate.become(Circle().move_to(t[4].get_center()).scale_to_fit_width(t[4].width))
    # )

    definition = MathTex(r"\text{\# of notes from\ } [", "|||", ",", "|||", r"] \text{\ in a measure of\ } \frac{n}{4}: F_{n+1}", font_size=55).to_edge(UP)
    definition[1].become(QuarterNote(0.2).move_to(definition[1].get_center()))
    definition[3].become(HalfNote(0.2).move_to(definition[3].get_center()))
    self.play(Write(definition))