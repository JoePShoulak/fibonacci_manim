from manim import *

# line thicknesses
THIN = 1.25
THICK = 3
STEM = 4

# TODO: consider adding more verbose output
class NotEnoughBeats(Exception):
  def __init__(self, error_beats, beats):
    self.error_beats = error_beats
    self.beats = beats

  def __str__(self):
    return f"Not enough notes were provided to fill the measure. ({self.error_beats} instead of {self.beats})"

# TODO: consider adding more verbose output
class TooManyBeats(Exception):
  def __init__(self, error_beats, beats):
    self.error_beats = error_beats
    self.beats = beats

  def __str__(self):
    return f"Too many notes were provided to fill the measure. ({self.error_beats} instead of {self.beats})"
  
# TODO: consider adding more verbose output
class InvalidNote(Exception):
  def __str__(self):
    return f"Invalid note provided"

class Note:
  WHOLE = 4
  HALF = 2
  QUARTER = 1

def makeNoteHead(size, open=False):
  if open:
    headOuter = Ellipse(1.618, 1, color=WHITE).set_opacity(1)
    headInner = Ellipse(1.618, 0.618, color=WHITE, stroke_width=1)
    headInner.set_opacity(1).set_fill(BLACK)

    head = VGroup(headOuter, headInner)
  else:
    head = Ellipse(1.618, 1, color=WHITE).set_opacity(1)

  return head.rotate(22 * DEGREES).scale_to_fit_height(size).center()

def makeNoteStem(size, head):
  stem = Line([0, 0, 0], [0, size*3, 0], stroke_width=STEM)
  return stem.align_to(head, DR).shift(UP*(2/3)*size)

def makeNote(size, openHead=False, stem=True):
  head = makeNoteHead(size, openHead)
  return (VGroup(head, makeNoteStem(size, head)) if stem else head).center()

def makeQuarterNote(size): return makeNote(size)
def makeHalfNote(size): return makeNote(size, openHead=True)
def makeWholeNote(size): return makeNote(size, openHead=True, stem=False)

def makeMeasure(notes, width=-1, time_signature=[4,4]):
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
  signature[1].align_to(nLines[-1].get_start(), DL)

  # notes
  xLeft = signature[0].get_edge_center(RIGHT)[0]
  xRight = barLines[1].get_edge_center(LEFT)[0]
  noteRegionWidth = xRight - xLeft
  x0 = signature[0].get_corner(UR)[0]

  noteMobjs = []
  duration = 0
  beatFactor = time_signature[1]/4
  k = 0 # offset, used for spacing notes correctly

  for i, note in enumerate(notes):
    noteMobj = Mobject()
    x = x0 + (i+k+1)*noteRegionWidth/(width+1)
    
    match note:
      case Note.QUARTER:
        noteMobj = makeQuarterNote(nLineSpacing).move_to([x, 0, 0])
      case Note.HALF:
        noteMobj = makeHalfNote(nLineSpacing).move_to([x, 0, 0])
        k += 1 # don't put another note right next to it
      case Note.WHOLE:
        noteMobj = makeWholeNote(nLineSpacing).move_to([x0 + noteRegionWidth/2, 0, 0])
      case _:
        raise(InvalidNote)
    
    duration += note * beatFactor
      
    if duration > time_signature[0]: 
      raise(TooManyBeats(duration, time_signature[0]))
      
    noteMobjs += noteMobj.align_to(nLines[2], DOWN).shift(DOWN*nLineSpacing/2)    

  if duration < time_signature[0]:
    raise(NotEnoughBeats(duration, time_signature[0]))
      
  return VGroup(*nLines, *barLines, *signature, *noteMobjs).center()
