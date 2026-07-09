from .scene import Scene

from effects import Starfield

from hud.overlay import NovaHUD
from hud.nova_hud import NovaHub


from OpenGL.GL import *
from OpenGL.GLU import *





class NovaScene(Scene):


    def __init__(
            self,
            parent=None
    ):


        self.parent = parent



        # ==========================================
        # WORLD
        # ==========================================

        self.starfield = Starfield()



        # ==========================================
        # NOVA CORE HUD
        # ==========================================

        self.nova_hub = NovaHub()



        # ==========================================
        # PYQT OVERLAY
        # ==========================================

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


        self.nova_hub.update(

            delta

        )





    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):


        # ======================================
        # DRAW STARFIELD
        # ======================================

        self.starfield.draw()



        # ======================================
        # DRAW NOVA CORE HUD
        # ======================================


        glDisable(

            GL_DEPTH_TEST

        )


        glDisable(

            GL_LIGHTING

        )



        # get screen size

        viewport = glGetIntegerv(

            GL_VIEWPORT

        )


        width = viewport[2]

        height = viewport[3]



        if height == 0:

            height = 1



        aspect = width / height





        # save projection

        glMatrixMode(

            GL_PROJECTION

        )


        glPushMatrix()



        glLoadIdentity()



        # ======================================
        # ASPECT CORRECTED HUD SPACE
        # ======================================

        if aspect >= 1:


            glOrtho(

                -aspect,

                aspect,

                -1,

                1,

                -10,

                10

            )


        else:


            glOrtho(

                -1,

                1,

                -1 / aspect,

                1 / aspect,

                -10,

                10

            )





        # save model

        glMatrixMode(

            GL_MODELVIEW

        )


        glPushMatrix()



        glLoadIdentity()



        # ======================================
        # NOVA CORE SIZE
        # ======================================

        glScalef(

            0.42,

            0.42,

            1

        )



        self.nova_hub.draw()



        glPopMatrix()



        # restore projection

        glMatrixMode(

            GL_PROJECTION

        )


        glPopMatrix()



        glMatrixMode(

            GL_MODELVIEW

        )


        glEnable(

            GL_DEPTH_TEST

        )





    # ==========================================
    # EXIT
    # ==========================================

    def exit(self):


        self.hud.hide()