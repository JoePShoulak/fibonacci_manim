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

  return reducedNoteOptions

class Music(Scene):
  def construct(self):
    measureGroups = []

    for i in range(5):
      signature = [i, 4]

      measures = VGroup(
        *[Measure(m, signature) for m in fibonacciNotes(signature)]
      ).arrange(LEFT)
      if i == 4: measures.scale(0.6)
      measures.center().to_edge(UP)
      measureGroups += [measures]

      self.play(Write(measureGroups[-1]), reverse=True)

      anim = measureGroups[-1].animate

      if i == 0:
        anim.scale(0.6).to_corner(UL).shift(DOWN*2)
      elif i == 4:
        anim.next_to(measureGroups[-2], DOWN).to_edge(LEFT)
      else:
        anim.scale(0.6).next_to(measureGroups[-2], DOWN).to_edge(LEFT)

      self.play(anim.shift(RIGHT * 0.25))
      self.play(Write(MathTex(len(measures)).next_to(measures[-1].noteLines[2], LEFT)))

    self.wait()
    