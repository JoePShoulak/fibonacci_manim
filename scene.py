from manim import *

def musicStaff(signature=[4,4]):
  THIN = 1.25
  THICK = 2.5

  # note lines
  noteLines = [Line(LEFT, RIGHT, stroke_width=THIN) for i in range(5)]

  for i in range(1, len(noteLines)):
      noteLines[i].next_to(noteLines[i-1], DOWN)

  # bar lines
  barLines = [
    Line(noteLines[0].get_start(), noteLines[4].get_start(), stroke_width=THIN), 
    Line(noteLines[0].get_end(), noteLines[4].get_end(), stroke_width=THIN).shift(LEFT*0.125), 
    Line(noteLines[0].get_end(), noteLines[4].get_end(), stroke_width=THICK)
  ]

  # time signature
  numHeight = noteLines[0].get_start()[1] - noteLines[2].get_start()[1]
  signature = [MathTex(signature[i]).scale_to_fit_height(numHeight) for i in [0, 1]]
  signature[0].align_to(noteLines[0].get_start(), UL)
  signature[1].next_to(signature[0], DOWN, buff=0)

  return VGroup(*noteLines, *barLines, *signature)

class Music(Scene):
  def construct(self):
    staff = musicStaff()

    self.add(staff)
