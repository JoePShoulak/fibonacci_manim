from manim import *
from math import sqrt

rabbit_path = "rabbit.svg"

PHI = (1+sqrt(5))/2
RABBIT_SIZE = 2

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

def get_next_gen_mobs(row):
    copies = []
    for rabbit in row:
        if rabbit.height < Rabbit().get_image().height:
            copies += [rabbit.copy(), rabbit.copy()]
        else:
            copies += rabbit.copy()

    return copies

class Rabbits(MovingCameraScene):
    def construct(self):
        scene_width = config.frame_width
        scene_height = config.frame_height 

        tree = RabbitTree()

        iterations = 4

        tree.iterate(iterations)

        allRows = VGroup()

        def camera_updater_force():
            anim = self.camera.frame.animate.move_to(allRows.get_center())
                
            if allRows.height > scene_height - 1:
                anim.scale_to_fit_height(allRows.height+1)

            return anim
        
        def camera_updater(mobj):
            mobj.move_to(allRows.get_center())

        rabbits = tree.get_generation(1)
        mobjs = VGroup(*[r.data.image for r in rabbits])
        allRows += mobjs
        self.play(Write(mobjs, stroke_color=WHITE))
        self.wait()

        for i in range(1, iterations+1):
            rabbits = tree.get_generation(i+1)
            mobjs = VGroup(*[r.data.image for r in rabbits]).arrange(RIGHT).next_to(allRows[-1], DOWN)
            allRows += mobjs
            self.play(Transform(VGroup(*get_next_gen_mobs(allRows[-2])), mobjs), camera_updater_force())
            self.wait()

        self.wait()

# Fix the gact that it's not always adult rabbits that spawn off a pair