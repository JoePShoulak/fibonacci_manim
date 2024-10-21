from manim import *

class Test(MovingCameraScene):
  def construct(self):
    squares = VGroup(Square(1))

    def cameraUpdater(mobj):
      mobj.move_to(squares.get_center())

    def makeItMove(mobj):
      return mobj.move_to(squares.get_center())

    # self.camera.frame.add_updater(cameraUpdater)

    self.play(Write(squares[0]))

    for i in range(5):
      squares += Square(1).next_to(squares[-1], DOWN)
      self.play(Write(squares[-1]), makeItMove(self.camera.frame.animate))
