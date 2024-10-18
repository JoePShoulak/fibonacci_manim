from manim import *
from sheet_music import *

class Music(Scene):
  def construct(self):
    staff = musicStaff([-1, -1, -1, -1]).scale(2)

    self.add(staff)
