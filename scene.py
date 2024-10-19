from manim import *
from music import *
import itertools

def chooseKFromArray(k, array):
  result = [*array]
  result = [list(i) for i in list(itertools.product(array, result))]

  for _ in range(k-2):
    result = [[*i[:-1], *i[-1]] for i in list(itertools.product(array, result))]

  return result

class Music(Scene):
  def construct(self):
    # self.add(makeMeasure([])) # too few error
    # self.add(makeMeasure([Note.WHOLE, Note.WHOLE])) # too many error
    # self.add(makeMeasure(["glorm"])) # invalid error

    noteOptions = []
    noteList = [Note.HALF, Note.QUARTER, 0]

    for noteOption in chooseKFromArray(4, noteList):
      if not sum(noteOption) == 4:
        pass
      else:
        noteOptions += [list(filter(lambda n: n != 0, noteOption))]

    reducedNoteOptions = []
    [reducedNoteOptions.append(x) for x in noteOptions if x not in reducedNoteOptions]

    staves = VGroup(*[makeMeasure(notes) for notes in reducedNoteOptions])
    staves.arrange(UP).center().scale(0.8)
    self.add(staves)
