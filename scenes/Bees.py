from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from math import sqrt

PHI = (1+sqrt(5))/2

# Helper classes
class Bee:
    def __init__(self, female=False):
        self.female = female
        self.image = self.get_image()

    def get_image(self):
        return SVGMobject("bee.svg").set_color(RED if self.female else YELLOW_D)
    
class NoRoomForChildren(Exception):
    def __str__(self): "No room for child in node"
    
class BeeTree:
    def __init__(self):
        self.left: BeeTree = None
        self.right: BeeTree = None
        self.data = Bee()

    def get_generation(self, n):
        if n == 1: return [self]
        
        generation = []
        if self.left: generation += self.left.get_generation(n - 1)
        if self.right: generation += self.right.get_generation(n - 1)
        return generation
    
    def get_generation_as_vgroup(self, n):
        return VGroup(*[rabbit.data.get_image() for rabbit in self.get_generation(n)]).arrange(RIGHT)

    def get_leaves(self):
        if self.is_leaf():
            return [self]
        
        leaves = []
        if self.left: leaves += [*self.left.get_leaves()]
        if self.right: leaves += [*self.right.get_leaves()]
        return leaves

    def is_leaf(self):
        return not self.left and not self.right

    def get_children(self):
        children = []
        if self.left: children.append(self.left)
        if self.right: children.append(self.right)
        return children
    
    def add_child(self, female=False):
        if self.left and self.right: raise NoRoomForChildren
        branch = "right" if self.left else "left"
        setattr(self, branch, BeeTree())
        getattr(self, branch).data = Bee(female)
    
    def iterate(self, n=1):
        if not n: return

        for leaf in self.get_leaves():
            leaf.add_child(female=True)
            if leaf.data.female:
                leaf.add_child()

        self.iterate(n-1)

# Main
class Bees(VoiceoverScene, MovingCameraScene):
  def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-AriaNeural",
                style="newscast-casual"
            )
        )
        # Setup
        scene_width = config.frame_width
        scene_height = config.frame_height 

        tree = BeeTree()
        tree.iterate(9)
        allRows = VGroup()

        # Helpers
        def update_camera():
            anim = self.camera.frame.animate.move_to(allRows.get_center())

            if allRows.width > scene_width - 1:
                return anim.scale_to_fit_width(allRows.width + 1)
            if allRows.height > scene_height - 1:
                return anim.scale_to_fit_height(allRows.height + 1)

            return anim

        def animateIteration(n, allRows, skip_animation=False):
            allRows += tree.get_generation_as_vgroup(n).next_to(allRows[-1], UP)
            if skip_animation: return

            i = 0
            anim = [update_camera()]
            for r, mob in zip(tree.get_generation(n-1), allRows[-2].submobjects):
                if r.data.female:
                    anim += [Transform(VGroup(mob.copy(), mob.copy()), allRows[-1][i:i+2])]
                    self.wait()
                    i += 2
                else:
                    anim += [Transform(VGroup(mob.copy()), allRows[-1][i])]
                    self.wait()
                    i += 1

            return anim

        # Intro
        with self.voiceover(
            """Now, I know what you're thinking, and being allergic to them myself, I'm not a huge fan of bees either.
            But this pattern is really cool, because it's basically the rabbit pattern but upside down."""
        ):
            title = Text("...Bees? BEES!!!", font_size=55).to_edge(UP)
            self.play(Write(title))
            self.wait()

        maleRuleBot = Bee(female=False).get_image().scale(0.5)
        maleRuleTop = Bee(female=True).get_image().scale(0.5)
        maleRule = VGroup(maleRuleTop, maleRuleBot).arrange(DOWN, buff=1)
        maleLine = Line(maleRuleTop.get_edge_center(DOWN), maleRuleBot.get_edge_center(UP)).scale(1/PHI)
        maleRule += maleLine

        femaleRuleBot = Bee(female=True).get_image().scale(0.5)
        femaleRuleTop = VGroup(
            Bee(female=True).get_image().scale(0.5),
            Bee(female=False).get_image().scale(0.5),
        ).arrange(RIGHT)
        femaleRule = VGroup(femaleRuleTop, femaleRuleBot).arrange(DOWN, buff=1)
        femaleLine = Line(femaleRuleTop.get_edge_center(DOWN), femaleRuleBot.get_edge_center(UP)).scale(1/PHI)
        femaleRule += femaleLine

        with self.voiceover(
            """This time, we're going to start by laying out the rules."""
        ):
            self.wait_for_voiceover()

        with self.voiceover(
            """Male bees, which we'll denote in yellow, come from an unfertilized egg, so only one female parent."""
        ):
            femaleCopy = maleRule[1].copy()
            self.play(Write(maleRule[1]))
            self.wait()
            self.play(Transform(femaleCopy, maleRule[::2]))
            self.wait_for_voiceover()
            self.remove(femaleCopy)
            self.play(maleRule.animate.to_edge(LEFT))
            self.wait()

        with self.voiceover(
            """Female bees, on the other hand, come from fertilized eggs, and therefore have one parent
            of each sex. We'll color the females red."""
        ):
            femaleCopy = femaleRule[1].copy()
            self.play(Write(femaleRule[1]))
            self.wait()
            self.play(Transform(femaleCopy, femaleRule[::2]))
            self.wait_for_voiceover()
            self.remove(femaleCopy)
            self.play(femaleRule.animate.to_edge(RIGHT))
            self.wait()

        # Layout
        allRows += tree.get_generation_as_vgroup(1)
        with self.voiceover("So let's start with one male bee"):
            self.play(FadeOut(title), Write(allRows[0]))

        anim = animateIteration(2, allRows)
        with self.voiceover(
            """Because it's a male bee, it must have had one female parent"""
        ):
            self.play(*anim)
            
        anim = animateIteration(3, allRows)
        with self.voiceover(
            """This female parent must, itself, <bookmark mark='have'/>have two parents."""
        ):
            self.wait_until_bookmark('have')
            self.play(*anim[0:2])

        anim = animateIteration(4, allRows)
        with self.voiceover(
            """This grandmother bee must also have <bookmark mark='two'/>two parents,
            while the grandfather must have only <bookmark mark='one'/>one female parent"""
        ):
            self.wait_until_bookmark('two')
            self.play(*anim[0:2])
            self.wait_until_bookmark('one')
            self.play(anim[2])

        anim = animateIteration(5, allRows)
        with self.voiceover("And so on for the next generation"):
            self.play(*anim[0:2])
            self.play(anim[2])
            self.play(anim[3])
            self.wait()

        animateIteration(6, allRows, skip_animation=True)
        animateIteration(7, allRows, skip_animation=True)
        animateIteration(8, allRows, skip_animation=True)
        animateIteration(9, allRows, skip_animation=True)
        with self.voiceover("And all the ones after that"):
            tempH, tempC = self.camera.frame.height, self.camera.frame.get_center()
            self.play(update_camera(), FadeIn(allRows[5:]))
            self.wait(3)

            self.play(
                self.camera.frame.animate.scale_to_fit_height(tempH).move_to(tempC),
                FadeOut(allRows[5:]),
                FadeOut(maleRule),
                FadeOut(femaleRule)
            )
            self.wait()

        with self.voiceover(
            """The analysis of this pattern is very similar to the last one, and we have a lot more to get to,
            so let's move on."""
        ):
            self.wait_for_voiceover()

        # HACK
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.wait()
        