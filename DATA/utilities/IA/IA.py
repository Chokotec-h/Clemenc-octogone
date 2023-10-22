class IA():
    def __init__(self, char) -> None:
        self.char = char

    def inputs(self,game):
        """ inputs :
            0 : left
            1 : right
            2 : up
            3 : down
            4 : fullhop
            5 : shorthop
            6 : attack
            7 : special
            8 : shield (hold to run)
            9 : C_Left
            10 : C_Right
            11 : C_Up
            12 : C_Down
            13 : D_Left
            14 : D_Right
            15 : D_Up
            16 : D_Down
            17 : 2e shorthop
            18 : L_Tilt
            19 : R_Tilt
            20 : U_Tilt
            21 : D_Tilt
        """
        inputs = [False for _ in range(23)]
        return inputs
