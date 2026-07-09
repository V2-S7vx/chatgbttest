from OpenGL.GL import *





class Renderer:


    def __init__(self):


        self.clear_color = (

            0.0,

            0.0,

            0.0,

            1.0

        )





    # ==========================================
    # OPENGL SETUP
    # ==========================================

    def setup(self):


        glEnable(

            GL_DEPTH_TEST

        )


        glEnable(

            GL_BLEND

        )


        glBlendFunc(

            GL_SRC_ALPHA,

            GL_ONE_MINUS_SRC_ALPHA

        )


        # smoother star particles

        glEnable(

            GL_POINT_SMOOTH

        )


        glHint(

            GL_POINT_SMOOTH_HINT,

            GL_NICEST

        )


        # smoother blending

        glEnable(

            GL_LINE_SMOOTH

        )


        glHint(

            GL_LINE_SMOOTH_HINT,

            GL_NICEST

        )





    # ==========================================
    # CLEAR
    # ==========================================

    def clear(self):


        glClearColor(

            *self.clear_color

        )


        glClear(

            GL_COLOR_BUFFER_BIT |

            GL_DEPTH_BUFFER_BIT

        )





    # ==========================================
    # CINEMATIC WHITE TRANSITION
    # ==========================================

    def draw_flash(
            self,
            alpha
    ):


        if alpha <= 0:

            return



        glDisable(

            GL_DEPTH_TEST

        )


        glDisable(

            GL_TEXTURE_2D

        )



        glMatrixMode(

            GL_PROJECTION

        )


        glPushMatrix()


        glLoadIdentity()



        glMatrixMode(

            GL_MODELVIEW

        )


        glPushMatrix()


        glLoadIdentity()





        # ======================================
        # MAIN SOFT WHITE LAYER
        # ======================================


        strength = alpha ** 2



        glColor4f(

            0.92,

            0.95,

            1.0,

            strength * 0.75

        )



        glBegin(

            GL_QUADS

        )


        glVertex2f(

            -1,

            -1

        )


        glVertex2f(

            1,

            -1

        )


        glVertex2f(

            1,

            1

        )


        glVertex2f(

            -1,

            1

        )


        glEnd()





        # ======================================
        # EXTRA LIGHT BLOOM
        # ======================================


        if alpha > 0.5:


            glow = (

                alpha - 0.5

            ) * 0.2



            glColor4f(

                1.0,

                1.0,

                1.0,

                glow

            )



            glBegin(

                GL_QUADS

            )


            glVertex2f(

                -1,

                -1

            )


            glVertex2f(

                1,

                -1

            )


            glVertex2f(

                1,

                1

            )


            glVertex2f(

                -1,

                1

            )


            glEnd()





        glMatrixMode(

            GL_MODELVIEW

        )


        glPopMatrix()



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