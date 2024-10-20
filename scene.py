from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

from music import Measure, QuarterNote, HalfNote, NoteTypes as NT
from helper import *

config.max_files_cached = -1

class Music(VoiceoverScene):
  def construct(self):
    self.set_speech_service(
      AzureService(
        voice="en-US-AriaNeural",
        style="newscast-casual"
      )
    )
            
    # QUESTION
    with self.voiceover(
      """Here's a fun question for you: how many ways can we fill up a measure of music?
      ...if we keep it a little simple"""
    ):
      title = Text("How Many Notes Can We Fit?", font_size=55).to_edge(UP)
      self.play(Write(title))
      self.wait()

    measure = Measure(signature=[2, 4])
    notes = VGroup(
        QuarterNote(measure.staff.noteSize),
        HalfNote(measure.staff.noteSize)
    ).arrange(RIGHT, buff=1)

    demo = VGroup(measure, notes).arrange(DOWN, buff=1).center()

    with self.voiceover(
      """First of all, we're only going to consider time signatures where the quarter note gets the beat.
      I'm choosing that mainly because we're more familiar with it."""
    ):
      self.play(Write(demo[0]))
      self.wait()

    with self.voiceover(
      """Our only real rule to the problem is we're only going to use two notes: a short and a long,
      which in our case would be the quarter note and the half note. This works any time the 
      short note is the one that gets the beat, and the long note is twice the length of the short note."""
    ):
      self.play(Write(demo[1]))
      self.wait()

    with self.voiceover(
      """So in this quick example, we can fit two quarter notes"""
    ):
      newMeasure = Measure(notes=[NT.QUARTER, NT.QUARTER], signature=[2, 4]).align_to(demo[0], DOWN)
      noteCopy = VGroup(*[demo[1][0].copy() for _ in range(2)])
      self.play(TransformMatchingShapes(noteCopy, newMeasure.notes))
      self.wait()

      self.play(FadeOut(newMeasure.notes))
      self.wait()

    with self.voiceover(
      """Or one half note"""
    ):
      newMeasure = Measure(notes=[NT.HALF], signature=[2, 4]).align_to(demo[0], DOWN)
      noteCopy = demo[1][1].copy()
      self.play(TransformMatchingShapes(noteCopy, newMeasure.notes))
      self.wait()

      self.play(FadeOut(newMeasure.notes))
      self.wait()

    with self.voiceover("Alright, let's go through them from the start"):
      self.play(FadeOut(title), FadeOut(demo))
      self.wait()

    return
  
    # LAYOUT
    allMeasureGroups = []
    counts = []

    vos = [
      [
        "So we'll start with time signature 0 4, which can't fit any notes",
        "but there's exactly one way to do that, I suppose"
      ],
      [
        "Then we'll move on to 1 4. We can only fill that with a quarter note",
        "So that's 1 too"
      ],
      [
        "Next is 2 4, which can be two quarter notes or one half note",
        "which is 2 ways"
      ],
      [
        "On to 3 4, which can be 3 quarter notes, a quarter note and a half note, or a half note and a quarter note",
        "that's 3 ways. Noticing anything yet?"
      ],
      [
        "and finally 4 4, which can be done... all these different ways",
        "which is 5"
      ]
    ]

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

      with self.voiceover(vos[i][0]):
        self.play(anim.shift(RIGHT * 0.25))

      count = MathTex(len(measures)).next_to(measures[0].staff.noteLines[2], LEFT)
      measureCount = count
      counts += [count]

      with self.voiceover(vos[i][1]):
        self.play(Write(measureCount))

      allMeasureGroups += [measures]

    self.wait()

    # HIGHLIGHT
    for i in range(3):
      aMeasures = allMeasureGroups[i]
      bMeasures = allMeasureGroups[i+1]
      bInspiredMeasures = allMeasureGroups[i+2][:len(bMeasures)]
      aInspiredMeasures = allMeasureGroups[i+2][len(bMeasures):]
      cMeasures = [*aInspiredMeasures, *bInspiredMeasures]

      # Show the notes from the previous measures in ours
      self.play(
        *[measure.notes.animate.set_color(ORANGE) for measure in bMeasures],
        *[measure.notes[:-1].animate.set_color(ORANGE) for measure in bInspiredMeasures]
      )
      self.wait()

      # Show the notes we add to complete them
      self.play(*[measure.notes[-1].animate.set_color(YELLOW) for measure in bInspiredMeasures])
      self.wait(2)

      # Show the notes from the twice-previous measures in ours
      self.play(
        *[measure.notes.animate.set_color(RED) for measure in aMeasures],
        *[measure.notes[:-1].animate.set_color(RED) for measure in aInspiredMeasures]
      )
      self.wait()

      # Show the notes we add to complete them
      self.play(*[measure.notes[-1].animate.set_color(YELLOW) for measure in aInspiredMeasures])
      self.wait(2)

      # Clear everything
      self.play(*[measures.animate.set_color(WHITE) for measures in [*aMeasures, *bMeasures, *cMeasures]])
      self.wait()

    self.play(*[FadeOut(mob) for mob in [*allMeasureGroups, *counts]])
    self.wait()
