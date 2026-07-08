from .scene import Scene

from effects import Starfield

from hud.overlay import NovaHUD





class NovaScene(Scene):


    def __init__(
            self,
            parent=None
    ):


        self.parent = parent


        self.starfield = Starfield()



        self.hud = NovaHUD()





    # ==========================================
    # ENTER
    # ==========================================

    def enter(self):


        if self.parent:


            self.hud.setParent(

                self.parent

            )


            self.hud.resize(

                self.parent.size()

            )


            self.hud.show()





    # ==========================================
    # UPDATE
    # ==========================================

    def update(
            self,
            delta
    ):


        self.starfield.update(

            delta

        )





    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):


        self.starfield.draw()





    # ==========================================
    # EXIT
    # ==========================================

    def exit(self):


        self.hud.hide()