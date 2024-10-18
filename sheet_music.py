from manim import *

# line thicknesses
THIN = 1.25
THICK = 3
STEM = 4

class Note:
  WHOLE = 0
  HALF = 1
  QUARTER = 2

def noteHead(size, open=False):
  if open:
    headOuter = Ellipse(1.618, 1, color=WHITE).set_opacity(1)
    headInner = Ellipse(1.618, 0.618, color=WHITE).set_opacity(1).set_fill(BLACK)

    head = VGroup(headOuter, headInner)
  else:
    head = Ellipse(1.618, 1, color=WHITE).set_opacity(1)

  return head.rotate(22 * DEGREES).scale_to_fit_height(size).center()

def noteStem(size, head):
  stem = Line([0, 0, 0], [0, size*3, 0], stroke_width=STEM)
  return stem.align_to(head, DR).shift(UP*(2/3)*size)

def note(size, openHead=False, stem=True):
  head = noteHead(size, openHead)
  return (VGroup(head, noteStem(size, head)) if stem else head).center()

def quarterNote(size):
  return note(size)

def halfNote(size):
  return note(size, openHead=False)

def wholeNote(size):
  return note(size, openHead=True, stem=False)

def musicStaff(notes, width=-1, time_signature=[4,4]):
  # note lines
  if width == -1: width = time_signature[0]
  nLines = [Line([-width/2, 0, 0], [width/2, 0, 0], stroke_width=THIN) for i in range(5)]

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
  signature = [MathTex(time_signature[i]).scale_to_fit_height(2*nLineSpacing) for i in [0, 1]]
  signature[0].align_to(nLines[0].get_start(), UL)
  signature[1].next_to(signature[0], DOWN, buff=0)

  # notes
  xLeft = signature[0].get_edge_center(RIGHT)[0]
  xRight = barLines[1].get_edge_center(LEFT)[0]
  noteRegionWidth = xRight - xLeft
  x1, y1, _ = signature[0].get_corner(UR)
  y2 = nLines[-1].get_center()[1]

  noteMobjs = []
  duration = 0
  beatFactor = time_signature[1]/4
  for i, note in enumerate(notes):
    if duration >= time_signature[0]: break

    if note == Note.QUARTER:
      duration += 1 * beatFactor
      x = x1 + (i+1)*noteRegionWidth/(width+1)
      noteMobjs += Line([x, y1, 0], [x, y2, 0])
    elif note == Note.HALF:
      duration += 2 * beatFactor
      x = x1 + (i+1)*noteRegionWidth/(width+1)
      noteMobjs += Line([x, y1, 0], [x, y2, 0])
    elif note == Note.WHOLE:
      duration += 4 * beatFactor
      x = x1 + noteRegionWidth/2
      noteMobjs += wholeNote(nLineSpacing).move_to([x, 0, 0]).align_to(nLines[2], DOWN).shift(DOWN*nLineSpacing/2)
    else:
      x = x1 + (i+1)*noteRegionWidth/(width+1)
      noteMobjs += Line([x, y1, 0], [x, y2, 0])
      

  return VGroup(*nLines, *barLines, *signature, *noteMobjs).center()
