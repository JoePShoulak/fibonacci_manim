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
  def __init__(self, size, open=False, color=WHITE, **kwargs):
    super().__init__(**kwargs)
    head = Ellipse(1.618, 1, color=color).set_opacity(1)
    self.open = open

    if open:
      hole = Ellipse(1.618, 0.618, color=color).set_opacity(1)
      head = Cutout(head, hole, color=color, fill_opacity=1)
      
    self.become(head)
    self.rotate(21 * DEGREES).scale_to_fit_height(size)
    
  def set_color(self, color: ParsableManimColor, family: bool = True):
    if self.openHead:
      self[0].set_color(color, family)
    else:
      super().set_color(color, family)
    return self

class NoteStem(VMobject):
  def __init__(self, size, **kwargs):
    super().__init__(**kwargs)

    self.become(Line([0, 0, 0], [0, size*3, 0], stroke_width=STEM))

class Note(VMobject):
  def __init__(self, size, openHead=False, stem=True, color=WHITE, **kwargs):
    super().__init__(**kwargs)

    self.head = NoteHead(size, openHead, color=color)
    self.add(self.head)

    if stem:
      self.stem = NoteStem(size).align_to(self.head, DR).shift(UP*(2/3)*size)
      self.add(self.stem)

  def set_color(self, color: ParsableManimColor, family: bool = True):
    self.head.set_color(color, family)
    self.stem.set_color(color, family)

class QuarterNote(Note):
  def __init__(self, size=1, color=WHITE, **kwargs):
    super().__init__(size, color=color, **kwargs)

class HalfNote(Note):
  def __init__(self, size=1, color=WHITE, **kwargs):
    super().__init__(size, openHead=True, color=color, **kwargs)

class WholeNote(Note):
  def __init__(self, size=1, color=WHITE, **kwargs):
    super().__init__(size, openHead=True, stem=False, color=color, **kwargs)

class NoteTypes:
  WHOLE = NoteData(4, WholeNote)
  HALF = NoteData(2, HalfNote)
  QUARTER = NoteData(1, QuarterNote)

class Measure(VMobject):
  def __init__(self, notes=[], signature=[4,4], width=False, **kwargs):
    super().__init__(**kwargs)

    # note lines
    if not width:
      width = max(signature[0], 2)

    self.noteLines = VGroup(
      *[Line([-width/2, 0, 0], [width/2, 0, 0], stroke_width=THIN) for i in range(5)]
    ).arrange(DOWN)

    nLineSpacing = self.noteLines[0].get_start()[1] - self.noteLines[1].get_start()[1]

    # bar lines
    self.barLines = VGroup(*[
      Line(self.noteLines[0].get_start(), self.noteLines[4].get_start(), stroke_width=THIN), 
      Line(self.noteLines[0].get_end(), self.noteLines[4].get_end(), stroke_width=THIN).shift(LEFT*0.125), 
      Line(self.noteLines[0].get_end(), self.noteLines[4].get_end(), stroke_width=THICK)
    ])

    # time signature
    self.signature = VGroup(
      *[MathTex(signature[i]).scale_to_fit_height(2*nLineSpacing) for i in [0, 1]]
    )
    self.signature[1].align_to(self.noteLines[-1].get_start(), DL)
    self.signature[0].next_to(self.signature[1], UP, buff=0).align_to(self.signature)

    self.staff = VGroup(self.noteLines, self.barLines, self.signature)
    self.add(self.staff)

    # notes
    xLeft = self.signature[0].get_edge_center(RIGHT)[0]
    xRight = self.barLines[1].get_edge_center(LEFT)[0]
    noteRegionWidth = xRight - xLeft
    x0 = self.signature[0].get_corner(UR)[0]

    noteMobjs = []
    self.notes = VMobject()

    if len(notes):
      duration = 0
      beatFactor = signature[1]/4
      measureLength = signature[0]/beatFactor
      k = 0 # offset, used for spacing notes correctly

      for i, note in enumerate(notes):
        if note.duration == measureLength:
          x = x0 + noteRegionWidth/2
        else:
          x = x0 + (i+k+1)*noteRegionWidth/(width+1)

        if note.duration == NoteTypes.HALF.duration:
          k += 1
        
        noteMobj = note.vMobj(nLineSpacing)
        duration += note.duration * beatFactor
          
        if duration > signature[0]: 
          raise(TooManyBeats(duration, signature[0]))
          
        noteMobjs += noteMobj.move_to([x, 0, 0]).align_to(self.noteLines[2], DOWN).shift(DOWN*nLineSpacing/2)

      if duration < signature[0]:
        raise(NotEnoughBeats(duration, signature[0]))
      
      self.notes = VGroup(*noteMobjs)
      self.add(self.staff, self.notes)
