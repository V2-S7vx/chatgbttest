import math

from OpenGL.GL import *



class NovaHub:


    def __init__(self):

        self.time = 0
        self.pulse = 0



    def update(self, delta):

        self.time += delta

        self.pulse = (
            math.sin(self.time * 2.5) + 1
        ) / 2



    def circle(self, radius, color, width=2, alpha=1):

        glLineWidth(width)

        glColor4f(
            color[0],
            color[1],
            color[2],
            alpha
        )

        glBegin(GL_LINE_LOOP)

        for i in range(240):

            a = math.pi * 2 * i / 240

            glVertex2f(
                math.cos(a) * radius,
                math.sin(a) * radius
            )

        glEnd()



    def fill_circle(self, radius, color, alpha=1):

        glColor4f(
            color[0],
            color[1],
            color[2],
            alpha
        )

        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(0,0)

        for i in range(241):

            a = math.pi * 2 * i / 240

            glVertex2f(
                math.cos(a) * radius,
                math.sin(a) * radius
            )

        glEnd()



    def arc(self, radius, start, end, color, width=3, alpha=1):

        glLineWidth(width)

        glColor4f(
            color[0],
            color[1],
            color[2],
            alpha
        )

        glBegin(GL_LINE_STRIP)

        for i in range(120):

            a = start + (end-start) * i / 120

            glVertex2f(
                math.cos(a)*radius,
                math.sin(a)*radius
            )

        glEnd()



    def line_detail(self, r1, r2, amount, rotation):

        glColor4f(
            0.025,
            0.035,
            0.055,
            1
        )

        glLineWidth(2)

        glBegin(GL_LINES)

        for i in range(amount):

            a = rotation + (
                i * math.pi * 2 / amount
            )

            glVertex2f(
                math.cos(a)*r1,
                math.sin(a)*r1
            )

            glVertex2f(
                math.cos(a)*r2,
                math.sin(a)*r2
            )

        glEnd()



    def reactor_segments(self, radius, amount, rotation):

        for i in range(amount):

            a = rotation + (
                i * math.pi * 2 / amount
            )

            self.arc(
                radius,
                a,
                a+0.12,
                (
                    0.008,
                    0.035,
                    0.10
                ),
                5
            )



    def draw_core(self):


        # almost invisible dark blue atmosphere

        self.fill_circle(
            0.62,
            (
                0.0,
                0.001,
                0.008
            ),
            0.35
        )


        # near black reactor shell

        self.fill_circle(
            0.55,
            (
                0.001,
                0.002,
                0.005
            )
        )


        # outer armour rings

        self.circle(
            0.55,
            (
                0.015,
                0.02,
                0.035
            ),
            8
        )


        self.circle(
            0.50,
            (
                0.02,
                0.03,
                0.055
            ),
            3
        )


        self.circle(
            0.46,
            (
                0.008,
                0.025,
                0.08
            ),
            2
        )


        # dim reactor segments

        self.reactor_segments(
            0.48,
            32,
            self.time * 0.5
        )


        # internal engineering marks

        self.line_detail(
            0.40,
            0.44,
            48,
            -self.time
        )


        # middle shell

        self.circle(
            0.38,
            (
                0.035,
                0.045,
                0.065
            ),
            4
        )


        self.fill_circle(
            0.35,
            (
                0.001,
                0.003,
                0.008
            )
        )


        # slow moving inner energy

        self.arc(
            0.32,
            self.time,
            self.time+2.5,
            (
                0.005,
                0.045,
                0.14
            ),
            6
        )


        self.arc(
            0.28,
            -self.time*1.3,
            -self.time*1.3+2,
            (
                0.008,
                0.03,
                0.10
            ),
            4
        )


        # centre chamber

        self.circle(
            0.23,
            (
                0.035,
                0.045,
                0.07
            ),
            3
        )


        self.fill_circle(
            0.20,
            (
                0.002,
                0.003,
                0.008
            )
        )


        # extremely faint core pulse

        glow = (
            0.025 +
            self.pulse * 0.012
        )


        self.fill_circle(
            glow,
            (
                0.008,
                0.06,
                0.18
            )
        )


        self.circle(
            0.12,
            (
                0.02,
                0.09,
                0.22
            ),
            2
        )


        # dark metallic bolts

        glPointSize(5)

        glColor4f(
            0.04,
            0.055,
            0.08,
            1
        )


        glBegin(GL_POINTS)


        for i in range(24):

            a = (
                self.time*0.2 +
                i*math.pi*2/24
            )

            glVertex2f(
                math.cos(a)*0.52,
                math.sin(a)*0.52
            )


        glEnd()



    def draw(self):

        glDisable(GL_DEPTH_TEST)

        glEnable(GL_BLEND)

        glBlendFunc(
            GL_SRC_ALPHA,
            GL_ONE_MINUS_SRC_ALPHA
        )


        self.draw_core()


        glDisable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)