from manim import *
from music import *
import itertools

def chooseKFromArray(k, array):
  result = [*array]
  result = [list(i) for i in list(itertools.product(array, result))]

  for _ in range(k-2):
    result = [[*i[:-1], *i[-1]] for i in list(itertools.product(array, result))]

  return result

def fibonacciNotes(signature):
  noteOptions = []
  noteList = [0, Note.QUARTER, Note.HALF]

  for noteOption in chooseKFromArray(signature[0], noteList):
    if not sum(noteOption) == signature[0] * 4/signature[1]:
      pass
    else:
      noteOptions += [list(filter(lambda n: n != 0, noteOption))]

  reducedNoteOptions = []
  [reducedNoteOptions.append(x) for x in noteOptions if x not in reducedNoteOptions]

  return reducedNoteOptions

class Music(Scene):
  def construct(self):
    self.add(makeMeasure([Note.QUARTER], [1, 4]))

    # signature = [4, 4]
    # measures = VGroup(*[makeMeasure(m, signature) for m in fibonacciNotes(signature)])
    # measures.arrange(UP).center().scale(0.8)
    # self.add(measures)


