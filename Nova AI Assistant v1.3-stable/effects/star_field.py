import random

from OpenGL.GL import *





class Starfield:


    def __init__(
            self,
            amount=8000
    ):


        self.amount = amount

        self.stars = []


        self.create_stars()





    # ==========================================
    # CREATE STARS
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


        # draw by size without rebuilding lists


        for size in [1,2,3]:


            glPointSize(size)



            glBegin(

                GL_POINTS

            )



            for star in self.stars:


                if star["size"] != size:

                    continue



                r,g,b = star["color"]



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