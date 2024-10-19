from manim import *

# line thicknesses
THIN = 1.25
THICK = 3
STEM = 4

# region ERRORS
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
# endregion
  
# region META
class NoteData:
  def __init__(self, duration, vMobj):
    self.duration = duration
    self.vMobj = vMobj

  def __add__(self, note):
    return self.duration + note.duration
  
  def __radd__(self, n):
    return self.duration + n
    
# endregion

class NoteHead(VMobject):
  def __init__(self, size, open=False, **kwargs):
    super().__init__(**kwargs)

    if open:
      headOuter = Ellipse(1.618, 1, color=WHITE).set_opacity(1)
      headInner = Ellipse(1.618, 0.618, color=WHITE, stroke_width=1)
      headInner.set_opacity(1).set_fill(BLACK)

      self.add(headOuter, headInner)
    else:
      self.add(Ellipse(1.618, 1, color=WHITE).set_opacity(1))

    self.rotate(22 * DEGREES).scale_to_fit_height(size).center()

class NoteStem(VMobject):
  def __init__(self, size, head, **kwargs):
    super().__init__(**kwargs)

    self.become(Line([0, 0, 0], [0, size*3, 0], stroke_width=STEM))
    self.align_to(head, DR).shift(UP*(2/3)*size)

class Note(VMobject):
  def __init__(self, size, openHead=False, stem=True, **kwargs):
    super().__init__(**kwargs)

    self.become(NoteHead(size, openHead))
    if stem:
      self.add(NoteStem(size, self))

class QuarterNote(VMobject):
  def __init__(self, size, **kwargs):
    super().__init__(**kwargs)
    self.become(Note(size))

class HalfNote(VMobject):
  def __init__(self, size, **kwargs):
    super().__init__(**kwargs)
    self.become(Note(size, openHead=True))

class WholeNote(VMobject):
  def __init__(self, size, **kwargs):
    super().__init__(**kwargs)
    self.become(Note(size, openHead=True, stem=False))

class NoteTypes:
  WHOLE = NoteData(4, WholeNote)
  HALF = NoteData(2, HalfNote)
  QUARTER = NoteData(1, QuarterNote)
  # WHOLE = 4
  # HALF = 2
  # QUARTER = 1

class Measure(VMobject):
  def __init__(self, notes=[], time_signature=[4,4], width=False, **kwargs):
    super().__init__(**kwargs)
    self.add(makeMeasure(notes, time_signature, width))

def makeMeasure(notes=[], time_signature=[4,4], width=False):
  # note lines
  if not width:
    width = max(time_signature[0], 2)

  nLines = VGroup(
    *[Line([-width/2, 0, 0], [width/2, 0, 0], stroke_width=THIN) for i in range(5)]
  ).arrange(DOWN)

  nLineSpacing = nLines[0].get_start()[1] - nLines[1].get_start()[1]

  # bar lines
  barLines = VGroup(*[
    Line(nLines[0].get_start(), nLines[4].get_start(), stroke_width=THIN), 
    Line(nLines[0].get_end(), nLines[4].get_end(), stroke_width=THIN).shift(LEFT*0.125), 
    Line(nLines[0].get_end(), nLines[4].get_end(), stroke_width=THICK)
  ])

  # time signature
  signature = VGroup(
    *[MathTex(time_signature[i]).scale_to_fit_height(2*nLineSpacing) for i in [0, 1]]
  )
  signature[1].align_to(nLines[-1].get_start(), DL)
  signature[0].next_to(signature[1], UP, buff=0).align_to(signature)

  # notes
  xLeft = signature[0].get_edge_center(RIGHT)[0]
  xRight = barLines[1].get_edge_center(LEFT)[0]
  noteRegionWidth = xRight - xLeft
  x0 = signature[0].get_corner(UR)[0]

  noteMobjs = []

  if len(notes):
    duration = 0
    beatFactor = time_signature[1]/4
    measureLength = time_signature[0]/beatFactor
    k = 0 # offset, used for spacing notes correctly

    for i, note in enumerate(notes):
      if note.duration == measureLength:
        x = x0 + noteRegionWidth/2
      else:
        x = x0 + (i+k+1)*noteRegionWidth/(width+1)
      
      noteMobj = note.vMobj(nLineSpacing)
      duration += note.duration * beatFactor
        
      if duration > time_signature[0]: 
        raise(TooManyBeats(duration, time_signature[0]))
        
      noteMobjs += noteMobj.move_to([x, 0, 0]).align_to(nLines[2], DOWN).shift(DOWN*nLineSpacing/2)

    if duration < time_signature[0]:
      raise(NotEnoughBeats(duration, time_signature[0]))
    
    return VGroup(nLines, barLines, signature, VGroup(*noteMobjs)).center()
      
  return VGroup(nLines, barLines, signature).center()
