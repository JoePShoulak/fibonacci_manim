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

    def mesNumUpdater(mesNum):
      mesNum[1].next_to(mesNum[0][-1].noteLines[2], LEFT).scale_to_fit_height(max(mesNum[1].height, 0.4))

    mes = VGroup(Measure([], [0, 4]))
    num = Tex(1).scale(2).next_to(mes, LEFT).next_to(mes[-1].noteLines[2], LEFT)
    mesNum = VGroup(mes, num).center().to_edge(UP).add_updater(mesNumUpdater)
    measureGroups += [mesNum]

    self.play(Write(measureGroups[-1][0]), reverse=True)
    self.play(Write(measureGroups[-1][1]))
    self.play(measureGroups[-1].animate.scale(0.6).to_corner(UL).shift(DOWN*2))

    for i in range(1,4):
      signature = [i, 4]
      mes = VGroup(*[Measure(m, signature) for m in fibonacciNotes(signature)])
      mes.arrange(LEFT).center()
      num = Tex(str(len(mes))).scale(2).next_to(mes[-1].noteLines[2], LEFT)
      mesNum = VGroup(mes, num).center().to_edge(UP).add_updater(mesNumUpdater)
      measureGroups += [mesNum]

      self.play(Write(measureGroups[-1][0]), reverse=True)
      self.play(Write(measureGroups[-1][1]))
      self.play(measureGroups[-1].animate.scale(0.6).next_to(measureGroups[-2], DOWN).to_edge(LEFT))

    mes = VGroup(*[Measure(m, [4, 4]) for m in fibonacciNotes([4, 4])])
    mes.arrange(LEFT).center().scale(0.6)
    num = Tex(str(len(mes))).scale(1.2).next_to(mes[-1].noteLines[2], LEFT)
    mesNum = VGroup(mes, num).center().to_edge(UP).add_updater(mesNumUpdater)
    measureGroups += [mesNum]

    self.play(Write(measureGroups[-1][0]), reverse=True)
    self.play(Write(measureGroups[-1][1]))
    self.play(measureGroups[-1].animate.next_to(measureGroups[-2], DOWN).to_edge(LEFT))

    self.wait()

# class Squircle(VMobject):
#   def __init__(self, **kargs):
#     super().__init__(**kargs)
#     self.add(Square())
#     self.add(Circle())

# class Test(Scene):
#   def construct(self):
#     s = Squircle()
#     self.add(s)
#     s[0].shift(LEFT)
#     print(len(s))



