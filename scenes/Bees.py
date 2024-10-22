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
        # with self.voiceover(
        #     """Let's start with the way Fibonacci himself talked about these numbers in his book, the Liber Abaci.
        #     How do rabbits breed? Like most problems we'll consider in this video, this is not the literal 
        #     best mathematics for tracking mammal populations, but more a metaphor for an interesting relationship
        #     of things, in this case rabbits, and the numbers that show up there."""
        # ):
        title = Text("...Bees? BEES!!!", font_size=55).to_edge(UP)
        self.play(Write(title))
        self.wait()

        maleRuleBot = Bee(female=False).get_image().scale(0.5)
        maleRuleTop = Bee(female=True).get_image().scale(0.5)
        maleRule = VGroup(maleRuleTop, maleRuleBot).arrange(DOWN, buff=1)
        maleLine = Line(maleRuleTop.get_edge_center(DOWN), maleRuleBot.get_edge_center(UP)).scale(1/PHI)
        maleRule += maleLine

        femaleRuleBot = Bee(female=False).get_image().scale(0.5)
        femaleRuleTop = VGroup(
            Bee(female=True).get_image().scale(0.5),
            Bee(female=False).get_image().scale(0.5),
        ).arrange(RIGHT)
        femaleRule = VGroup(femaleRuleTop, femaleRuleBot).arrange(DOWN, buff=1)
        femaleLine = Line(femaleRuleTop.get_edge_center(DOWN), femaleRuleBot.get_edge_center(UP)).scale(1/PHI)
        femaleRule += femaleLine

        maleCopy = maleRule[1].copy()
        self.play(Write(maleRule[1]))
        self.wait()
        self.play(Transform(maleCopy, maleRule[::2]))
        self.wait()
        self.remove(maleCopy)
        self.play(maleRule.animate.to_edge(LEFT))
        self.wait()

        femaleCopy = femaleRule[1].copy()
        self.play(Write(femaleRule[1]))
        self.wait()
        self.play(Transform(femaleCopy, femaleRule[::2]))
        self.wait()
        self.remove(femaleCopy)
        self.play(femaleRule.animate.to_edge(RIGHT))
        self.wait()


        # # Layout
        # allRows += tree.get_generation_as_vgroup(1)
        # # with self.voiceover("We'll start with one pair of young rabbits."):
        # self.play(FadeOut(title), Write(allRows[0]), Write(maleText))

        # anim = animateIteration(2, allRows)
        # # with self.voiceover(
        # #     """Because they're young, in one generation's time they simply
        # #     <bookmark mark='grow'/>grow into female rabbits."""
        # # ):
        # # self.wait_until_bookmark('grow')
        # self.play(*anim)
            
        # anim = animateIteration(3, allRows)
        # # with self.voiceover(
        # #     """As female rabbits, they <bookmark mark='survive'/> survive into the next generation,
        # #     and also breed to produce a new pair of rabbits. 
        # #     And to emphasize the fact of the metaphor here, we're not considering things like inbreeding.
        # #     We defined a simple rule, and we're seeing what happens."""
        # # ):
        # # self.wait_until_bookmark('survive')
        # self.play(*anim[0:2])

        # anim = animateIteration(4, allRows)
        # # with self.voiceover(
        # #     """Now things start getting interesting. The <bookmark mark='first'/>first pair,
        # #     being females, both survive and breed. The <bookmark mark='second'/>second pair, being young,
        # #     only grow up to become female rabbits."""
        # # ):
        # # self.wait_until_bookmark('first')
        # self.play(*anim[0:2])
        # # self.wait_until_bookmark('second')
        # self.play(anim[2])

        # anim = animateIteration(5, allRows)
        # # with self.voiceover("And so on for the next generation"):
        # self.play(*anim[0:2])
        # self.play(anim[2])
        # self.play(anim[3])
        # self.wait()

        # animateIteration(6, allRows, skip_animation=True)
        # animateIteration(7, allRows, skip_animation=True)
        # animateIteration(8, allRows, skip_animation=True)
        # animateIteration(9, allRows, skip_animation=True)
        # # with self.voiceover("And all the ones after that"):
        # tempH, tempC = self.camera.frame.height, self.camera.frame.get_center()
        # self.play(update_camera(), FadeIn(allRows[5:]))
        # self.wait(3)

        # self.play(self.camera.frame.animate.scale_to_fit_height(tempH).move_to(tempC), FadeOut(allRows[5:]))
        # self.wait()

        # Counting
        # nums = VGroup()
        # with self.voiceover("So let's count these up, and see what's going on here"):
        #     for i, row in enumerate(allRows.submobjects):
        #         if i >= 2:
        #             num = MathTex(len(row), "=", len(allRows[i-1]), "+", len(allRows[i-2]), font_size=89)
        #         else:
        #             num = MathTex(len(row), font_size=89)
        #         nums += num.next_to(row, LEFT).to_edge(LEFT).shift(LEFT * 3)

        # self.play(*[Write(num[0]) for num in nums], self.camera.frame.animate.shift(LEFT*1.5))

        # animationVOs = [
        #     [
        #         """So we know 1 plus 1 is 2, and that those are the beginning of the Fibonacci numbers,
        #         but let's make what's happening more clear.""",
        #         """We're getting one of those ones by the number of rabbits in the row previous""",
        #         """And another from the row previous to that. Okay, that's still probably not more novel,
        #         but let's think of it a slightly different way. It'll help if we see the next example first."""
        #     ],
        #     # TODO need a better explanation here
        #     [ 
        #         """So, again, 1 and 2 is 3, nothing groundbreaking here.""",
        #         """But if you think about it as actually taking these two rabbits from the row above us,""",
        #         """and the one from two rows ago, you'll see we're doing more than combining numbers, we're basically combining lists!
        #         One way of thinking about how this works is that every rabbit from one generation ago survives,
        #         and every rabbit from two generations ago produces offspring. For every rabbit two generations
        #         ago that could breed, there's one rabbit in the last generation that couldn't,
        #         which is why the number of young and female rabbits stays consistent when combining the rows.""",
        #     ],
        #     [
        #         """And again,""",
        #         """We can take these 3 rabbits from row 4,""",
        #         """and these 2 rabbits from row 3 to create row 5""",
        #     ],
        # ]

        # # Animation
        # for i in range(3):
        #     with self.voiceover(animationVOs[i][0]):
        #         self.play(
        #             nums[i+2][0].animate.set_color(ORANGE),
        #             FadeIn(nums[i+2][1:].set_color(ORANGE))
        #         )
                
        #     with self.voiceover(animationVOs[i][1]):
        #         self.play(
        #             allRows[i+1].animate.set_fill_color(RED),
        #             allRows[i+2][:len(allRows[i+1])].animate.set_fill_color(RED),
        #             nums[i+1][0].animate.set_color(RED),
        #             nums[i+2][2].animate.set_color(RED),
        #         )

        #     with self.voiceover(animationVOs[i][2]):
        #         self.play(
        #             allRows[i].animate.set_fill_color(YELLOW_D),
        #             allRows[i+2][len(allRows[i+1]):].animate.set_fill_color(YELLOW_D),
        #             nums[i][0].animate.set_color(YELLOW_D),
        #             nums[i+2][4].animate.set_color(YELLOW_D)
        #         )

        #     self.play(
        #         allRows[:5].animate.set_fill_color(WHITE),
        #         *[num[0].animate.set_color(WHITE) for num in nums],
        #         FadeOut(nums[i+2][1:])
        #     )

        #     self.wait()

        # # Outro
        # with self.voiceover(
        #     """Now that we have the most historical case out of the way, let's move into some others."""
        # ):
        #     self.wait_for_voiceover()

        # self.play(FadeOut(allRows), FadeOut(nums))
