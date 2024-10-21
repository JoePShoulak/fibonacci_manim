from manim import *
from math import sqrt

rabbit_path = "rabbit.svg"

PHI = (1+sqrt(5))/2
RABBIT_SIZE = 1

def rabbitsSvg():
    rabbit = SVGMobject(rabbit_path, height=RABBIT_SIZE, fill_color=WHITE, stroke_color=BLACK, stroke_width=5, stroke_opacity=1)
    return VGroup(
        rabbit.copy().scale(0.9),
        rabbit.copy().shift(DOWN*0.1*RABBIT_SIZE, LEFT*0.2*RABBIT_SIZE),
    )
    
class Rabbit:
    def __init__(self, adult=False):
        self.adult = adult
        self.image = self.get_image()

    def get_image(self):
        image = rabbitsSvg()
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

class Rabbits(MovingCameraScene):
    def construct(self):
        scene_width = config.frame_width
        scene_height = config.frame_height 

        tree = RabbitTree()
        tree.iterate(4)
        allRows = VGroup()

        def center_camera():
            return self.camera.frame.animate.move_to(allRows.get_center())

        def animateIteration(n, allRows):
            allRows += tree.get_generation_as_vgroup(n).next_to(allRows[-1], DOWN)
            i = 0
            for r, mob in zip(tree.get_generation(n-1), allRows[-2].submobjects):
                if r.data.adult:
                    print("yes")
                    self.play(Transform(VGroup(mob.copy(), mob.copy()), allRows[-1][i:i+2]), center_camera())
                    i += 2
                else:
                    print("no")
                    self.play(Transform(VGroup(mob.copy()), allRows[-1][i]), center_camera())
                    i += 1

        allRows += tree.get_generation_as_vgroup(1)
        self.play(Write(allRows[0]))

        print("it start")
        animateIteration(2, allRows)
        print("it start")
        animateIteration(3, allRows)
        print("it start")
        animateIteration(4, allRows)
        print("it start")
        animateIteration(5, allRows)
