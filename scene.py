from manim import *


def musicStaff():
  THIN = 1.25
  THICK = 2.5

  # note lines
  noteLines = []

  for i in range(5):
    line = Line(LEFT, RIGHT, stroke_width=THIN)

    if i != 0: line.next_to(noteLines[-1], DOWN)

    noteLines += line

  # bar lines
  barLines = [
    Line(noteLines[0].get_start(), noteLines[4].get_start(), stroke_width=THIN), 
    Line(noteLines[0].get_end(), noteLines[4].get_end(), stroke_width=THIN).shift(LEFT*0.125), 
    Line(noteLines[0].get_end(), noteLines[4].get_end(), stroke_width=THICK)
  ]

  return VGroup(*noteLines, *barLines)

class Music(Scene):
  def construct(self):
    staff = musicStaff()

    self.add(staff)
