from manim import *
from music import Measure, NoteTypes as NT
import itertools

def chooseKFromArray(k, array):
  result = [*array]
  result = [list(i) for i in list(itertools.product(array, result))]

  for _ in range(k-2):
    result = [[*i[:-1], *i[-1]] for i in list(itertools.product(array, result))]

  return result

def fibonacciNotes(signature):
  noteOptions = []
  noteList = [0, NT.QUARTER, NT.HALF]

  for noteOption in chooseKFromArray(signature[0], noteList):
    if not sum(noteOption) == signature[0] * 4/signature[1]:
      pass
    else:
      noteOptions += [list(filter(lambda n: n != 0, noteOption))]

  reducedNoteOptions = []
  [reducedNoteOptions.append(x) for x in noteOptions if x not in reducedNoteOptions]

  return reversed(reducedNoteOptions)

class Music(Scene):
  def construct(self):
    # LAYOUT
    allMeasureGroups = []

    for i in range(5):
      signature = [i, 4]

      measures = VGroup(*[Measure(m, signature) for m in fibonacciNotes(signature)])
      measures.arrange(RIGHT).scale(0.6 if i == 4 else 1).center().to_edge(UP)
      self.play(Write(measures))

      anim = measures.animate.scale(1 if i == 4 else 0.6)

      if allMeasureGroups:
        anim.next_to(allMeasureGroups[-1], DOWN).to_edge(LEFT)
      else:
        anim.to_corner(UL).shift(DOWN*2)

      self.play(anim.shift(RIGHT * 0.25))
      measureCount = MathTex(len(measures)).next_to(measures[0].noteLines[2], LEFT)
      self.play(Write(measureCount))

      allMeasureGroups += [measures]

    self.wait()

    # HIGHLIGHT
    for i in range(3):
      aMeasures = allMeasureGroups[i]
      
