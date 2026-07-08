import sys
import subprocess
import os





# ==========================================
# NOVA DEPENDENCIES
# ==========================================

DEPENDENCIES = [

    (
        "PySide6",
        "PySide6"
    ),

    (
        "PyOpenGL",
        "OpenGL"
    ),

    (
        "PyOpenGL_accelerate",
        "OpenGL_accelerate"
    ),

    (
        "psutil",
        "psutil"
    )

]





# ==========================================
# INSTALL PACKAGES
# ==========================================

def install_packages():


    print(
        "\n[NOVA] Checking dependencies...\n"
    )



    for package, module in DEPENDENCIES:


        try:


            __import__(
                module
            )


            print(
                f"[OK] {package}"
            )


        except ImportError:


            print(
                f"[INSTALLING] {package}"
            )



            subprocess.check_call(

                [

                    sys.executable,

                    "-m",

                    "pip",

                    "install",

                    package

                ]

            )





# ==========================================
# CREATE PROJECT STRUCTURE
# ==========================================

def create_structure():


    folders = [

        "assets",

        "assets/models",

        "assets/sounds",

        "assets/textures",

        "effects",

        "engine",

        "hud"

    ]



    print(

        "\n[NOVA] Checking folders...\n"

    )



    for folder in folders:


        if not os.path.exists(folder):


            os.makedirs(folder)


            print(

                f"[CREATED] {folder}"

            )


        else:


            print(

                f"[OK] {folder}"

            )





# ==========================================
# CREATE INIT FILES
# ==========================================

def create_init_files():


    packages = [

        "effects",

        "engine",

        "hud"

    ]



    print(

        "\n[NOVA] Checking Python packages...\n"

    )



    for package in packages:


        init = os.path.join(

            package,

            "__init__.py"

        )



        if not os.path.exists(init):


            open(

                init,

                "w"

            ).close()



            print(

                f"[CREATED] {init}"

            )


        else:


            print(

                f"[OK] {init}"

            )





# ==========================================
# PYTHON CHECK
# ==========================================

def python_check():


    version = sys.version_info



    print(

        "\n[NOVA] Python version:"

    )


    print(

        f"{version.major}.{version.minor}.{version.micro}"

    )



    if version.major < 3:


        print(

            "[ERROR] Python 3 required"

        )


        sys.exit(1)





# ==========================================
# SETUP
# ==========================================

def setup():


    print(

        """

================================

        NOVA V2 SETUP

================================

        """

    )



    python_check()


    install_packages()


    create_structure()


    create_init_files()



    print(

        """

================================

      NOVA SETUP COMPLETE


 Run:


      python main.py


================================

        """

    )







if __name__ == "__main__":

    setup()