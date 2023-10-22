class IAtest():
    def __init__(self, char) -> None:
        self.char = char

    def inputs(self,game):
        # inputs : left, right, up, down, fullhop, shorthop, attack, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down, ? , L_Tilt, R_Tilt, U_Tilt, D_Tilt, 
        inputs = [False for _ in range(23)]
        return inputs
