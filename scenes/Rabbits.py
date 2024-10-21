from manim import *
from math import sqrt

PHI = (1+sqrt(5))/2
RABBIT_SIZE = 2
rabbit_path = "rabbit.svg"
rabbitSVG = SVGMobject(rabbit_path, height=RABBIT_SIZE, fill_color=WHITE, stroke_color=BLACK, stroke_width=5, stroke_opacity=1)

# Helper classes
class Rabbit:
    def __init__(self, adult=False):
        self.adult = adult
        self.image = self.get_image()

    def get_image(self):
        image = VGroup(
            rabbitSVG.copy().scale(0.9),
            rabbitSVG.copy().shift(DOWN*0.1*RABBIT_SIZE, LEFT*0.2*RABBIT_SIZE),
        )
        if not self.adult: image.scale(1/PHI)
        return image
    
class NoRoomForChildren(Exception):
    def __str__(self): "No room for child in node"
    
class RabbitTree:
    def __init__(self):
        self.left: RabbitTree = None
        self.right: RabbitTree = None
        self.data = Rabbit()

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
    
    def add_child(self, adult=False):
        if self.left and self.right: raise NoRoomForChildren
        branch = "right" if self.left else "left"
        setattr(self, branch, RabbitTree())
        getattr(self, branch).data = Rabbit(adult)
    
    def iterate(self, n=1):
        if not n: return

        for leaf in self.get_leaves():
            leaf.add_child(adult=True)
            if leaf.data.adult:
                leaf.add_child()

        self.iterate(n-1)

# Main
class Rabbits(MovingCameraScene):
    def construct(self):
        # Setup
        scene_width = config.frame_width
        scene_height = config.frame_height 

        tree = RabbitTree()
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
            allRows += tree.get_generation_as_vgroup(n).next_to(allRows[-1], DOWN)
            if skip_animation: return

            i = 0
            for r, mob in zip(tree.get_generation(n-1), allRows[-2].submobjects):
                if r.data.adult:
                    self.play(Transform(VGroup(mob.copy(), mob.copy()), allRows[-1][i:i+2]), update_camera())
                    self.wait()
                    i += 2
                else:
                    self.play(Transform(VGroup(mob.copy()), allRows[-1][i]), update_camera())
                    self.wait()
                    i += 1

        # Layout
        allRows += tree.get_generation_as_vgroup(1)
        self.play(Write(allRows[0]))

        animateIteration(2, allRows)
        animateIteration(3, allRows)
        animateIteration(4, allRows)
        animateIteration(5, allRows)
        animateIteration(6, allRows, skip_animation=True)
        animateIteration(7, allRows, skip_animation=True)
        animateIteration(8, allRows, skip_animation=True)
        animateIteration(9, allRows, skip_animation=True)

        tempH, tempC = self.camera.frame.height, self.camera.frame.get_center()
        self.play(update_camera(), FadeIn(allRows[5:]))
        self.wait()

        self.play(self.camera.frame.animate.scale_to_fit_height(tempH).move_to(tempC), FadeOut(allRows[5:]))
        self.wait()

        # Animation
        for i in range(3):
            self.play(allRows[i+1].animate.set_fill_color(RED), allRows[i+2][:len(allRows[i+1])].animate.set_fill_color(RED))
            self.play(allRows[i].animate.set_fill_color(YELLOW_D), allRows[i+2][len(allRows[i+1]):].animate.set_fill_color(YELLOW_D))
            self.play(allRows[:5].animate.set_fill_color(WHITE))
            self.wait()
