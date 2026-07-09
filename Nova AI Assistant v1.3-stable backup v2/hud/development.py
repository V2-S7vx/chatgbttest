# ==========================================================
# NOVA DEVELOPMENT HUD
# TOP CINEMATIC VERSION DISPLAY
# ==========================================================


import math



class DevelopmentHUD:


    def __init__(self):


        self.time = 0


        self.alpha = 0



    # ==================================================
    # UPDATE
    # ==================================================

    def update(
            self,
            delta
    ):


        self.time += delta



        # smooth fade cycle

        self.alpha = (

            math.sin(
                self.time * 1.2
            )

            +

            1

        ) / 2



    # ==================================================
    # DRAW
    # ==================================================

    def draw(
            self,
            width,
            height
    ):


        from OpenGL.GL import *



        # This will later be replaced
        # with the proper text renderer.


        return