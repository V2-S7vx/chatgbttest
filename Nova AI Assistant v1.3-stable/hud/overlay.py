# ==========================================================
# NOVA CINEMATIC HUD OVERLAY
# JARVIS STYLE INTERFACE LAYER
# ==========================================================


from PySide6.QtWidgets import QWidget

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QFont
)


import psutil
import math


from engine import config

from hud import config as hud_config





class NovaHUD(QWidget):


    def __init__(
            self,
            parent=None
    ):

        super().__init__(
            parent
        )


        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )


        self.setAttribute(
            Qt.WA_TranslucentBackground
        )



        # ==========================================
        # TITLE ANIMATION
        # ==========================================

        self.title_time = 0



        # ==========================================
        # TELEMETRY
        # ==========================================

        self.cpu = 0

        self.memory = 0

        self.gpu = 0



        self.time = 0



        self.timer = QTimer(
            self
        )


        self.timer.timeout.connect(
            self.animate
        )


        self.timer.start(
            16
        )




    # ==========================================
    # UPDATE
    # ==========================================

    def animate(
            self
    ):


        self.title_time += 1

        self.time += 1



        self.cpu = psutil.cpu_percent()



        self.memory = (

            psutil.virtual_memory()

            .percent

        )



        self.update()




    # ==========================================
    # TITLE BRIGHTNESS
    # ==========================================

    def get_title_brightness(
            self
    ):


        t = self.title_time



        fade_in = hud_config.TITLE_FADE_IN_FRAMES


        hold = hud_config.TITLE_WHITE_HOLD_FRAMES


        fade_out = hud_config.TITLE_FADE_OUT_FRAMES



        # Fade from black to white

        if t < fade_in:


            return int(

                255 *

                (

                    t /

                    fade_in

                )

            )



        # Stay white

        elif t < (

            fade_in +

            hold

        ):


            return 255




        # Fade white back to black

        elif t < (

            fade_in +

            hold +

            fade_out

        ):


            progress = (

                t -

                fade_in -

                hold

            ) / fade_out



            return int(

                255 *

                (

                    1 -

                    progress

                )

            )



        else:


            self.title_time = 0


            return 0





    # ==========================================
    # DRAW
    # ==========================================

    def paintEvent(
            self,
            event
    ):


        painter = QPainter(
            self
        )


        painter.setRenderHint(
            QPainter.Antialiasing
        )


        width = self.width()

        height = self.height()



        # ==========================================
        # V2 DEVELOPMENT
        # ==========================================


        brightness = self.get_title_brightness()



        painter.setFont(

            QFont(

                hud_config.TITLE_FONT,

                hud_config.TITLE_FONT_SIZE

            )

        )


        painter.setPen(

            QColor(

                brightness,

                brightness,

                brightness

            )

        )



        title = "V2 DEVELOPMENT"



        text_width = (

            painter.fontMetrics()

            .horizontalAdvance(
                title
            )

        )


        painter.drawText(

            (

                width -

                text_width

            )

            //

            2,

            hud_config.TITLE_Y,

            title

        )



        # ==========================================
        # LEFT STATUS
        # ==========================================


        painter.setFont(

            QFont(

                hud_config.HUD_FONT,

                hud_config.HUD_FONT_SIZE

            )

        )



        systems = [

            "NOVA GPU PIPELINE // ONLINE",

            "GPU RENDERER // ONLINE",

            "HOLOGRAM HUD // ONLINE",

            "NOVA AI SYSTEM // ONLINE"

        ]



        for i,text in enumerate(
            systems
        ):


            painter.setPen(

                QColor(

                    hud_config.HUD_RED,

                    hud_config.HUD_GREEN,

                    hud_config.HUD_BLUE

                )

            )


            painter.drawText(

                hud_config.LEFT_HUD_X,

                (

                    height //

                    2

                    +

                    hud_config.LEFT_HUD_Y_OFFSET

                    +

                    i *

                    hud_config.LEFT_HUD_SPACING

                ),

                text

            )




        # ==========================================
        # TELEMETRY
        # ==========================================


        telemetry = [

            f"MEMORY USAGE // {self.memory:.1f}%",

            f"CPU LOAD // {self.cpu:.1f}%",

            f"GPU POWER // {self.gpu:.1f}%"

        ]



        for i,text in enumerate(
            telemetry
        ):


            painter.drawText(

                width -

                hud_config.RIGHT_HUD_OFFSET_X,

                height -

                hud_config.RIGHT_HUD_OFFSET_Y

                +

                (

                    i *

                    hud_config.RIGHT_HUD_SPACING

                ),

                text

            )



        painter.end()
