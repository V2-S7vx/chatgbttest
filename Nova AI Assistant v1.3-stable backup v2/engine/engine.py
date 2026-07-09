import sys

from PySide6.QtWidgets import QApplication

from PySide6.QtOpenGLWidgets import QOpenGLWidget

from PySide6.QtCore import Qt

from OpenGL.GL import *


from .clock import Clock
from .renderer import Renderer
from .events import EventManager
from .camera import Camera
from .config import *

from nova import Nova





class NovaWindow(QOpenGLWidget):


    def __init__(
            self,
            engine
    ):


        super().__init__()


        self.engine = engine


        self.fullscreen = False



        self.setWindowTitle(

            WINDOW_TITLE

        )



        # windowed fullscreen

        self.showMaximized()



        self.setFocusPolicy(

            Qt.StrongFocus

        )





    # ==========================================
    # KEYBOARD
    # ==========================================

    def keyPressEvent(
            self,
            event
    ):


        # F11 fullscreen toggle

        if event.key() == Qt.Key_F11:


            self.toggle_fullscreen()



        # ESC return to window

        elif event.key() == Qt.Key_Escape:


            if self.fullscreen:


                self.toggle_fullscreen()



        else:


            super().keyPressEvent(

                event

            )





    # ==========================================
    # FULLSCREEN TOGGLE
    # ==========================================

    def toggle_fullscreen(self):


        if self.fullscreen:


            self.showMaximized()


            self.fullscreen = False



        else:


            self.showFullScreen()


            self.fullscreen = True





    # ==========================================
    # OPENGL INIT
    # ==========================================

    def initializeGL(self):


        self.engine.renderer.setup()





    # ==========================================
    # RESIZE
    # ==========================================

    def resizeGL(
            self,
            width,
            height
    ):


        glViewport(

            0,

            0,

            width,

            height

        )


        self.engine.camera.setup_projection(

            width,

            height

        )





    # ==========================================
    # DRAW
    # ==========================================

    def paintGL(self):


        self.engine.renderer.clear()



        # protect camera matrix

        glMatrixMode(

            GL_MODELVIEW

        )


        glPushMatrix()



        self.engine.camera.apply()



        if self.engine.scene:


            self.engine.scene.draw()



        # restore clean state

        glPopMatrix()





    # ==========================================
    # LOOP
    # ==========================================

    def timerEvent(
            self,
            event
    ):


        self.engine.update()


        self.update()







class NovaEngine:



    def __init__(self):


        self.app = QApplication(

            sys.argv

        )



        # CORE SYSTEMS


        self.clock = Clock(

            TARGET_FPS

        )


        self.renderer = Renderer()



        self.events = EventManager()



        self.camera = Camera()





        # NOVA


        self.nova = Nova()


        self.nova.start()





        # CURRENT SCENE


        self.scene = None





        # WINDOW


        self.window = NovaWindow(

            self

        )








    # ==========================================
    # SCENE CONTROL
    # ==========================================

    def set_scene(
            self,
            scene
    ):


        if self.scene:


            self.scene.exit()



        self.scene = scene



        if self.scene:


            self.scene.enter()





    # ==========================================
    # UPDATE
    # ==========================================

    def update(self):


        self.clock.update()



        delta = self.clock.get_delta()



        if self.scene:


            self.scene.update(

                delta

            )








    # ==========================================
    # START
    # ==========================================

    def start(self):


        self.window.show()



        self.window.startTimer(

            int(

                1000 /

                TARGET_FPS

            )

        )



        sys.exit(

            self.app.exec()

        )