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

    mes = Measure([], [0, 4])
    num = Tex(1).next_to(mes, DOWN) # .add_updater(lambda n: n.scale_to_fit_height(0.5))
    measureGroups += [VGroup(mes, num).center().to_edge(UP)]

    self.play(Write(measureGroups[-1][0]), reverse=True)
    self.play(Write(measureGroups[-1][1]))
    self.play(measureGroups[-1].animate.scale_to_fit_height(0.8).to_corner(UL).shift(DOWN))

    for i in range(1,5):
      signature = [i, 4]
      mes = VGroup(*[Measure(m, signature) for m in fibonacciNotes(signature)])
      mes.arrange(LEFT).center()
      num = Tex(str(len(mes))).next_to(mes, DOWN)
      measureGroups += [VGroup(mes, num).center().to_edge(UP)]
      if i == 4: mes.scale(0.5).next_to(num, UP)

      self.play(Write(measureGroups[-1][0]), reverse=True)
      self.play(Write(measureGroups[-1][1]))
      self.play(measureGroups[-1].animate.scale_to_fit_height(0.8).next_to(measureGroups[-2], DOWN).to_edge(LEFT))

    self.wait()
