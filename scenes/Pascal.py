from manim import *

class TexHex(VMobject):
    def __init__(self, tex=Tex(), stroke_opacity=1, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.become(RegularPolygon(n=6, start_angle=30*DEGREES, color=color, stroke_opacity=stroke_opacity))
        self.tex = tex
        self.add(self.tex)

    def update_tex(self, tex):
        self.tex = tex.move_to(self.get_center())

def hexRow(length):
    return VGroup(*[TexHex() for _ in range(length)]).arrange(RIGHT, buff=0)

def hexPyramid(rows):
    pyramid = VGroup()
    for i in range(rows):
        pyramid += hexRow(i + 1)
    return pyramid.arrange(DOWN, buff=-0.5)

class Pascal(MovingCameraScene):
    def construct(self):
        scene_height = config.frame_height
        scene_width = config.frame_width
        cam = self.camera.frame

        self.wait()

        pyramid = hexPyramid(9).scale(0.4)
        self.play(Write(pyramid))

        pyramid[0][0].update_tex(Tex(1))
        self.play(Write(pyramid[0][0].tex))

        zeroHat = VGroup()
        for row in pyramid:
            zeroHat += TexHex(Tex(0, fill_opacity=0.5).scale(10/4), stroke_opacity=0.5).scale(0.4).next_to(row, LEFT, buff=0)
            zeroHat += TexHex(Tex(0, fill_opacity=0.5).scale(10/4), stroke_opacity=0.5).scale(0.4).next_to(row, RIGHT, buff=0)

        self.play(cam.animate.scale(0.3).move_to(pyramid[1][1].get_edge_center(LEFT)))
        self.play(Write(zeroHat))

        pyramid[1][0].update_tex(Tex("0+1").scale(0.5))
        pyramid[1][1].update_tex(Tex("1+0").scale(0.5))
        self.play(*[Write(i.tex) for i in pyramid[1]])

        self.play(Transform(pyramid[1][0].tex, Tex(1).move_to(pyramid[1][0].tex.get_center())))
        self.play(Transform(pyramid[1][1].tex, Tex(1).move_to(pyramid[1][1].tex.get_center())))

        pyramid[2][0].update_tex(Tex("0+1").scale(0.5))
        pyramid[2][1].update_tex(Tex("1+1").scale(0.5))
        pyramid[2][2].update_tex(Tex("1+0").scale(0.5))
        self.play(*[Write(i.tex) for i in pyramid[2]])

        self.play(Transform(pyramid[2][0].tex, Tex(1).move_to(pyramid[2][0].tex.get_center())))
        self.play(Transform(pyramid[2][1].tex, Tex(2).move_to(pyramid[2][1].tex.get_center())))
        self.play(Transform(pyramid[2][2].tex, Tex(1).move_to(pyramid[2][2].tex.get_center())))

        self.play(
            Unwrite(zeroHat, reverse=False),
            cam.animate.center().scale_to_fit_height(scene_height)
        )

        [pyramid[3][i].update_tex(Tex(k)) for [i, k] in enumerate([1, 3, 3, 1])]
        self.play(*[Write(i.tex) for i in pyramid[3]])

        for i in range(4, len(pyramid)):
            row = pyramid[i]
            last_row = pyramid[i-1]

            for i, hex in enumerate(row):
                if i == 0 or i == len(row) - 1:
                    hex.update_tex(Tex(1))
                else:
                    sum = int(last_row[i].tex.get_tex_string()) + int(last_row[i-1].tex.get_tex_string())
                    hex.update_tex(Tex(sum))
            self.play(*[Write(i.tex) for i in row])
        
        self.wait()

        fibHexes = VGroup()

        for i, row in enumerate(pyramid[1:]):
            fibHexes += TexHex(color=YELLOW_D if i % 2 else RED, stroke_opacity=0.75).scale(0.4).next_to(row, LEFT, buff=0)

        self.play(Write(fibHexes))

        self.wait()
