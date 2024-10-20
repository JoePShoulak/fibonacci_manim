from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

from music import *
from music import NoteTypes as NT
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
      """First of all, we're only going to consider time signatures where the quarter note gets the beat."""
    ):
      self.play(Write(demo[0]))
      self.wait()

    # TODO: Add transformations that match the following voiceover, so the signature changes
    
    with self.voiceover("So, 2 4,"):
      self.play(demo[0].staff.signature[1].animate.set_color(YELLOW_D))

    with self.voiceover("3 4,"):
      newMeasure = Measure(signature=[3,4]).move_to(measure.get_center())
      newMeasure.staff.signature[1].set_color(YELLOW_D)
      self.play(Transform(measure, newMeasure))

    with self.voiceover("4 4,"):
      newMeasure = Measure(signature=[4,4]).move_to(measure.get_center())
      newMeasure.staff.signature[1].set_color(YELLOW_D)
      self.play(Transform(measure, newMeasure))

    with self.voiceover("and so on. I'm choosing that mainly because we're more familiar with them."):
      newMeasure = Measure(signature=[2,4]).move_to(measure.get_center())
      self.play(Transform(measure, newMeasure))

    with self.voiceover(
      """Our only real defining rule is we're only going to use notes of two durations:
      a short and a long, which in our <bookmark mark='case'/>case would be the quarter note and the half note.
      This works for any time signature as long as the short note is the one that gets the beat,
      and the long note is twice the length of the short note."""
    ):
      self.wait_until_bookmark('case')
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

    # LAYOUT
    allMeasureGroups = []
    counts = []

    vos = [
      [
        "Not that it's a real time signature, but to make things neat, we'll start with  0 4, which can't fit any notes",
        "but there's exactly one way to do that"
      ],
      [
        "Then we'll move on to 1 4. We can only fill that with a quarter note",
        "So that's 1 as well"
      ],
      [
        "Next is 2 4, which can be two quarter notes or one half note",
        "and that's 2 ways"
      ],
      [
        "On to 3 4, which can be 3 quarter notes, a half note and a quarter note, or a quarter note and a half note",
        "that's 3 ways. Noticing anything yet?"
      ],
      [
        "finally 4 4, which can be done... all these different ways",
        "of which there are 5"
      ]
    ]

    for i in range(5):
      signature = [i, 4]

      measures = VGroup(*[Measure(m, signature) for m in fibonacciNotes(signature)])
      measures.arrange(RIGHT).scale(0.6 if i == 4 else 1).center().to_edge(UP)
      with self.voiceover(vos[i][0]):
        self.play(Write(measures))

      anim = measures.animate.scale(1 if i == 4 else 0.6)

      if allMeasureGroups:
        anim.next_to(allMeasureGroups[-1], DOWN).to_edge(LEFT)
      else:
        anim.to_corner(UL).shift(DOWN*2)

      with self.voiceover(vos[i][1]):
        self.play(anim.shift(RIGHT * 0.25))

        count = MathTex(len(measures)).next_to(measures[0].staff.noteLines[2], LEFT)
        measureCount = count
        counts += [count]

        self.play(Write(measureCount))

      allMeasureGroups += [measures]

    self.wait()

    # HIGHLIGHT
    vos = [
      [
        """Starting at the first 3 sets of measures, we can create the third by making measures from
        the ones one beat shorter""",
        """and then add another beat, which is a quarter note""",
        """Or we can take all the measures with two fewer beats (that measure happens to be empty),""",
        """but we can still add two beats, or a half note, to those and make everything in our current row"""
      ],
      [
        "Next we can take the row of 2 4",
        "Each with one additional quarter note",
        "And the row of 1 4",
        "with half notes to match, to make the row of 3 4"
      ],
      [
        "and again the 3 4 row",
        "with quarter notes each",
        "and the 2 4 row",
        "with half notes each, form the final row"
      ]
    ]

    with self.voiceover(
      """So what's going on here? Well, let's see if we can build any of these sets from
      any of the sets that came before them,
      because that's kind of how the Fibonacci numbers work, at least, generally.
      But we're trying something out! That's a big part of eventually figuring things out."""
    ):
      self.wait_for_voiceover()

    for i in range(3):
      aMeasures = allMeasureGroups[i]
      bMeasures = allMeasureGroups[i+1]
      bInspiredMeasures = allMeasureGroups[i+2][:len(bMeasures)]
      aInspiredMeasures = allMeasureGroups[i+2][len(bMeasures):]
      cMeasures = [*aInspiredMeasures, *bInspiredMeasures]

      # Show the notes from the previous measures in ours
      with self.voiceover(vos[i][0]):
        self.play(
          *[measure.animate.set_color(ORANGE) for measure in bMeasures],
          *[measure.notes[:-1].animate.set_color(ORANGE) for measure in bInspiredMeasures],
          *[measure.staff.animate.set_color(ORANGE) for measure in bInspiredMeasures]
        )
        self.wait()

      # Show the notes we add to complete them
      with self.voiceover(vos[i][1]):
        self.play(*[measure.notes[-1].animate.set_color(YELLOW) for measure in bInspiredMeasures])
        self.wait(2)

      # Show the notes from the twice-previous measures in ours
      with self.voiceover(vos[i][2]):
        self.play(
          *[measure.animate.set_color(RED) for measure in aMeasures],
          *[measure.notes[:-1].animate.set_color(RED) for measure in aInspiredMeasures],
          *[measure.staff.animate.set_color(RED) for measure in aInspiredMeasures]
        )
        self.wait()

      # Show the notes we add to complete them
      with self.voiceover(vos[i][3]):
        self.play(*[measure.notes[-1].animate.set_color(YELLOW) for measure in aInspiredMeasures])
        self.wait(2)

      # Clear everything
      self.play(*[measures.animate.set_color(WHITE) for measures in [*aMeasures, *bMeasures, *cMeasures]])
      self.wait()

    definition = MathTex(r"\text{\# of notes from\ } [", "|||", ",", "|||", r"] \text{\ in a measure of\ } ", "|||", ": F_{n+1}", font_size=55).to_edge(UP)
    definition[1].become(QuarterNote(0.2).move_to(definition[1].get_center()))
    definition[3].become(HalfNote(0.2).move_to(definition[3].get_center()))
    sig = Signature(0.4, ["n", 4]).move_to(definition[5].get_center())
    sig[0].scale(0.8)
    definition[5].become(sig)

    with self.voiceover(
      """So remember, when the Fibonacci numbers show up,
      there's usually the Fibonacci pattern at work, somewhere,
      that the next term in the sequence should relate to the sum of the previous two"""
    ):
      self.play(Write(definition))

    self.play(
      FadeOut(definition),
      *[FadeOut(mob) for mob in [*allMeasureGroups, *counts]], lag_ratio=0.5
    )
    self.wait()
