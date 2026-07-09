from engine import NovaEngine

from engine.boot_scene import BootScene





def main():


    print(

        """

================================

        NOVA V1.3 STARTING

================================

        """

    )



    engine = NovaEngine()



    boot_scene = BootScene(

        engine

    )



    engine.set_scene(

        boot_scene

    )



    engine.start()





if __name__ == "__main__":

    main()