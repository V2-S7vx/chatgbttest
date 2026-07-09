class TextPoints:


    FONT = {


        "V":[
            "10001",
            "10001",
            "10001",
            "10001",
            "10001",
            "01010",
            "00100"
        ],



        "2":[
            "11111",
            "00001",
            "00001",
            "11111",
            "10000",
            "10000",
            "11111"
        ],



        "D":[
            "11110",
            "10001",
            "10001",
            "10001",
            "10001",
            "10001",
            "11110"
        ],



        "E":[
            "11111",
            "10000",
            "10000",
            "11110",
            "10000",
            "10000",
            "11111"
        ],



        "L":[
            "10000",
            "10000",
            "10000",
            "10000",
            "10000",
            "10000",
            "11111"
        ],



        "O":[
            "01110",
            "10001",
            "10001",
            "10001",
            "10001",
            "10001",
            "01110"
        ],



        "P":[
            "11110",
            "10001",
            "10001",
            "11110",
            "10000",
            "10000",
            "10000"
        ],



        "M":[
            "10001",
            "11011",
            "10101",
            "10101",
            "10001",
            "10001",
            "10001"
        ],



        "N":[
            "10001",
            "11001",
            "11101",
            "10101",
            "10111",
            "10011",
            "10001"
        ],



        "T":[
            "11111",
            "00100",
            "00100",
            "00100",
            "00100",
            "00100",
            "00100"
        ]

    }





    @staticmethod
    def generate(
            text,
            spacing=3
    ):


        points = []


        offset_x = 0



        for char in text:


            if char == " ":


                offset_x += 8

                continue



            pattern = TextPoints.FONT.get(

                char

            )



            if not pattern:

                continue



            for y,row in enumerate(pattern):


                for x,value in enumerate(row):


                    if value == "1":


                        points.append(

                            (

                                offset_x + x,

                                -y

                            )

                        )



            offset_x += len(pattern[0]) + spacing





        if points:


            min_x = min(

                p[0]

                for p in points

            )


            max_x = max(

                p[0]

                for p in points

            )


            min_y = min(

                p[1]

                for p in points

            )


            max_y = max(

                p[1]

                for p in points

            )



            center_x = (

                min_x + max_x

            ) / 2



            center_y = (

                min_y + max_y

            ) / 2





            centered = []



            for x,y in points:


                centered.append(

                    (

                        x - center_x,

                        y - center_y

                    )

                )



            return centered





        return points
