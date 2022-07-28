from random import randrange

class CodeMatrix:
    def __init__(self, matrix_len=5, seq_len=4):
        self.matrix_len = matrix_len
        self.seq_len = seq_len

        self.code_matrix = [["0" for _ in range(matrix_len)] for _ in range(matrix_len)] # create a string matrix square of 0
        self.sequence = ["0" for _ in range (seq_len)] # create a string table of one line (= the sequence)

    def create_code_matrix(self):  # sourcery skip: use-itertools-product
        idList = ["1C", "E9", "55", "BD", "7A", "FF"]

        for l in range(self.matrix_len):
            for c in range(self.matrix_len):
                self.code_matrix[l][c] = idList[randrange(0, len(idList))]  # complete randomly each position in the matrix

    def generate_sequence(self):
        startL = 0
        startC = randrange(0, self.matrix_len)
        turn = False
        self.sequence[0] = self.code_matrix[startL][startC] # defined the starting point of the sequence (always on the first line)
        for i in range(self.seq_len-1):
            if turn: # the condition allows to alternate line and column when find a new value to complete the sequence
                l = startL # the line doesn't change
                c = randrange(0, self.matrix_len) # choose a new value on the same line but an other column
                while (c == startC):
                    c = randrange(0, self.matrix_len) # verify the new value is different of the turning point
                turn = False
            else:
                c = startC # the column doesn't change
                l = randrange(0, self.matrix_len) # choose a new value on the same column but an other line
                while (l == startL):
                    l = randrange(0, self.matrix_len) # verify the new value is different of the turning point
                turn = True
            self.sequence[i+1] = self.code_matrix[l][c] # complete the sequence
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