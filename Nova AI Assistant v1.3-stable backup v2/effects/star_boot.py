import random
import math

from OpenGL.GL import *

from .text_points import TextPoints





class StarBoot:


    WAITING = "WAITING"
    RUSH_IN = "RUSH_IN"
    FORMING = "FORMING"
    HOLD = "HOLD"
    RUSH_OUT = "RUSH_OUT"
    COMPLETE = "COMPLETE"





    def __init__(
            self,
            amount=6000
    ):


        self.amount = amount

        self.state = self.WAITING

        self.time = 0

        self.finished = False

        self.stars = []

        self.create_stars()





    # ==========================================
    # CREATE STARS
    # ==========================================

    def create_stars(self):


        for i in range(self.amount):


            angle = random.uniform(
                0,
                math.pi * 2
            )


            distance = random.uniform(
                120,
                400
            )


            self.stars.append({


                "x":
                    math.cos(angle) * distance,


                "y":
                    math.sin(angle) * distance,


                "z":
                    random.uniform(
                        -900,
                        -100
                    ),


                "speed":
                    random.uniform(
                        90,
                        190
                    ),


                "brightness":
                    random.uniform(
                        0.5,
                        1.0
                    ),


                "target_x": 0,

                "target_y": 0,

                "target_z": 0

            })





    # ==========================================
    # START
    # ==========================================

    def start(self):


        self.state = self.RUSH_IN

        self.time = 0

        self.finished = False





    # ==========================================
    # UPDATE
    # ==========================================

    def update(
            self,
            delta
    ):


        self.time += delta


        if self.state == self.RUSH_IN:


            self.rush_in(delta)



        elif self.state == self.FORMING:


            self.form_text(delta)



        elif self.state == self.HOLD:


            self.hold()



        elif self.state == self.RUSH_OUT:


            self.rush_out(delta)





    # ==========================================
    # STAR RUSH IN
    # ==========================================

    def rush_in(
            self,
            delta
    ):


        finished = True


        for star in self.stars:


            star["z"] += (

                star["speed"]

                *

                2.2

                *

                delta

            )


            if star["z"] < 0:

                finished = False





        if finished:


            self.generate_text_targets()

            self.state = self.FORMING





    # ==========================================
    # TEXT TARGETS
    # ==========================================

    def generate_text_targets(self):


        points = TextPoints.generate(

            "V2 DEVELOPMENT"

        )


        scale = 1.5



        for i, star in enumerate(self.stars):


            point = points[i % len(points)]



            star["target_x"] = point[0] * scale

            star["target_y"] = point[1] * scale

            star["target_z"] = 0





    # ==========================================
    # FORM TEXT
    # ==========================================

    def form_text(
            self,
            delta
    ):


        finished = True



        for star in self.stars:


            star["x"] += (

                star["target_x"]

                -

                star["x"]

            ) * 0.09



            star["y"] += (

                star["target_y"]

                -

                star["y"]

            ) * 0.09



            star["z"] += (

                star["target_z"]

                -

                star["z"]

            ) * 0.09



            if abs(

                star["target_x"]

                -

                star["x"]

            ) > 0.2:


                finished = False





        if finished:


            self.state = self.HOLD

            self.time = 0





    # ==========================================
    # HOLD TITLE
    # ==========================================

    def hold(self):


        if self.time >= 1.6:


            self.state = self.RUSH_OUT

            self.time = 0





    # ==========================================
    # LETTER DISSOLVE
    # ==========================================

    def rush_out(
            self,
            delta
    ):


        progress = min(

            self.time / 4,

            1

        )


        speed = (

            10

            +

            (

                progress ** 2

                *

                450

            )

        )





        for star in self.stars:


            star["x"] += random.uniform(

                -1,

                1

            ) * delta * 20



            star["y"] += random.uniform(

                -1,

                1

            ) * delta * 20



            star["z"] += (

                speed

                *

                delta

            )





        if self.time >= 4:


            self.finished = True

            self.state = self.COMPLETE





    # ==========================================
    # STATUS
    # ==========================================

    def is_finished(self):


        return self.finished





    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):


        glPointSize(3)



        glBegin(

            GL_POINTS

        )



        for star in self.stars:


            glColor4f(

                star["brightness"],

                star["brightness"],

                1,

                1

            )


            glVertex3f(

                star["x"],

                star["y"],

                star["z"]

            )



        glEnd()