from manim import *
from sheet_music import *

class Music(Scene):
  def construct(self):
    noteOptions = []
    potentialNotes = [Note.HALF, Note.QUARTER, 0]

    for n1 in potentialNotes:
      for n2 in potentialNotes:
        for n3 in potentialNotes:
          for n4 in potentialNotes:
            if not n1 + n2 + n3 + n4 == 4:
              pass
            else:
              options = [n1, n2, n3, n4]
              noteOptions += [list(filter(lambda n: n != 0, options))]

    reducedNoteOptions = []
    [reducedNoteOptions.append(x) for x in noteOptions if x not in reducedNoteOptions]

    staves = VGroup(*[musicStaff(notes) for notes in reducedNoteOptions])
    staves.arrange(DOWN).center().scale(0.8)
    self.add(staves)
