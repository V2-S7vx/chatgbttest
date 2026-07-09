import random

from OpenGL.GL import *





class Starfield:


    def __init__(
            self,
            amount=2000
    ):


        self.amount = amount

        self.stars = []

        self.featured_stars = []


        self.create_stars()

        self.create_featured_stars()





    # ==========================================
    # CREATE NORMAL STARS
    # ==========================================

    def create_stars(self):


        for i in range(self.amount):


            self.stars.append(

                {


                    "x":
                        random.uniform(
                            -120,
                            120
                        ),


                    "y":
                        random.uniform(
                            -120,
                            120
                        ),


                    "z":
                        random.uniform(
                            -400,
                            40
                        ),


                    "size":
                        random.choice(

                            [
                                1,
                                1,
                                2,
                                3
                            ]

                        ),


                    "brightness":
                        random.uniform(
                            0.3,
                            1.0
                        ),


                    "speed":
                        random.uniform(
                            5,
                            40
                        ),


                    "color":
                        random.choice(

                            [

                                (
                                    1.0,
                                    1.0,
                                    1.0
                                ),

                                (
                                    0.7,
                                    0.9,
                                    1.0
                                ),

                                (
                                    0.85,
                                    0.95,
                                    1.0
                                )

                            ]

                        )

                }

            )





    # ==========================================
    # CREATE FEATURED STARS
    # ==========================================

    def create_featured_stars(self):


        self.featured_stars = [


            # original star 1

            {
                "x": -70,
                "y": 45,
                "z": -80
            },


            # original star 2

            {
                "x": 65,
                "y": 20,
                "z": -120
            },


            # original star 3

            {
                "x": 10,
                "y": -55,
                "z": -60
            },


            # new star 4 - far top center

            {
                "x": 0,
                "y": 100,
                "z": -200
            },


            # new star 5 - far bottom left

            {
                "x": -110,
                "y": -90,
                "z": -170
            }


        ]





    # ==========================================
    # UPDATE
    # ==========================================

    def update(
            self,
            delta
    ):


        for star in self.stars:


            star["z"] += (

                star["speed"]

                *

                delta

            )



            if star["z"] > 50:


                star["z"] = -400



                star["x"] = random.uniform(
                    -120,
                    120
                )


                star["y"] = random.uniform(
                    -120,
                    120
                )





    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):


        # ======================================
        # NORMAL STARS
        # ======================================


        for size in [1, 2, 3]:


            glPointSize(size)


            glBegin(

                GL_POINTS

            )


            for star in self.stars:


                if star["size"] != size:

                    continue



                r, g, b = star["color"]


                glow = star["brightness"]



                glColor4f(

                    r * glow,

                    g * glow,

                    b * glow,

                    glow

                )



                glVertex3f(

                    star["x"],

                    star["y"],

                    star["z"]

                )


            glEnd()





        # ======================================
        # FEATURED STAR GLOW
        # ======================================


        glBlendFunc(

            GL_SRC_ALPHA,

            GL_ONE

        )





        # --------------------------------------
        # OUTER GLOW
        # --------------------------------------


        glPointSize(45)


        glBegin(

            GL_POINTS

        )


        for star in self.featured_stars:


            glColor4f(

                0.65,

                0.85,

                1.0,

                0.08

            )


            glVertex3f(

                star["x"],

                star["y"],

                star["z"]

            )


        glEnd()





        # --------------------------------------
        # MIDDLE GLOW
        # --------------------------------------


        glPointSize(25)


        glBegin(

            GL_POINTS

        )


        for star in self.featured_stars:


            glColor4f(

                0.85,

                0.95,

                1.0,

                0.18

            )


            glVertex3f(

                star["x"],

                star["y"],

                star["z"]

            )


        glEnd()





        # --------------------------------------
        # BRIGHT CORE
        # --------------------------------------


        glPointSize(8)


        glBegin(

            GL_POINTS

        )


        for star in self.featured_stars:


            glColor4f(

                1.0,

                1.0,

                1.0,

                1.0

            )


            glVertex3f(

                star["x"],

                star["y"],

                star["z"]

            )


        glEnd()



        # restore normal blending


        glBlendFunc(

            GL_SRC_ALPHA,

            GL_ONE_MINUS_SRC_ALPHA

        )