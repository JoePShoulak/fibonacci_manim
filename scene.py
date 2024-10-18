from manim import *

# line thicknesses
THIN = 1.25
THICK = 3
STEM = 4

def quarterNote(noteLineSpacing):
  head = Ellipse(1.618, 1, color=WHITE).set_opacity(1)
  head.rotate(22 * DEGREES).scale_to_fit_height(noteLineSpacing)

  stem = Line([0, 0, 0], [0, noteLineSpacing*3, 0], stroke_width=STEM)
  stem.align_to(head, DR).shift(UP*(2/3)*noteLineSpacing)

  return VGroup(head, stem).center()

def musicStaff(signature=[4,4]):
  # note lines
  nLines = [Line(LEFT, RIGHT, stroke_width=THIN) for i in range(5)]

  for i in range(1, len(nLines)):
      nLines[i].next_to(nLines[i-1], DOWN)

  nLineSpacing = nLines[0].get_start()[1] - nLines[1].get_start()[1]

  # bar lines
  barLines = [
    Line(nLines[0].get_start(), nLines[4].get_start(), stroke_width=THIN), 
    Line(nLines[0].get_end(), nLines[4].get_end(), stroke_width=THIN).shift(LEFT*0.125), 
    Line(nLines[0].get_end(), nLines[4].get_end(), stroke_width=THICK)
  ]

  # time signature
  signature = [MathTex(signature[i]).scale_to_fit_height(2*nLineSpacing) for i in [0, 1]]
  signature[0].align_to(nLines[0].get_start(), UL)
  signature[1].next_to(signature[0], DOWN, buff=0)

  note = quarterNote(nLineSpacing).align_to(nLines[3], DOWN)

  return VGroup(*nLines, *barLines, *signature, note).center()

class Music(Scene):
  def construct(self):
    staff = musicStaff().scale(3)

    self.add(staff)
