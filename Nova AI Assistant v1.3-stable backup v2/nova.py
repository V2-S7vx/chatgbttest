class Nova:


    def __init__(self):

        self.name = "Nova"

        self.version = "V2"

        self.status = "OFFLINE"



    def start(self):

        self.status = "ONLINE"


        print(
            f"{self.name} {self.version} ONLINE"
        )



    def shutdown(self):

        self.status = "OFFLINE"


        print(
            f"{self.name} OFFLINE"
        )



    def get_status(self):

        return {

            "name": self.name,

            "version": self.version,

            "status": self.status

        }