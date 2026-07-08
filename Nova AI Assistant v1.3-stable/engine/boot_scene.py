from .scene import Scene

from effects import StarBoot

from .nova_scene import NovaScene


class BootScene(Scene):


    def __init__(
            self,
            engine
    ):


        self.engine = engine


        self.boot = StarBoot()



    # ==========================================
    # ENTER
    # ==========================================

    def enter(self):


        self.boot.start()



    # ==========================================
    # UPDATE
    # ==========================================

    def update(
            self,
            delta
    ):


        self.boot.update(

            delta

        )


        if self.boot.is_finished():


            self.engine.set_scene(

                NovaScene(

                    self.engine.window

                )

            )



    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):


        self.boot.draw()



    # ==========================================
    # EXIT
    # ==========================================

    def exit(self):


        pass