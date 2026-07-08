from OpenGL.GL import *
from OpenGL.GLU import *





class Camera:


    def __init__(self):


        self.x = 0


        self.y = 0


        self.z = 100



        self.fov = 60


        self.near = 0.1


        self.far = 2000





    # ==========================================
    # SET PROJECTION
    # ==========================================

    def setup_projection(
            self,
            width,
            height
    ):


        if height == 0:

            height = 1



        aspect = width / height



        glMatrixMode(

            GL_PROJECTION

        )


        glLoadIdentity()



        gluPerspective(

            self.fov,

            aspect,

            self.near,

            self.far

        )



        glMatrixMode(

            GL_MODELVIEW

        )





    # ==========================================
    # APPLY CAMERA
    # ==========================================

    def apply(self):


        glLoadIdentity()



        gluLookAt(

            self.x,

            self.y,

            self.z,


            0,

            0,

            0,


            0,

            1,

            0

        )