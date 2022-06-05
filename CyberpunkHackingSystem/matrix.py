from random import randrange

class CodeMatrix:
    def __init__(self, matrix_len=5, seq_len=4):
        self.matrix_len = matrix_len
        self.seq_len = seq_len

        self.code_matrix = [["0" for _ in range(matrix_len)] for _ in range(matrix_len)]
        self.sequence = ["0" for _ in range (seq_len)]

    def create_code_matrix(self):  # sourcery skip: use-itertools-product
        idList = ["1C", "E9", "55", "BD", "7A"]

        for l in range(self.matrix_len):
            for c in range(self.matrix_len):
                self.code_matrix[l][c] = idList[randrange(0, len(idList))] 

    def generate_sequence(self):
        startL = 0
        startC = randrange(0, self.matrix_len)
        turn = False
        self.sequence[0] = self.code_matrix[startL][startC]
        for i in range(self.seq_len-1):
            if turn:
                l = startL
                c = randrange(0, self.matrix_len)
                while (c == startC):
                    c = randrange(0, self.matrix_len)
                turn = False
            else:
                l = randrange(0, self.matrix_len)
                while (l == startL):
                    l = randrange(0, self.matrix_len)
                c = startC
                turn = True
            self.sequence[i+1] = self.code_matrix[l][c]
            startL = l
            startC = c

    def show_code_matrix(self):
        print("CODE MATRIX")
        for l in range(self.matrix_len):
            print("|", end=" ")
            for c in range(self.matrix_len):
                print(f"{self.code_matrix[l][c]} |", end=" ")
            print("\n")

    def show_sequence(self):
        print("SEQUENCE REQUIRED TO UPLOAD")
        for i in range(self.seq_len):
            print(self.sequence[i], end=" ")
        print("")

    def get_code(self, l, c): return self.code_matrix[l][c]

    def get_sequence(self, i): return self.sequence[i]

    def get_matrix_len(self): return self.matrix_len

    def get_seq_len(self): return self.seq_len