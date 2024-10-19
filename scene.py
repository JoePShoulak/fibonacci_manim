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
    
    for i in range(3):
      aMeasures = allMeasureGroups[i]
      aAnim = [measure.notes.animate.set_color(YELLOW_D) for measure in aMeasures]
      self.play(*aAnim)

      bMeasures = allMeasureGroups[i+1]
      bAnim = [measure.notes.animate.set_color(RED) for measure in bMeasures]
      self.play(*bAnim)

      cAnim = []
      cMeasures = allMeasureGroups[i+2]
      for cMeasure in cMeasures[:len(bMeasures)]:
        cAnim += [cMeasure.notes[:-2][::2].animate.set_color(RED)]
        cAnim += [cMeasure.notes[-2:][::2].animate.set_color(ORANGE)]
      for cMeasure in cMeasures[len(bMeasures):]:
        cAnim += [cMeasure.notes[:-2][::2].animate.set_color(YELLOW)]
        cAnim += [cMeasure.notes[-2:][::2].animate.set_color(ORANGE)]
      self.play(*cAnim)
      self.wait()

      self.play([measure.animate.set_color(WHITE) for measure in [*aMeasures, *bMeasures, *cMeasures]])
      self.wait()

from manim import *
from music import QuarterNote, HalfNote, NoteHead

def colorNoteAnim(note, color): # FIXME: This should be a class function somehow
  anim = []
  if len(note[0]) == 1:
    anim += [note[0].animate.set_color(color)]
  else:
    anim += [note[0][0].animate.set_color(color)]
  anim += [note[1].animate.set_color(color)]

  return AnimationGroup(*anim)

class Test(Scene):
  def construct(self):
    nHOpen = NoteHead(1, openHead=True)
    nHClosed = NoteHead(1).next_to(nHOpen, DOWN)

    self.play(Write(nHOpen), Write(nHClosed))

    self.play(nHClosed.animate.my_set_color(PINK), nHOpen.animate.my_set_color(PINK))

    self.play(FadeOut(nHClosed, nHOpen))

    noteOpen = HalfNote(1)
    self.play(Write(noteOpen))

    noteOpen.head.my_set_color(PINK)

    self.wait()

