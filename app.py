import pygame
import pygame.draw as draw
import time
import numpy as np

pygame.init()

width = 480
height = 480

icon = pygame.image.load('assets/Chess_klt60.png')
pygame.display.set_icon(icon)
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess')

dark = (34, 143, 58)
light = (232, 237, 197)
dark_selected = (34, 110, 58)
light_selected = (202, 207, 177)

clock = pygame.time.Clock()
crashed = False


class GameBoard():
    def __init__(self):
        self.gameBoard = np.zeros((8, 8), dtype=object)
        self.pieces = set([])
        self.kings = {'white': None, 'black': None}
        self.check = False

    def show(self):
        gameDisplay.fill(light)
        for i in range(4):
            for j in range(8):
                x = 120*i + 60*(j % 2)
                y = j*60
                draw.rect(gameDisplay, dark, (x, y, 60, 60))

        for piece in self.pieces:
            piece.show()

    def move(self, piece, dest):
        assert piece != 0
        target = piece.square
        if target == dest:
            return False

        dest_piece = self.gameBoard[dest]

        allowed = piece.check_legal(dest, self.gameBoard)
        if not allowed:
            return False

        if dest_piece != 0:
            self.pieces.remove(dest_piece)
        self.gameBoard[target] = 0
        self.gameBoard[dest] = piece
        piece.set_square(dest, gameBoard)
        return True

    def set_piece(self, piece, square):
        piece.set_square(square, gameBoard)
        self.gameBoard[square] = piece
        if piece.piece == 'K':
            self.kings[piece.colour] = piece
        self.pieces.add(piece)


class Piece():
    def __init__(self):
        self.square = (None, None)
        self.image = None
        self.xy = (None, None)
        self.on_mouse = False

    def update_xy(self):
        file, rank = self.square
        self.xy = (60*file, 420-60*rank)

    def set_square(self, square, board):
        self.square = square
        self.update_xy()

    def show(self):
        if not self.on_mouse:
            gameDisplay.blit(self.image, self.xy)


class King(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(King, self).__init__()
        self.colour = colour
        self.piece = 'K'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_k{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_distance = abs(dest_rank-rank)
        if file_distance > 1 or rank_distance > 1 or\
                self.square == dest_square or self.colour == dest_colour:
            return False
        else:
            return True


class Queen(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(Queen, self).__init__()
        self.colour = colour
        self.piece = 'Q'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_q{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_distance = abs(dest_rank-rank)
        if not(file_distance == 0 or rank_distance == 0 or file_distance == rank_distance) or\
                self.square == dest_square or self.colour == dest_colour:
            return False

        file_sign = np.sign(dest_file-file)
        rank_sign = np.sign(dest_rank-rank)

        while True:
            file += file_sign
            rank += rank_sign
            if (file, rank) == (dest_file, dest_rank):
                break

            if board[tuple([file, rank])] != 0:
                return False

        return True


class Bishop(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(Bishop, self).__init__()
        self.colour = colour
        self.piece = 'B'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_b{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_distance = abs(dest_rank-rank)
        if not(file_distance == rank_distance) or\
                self.square == dest_square or self.colour == dest_colour:
            return False

        file_sign = np.sign(dest_file-file)
        rank_sign = np.sign(dest_rank-rank)

        while True:
            file += file_sign
            rank += rank_sign
            if (file, rank) == (dest_file, dest_rank):
                break

            if board[tuple([file, rank])] != 0:
                return False

        return True


class Rook(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(Rook, self).__init__()
        self.colour = colour
        self.piece = 'R'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_r{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_distance = abs(dest_rank-rank)
        if not(file_distance == 0 or rank_distance == 0) or\
                self.square == dest_square or self.colour == dest_colour:
            return False

        file_sign = np.sign(dest_file-file)
        rank_sign = np.sign(dest_rank-rank)

        while True:
            file += file_sign
            rank += rank_sign
            if (file, rank) == (dest_file, dest_rank):
                break

            if board[tuple([file, rank])] != 0:
                return False

        return True


class Knight(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(Knight, self).__init__()
        self.colour = colour
        self.piece = 'N'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_n{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_distance = abs(dest_rank-rank)
        if file_distance == 0 or rank_distance == 0 or file_distance+rank_distance != 3 or\
                self.square == dest_square or self.colour == dest_colour:
            return False

        return True


class Pawn(Piece):
    def __init__(self, colour):
        assert colour in {'white', 'black'}

        super(Pawn, self).__init__()
        self.colour = colour
        self.piece = 'P'

        colour_char = {'white': 'l', 'black': 'd'}[colour]
        image_path = f'assets/Chess_p{colour_char}t60.png'
        self.image = pygame.image.load(image_path)

    def set_square(self, square, board):
        rank = square[1]
        if rank == 7 or rank == 0:
            board.pieces.remove(self)
            board.set_piece(Queen(self.colour), square)
        else:
            self.square = square
            self.update_xy()

    def check_legal(self, dest_square, board):
        file, rank = self.square
        dest_file, dest_rank = dest_square
        dest_piece = board[dest_square]
        dest_colour = dest_piece.colour if dest_piece else 0

        file_distance = abs(dest_file-file)
        rank_advance = dest_rank-rank

        if self.square == dest_square or self.colour == dest_colour:
            return False

        if ((rank == 1 and rank_advance == 2 and self.colour == 'white') or
            (rank == 6 and rank_advance == -2 and self.colour == 'black')) and\
                file_distance == 0:
            blockade_square = (file, rank+rank_advance//2)
            blockade_piece = board[blockade_square]
            if blockade_piece == 0:
                return True
            else:
                return False

        if (rank_advance != 1 and self.colour == 'white') or (rank_advance != -1 and self.colour == 'black') or\
                file_distance > 1:

            return False

        if file_distance == 0 and board[dest_square] != 0:
            return False

        if file_distance == 1 and board[dest_square] == 0:
            return False

        return True


gameBoard = GameBoard()


def initalise_pieces():
    gameBoard.set_piece(King('white'), (4, 0))
    gameBoard.set_piece(Queen('white'), (3, 0))
    gameBoard.set_piece(Bishop('white'), (2, 0))
    gameBoard.set_piece(Bishop('white'), (5, 0))
    gameBoard.set_piece(Rook('white'), (0, 0))
    gameBoard.set_piece(Rook('white'), (7, 0))
    gameBoard.set_piece(Knight('white'), (1, 0))
    gameBoard.set_piece(Knight('white'), (6, 0))
    gameBoard.set_piece(Pawn('white'), (0, 1))
    gameBoard.set_piece(Pawn('white'), (1, 1))
    gameBoard.set_piece(Pawn('white'), (2, 1))
    gameBoard.set_piece(Pawn('white'), (3, 1))
    gameBoard.set_piece(Pawn('white'), (4, 1))
    gameBoard.set_piece(Pawn('white'), (5, 1))
    gameBoard.set_piece(Pawn('white'), (6, 1))
    gameBoard.set_piece(Pawn('white'), (7, 1))
    gameBoard.set_piece(King('black'), (4, 7))
    gameBoard.set_piece(Queen('black'), (3, 7))
    gameBoard.set_piece(Bishop('black'), (2, 7))
    gameBoard.set_piece(Bishop('black'), (5, 7))
    gameBoard.set_piece(Rook('black'), (0, 7))
    gameBoard.set_piece(Rook('black'), (7, 7))
    gameBoard.set_piece(Knight('black'), (1, 7))
    gameBoard.set_piece(Knight('black'), (6, 7))
    gameBoard.set_piece(Pawn('black'), (0, 6))
    gameBoard.set_piece(Pawn('black'), (1, 6))
    gameBoard.set_piece(Pawn('black'), (2, 6))
    gameBoard.set_piece(Pawn('black'), (3, 6))
    gameBoard.set_piece(Pawn('black'), (4, 6))
    gameBoard.set_piece(Pawn('black'), (5, 6))
    gameBoard.set_piece(Pawn('black'), (6, 6))
    gameBoard.set_piece(Pawn('black'), (7, 6))


initalise_pieces()

mouse_target = None
mouse_piece = None

turn = 'white'

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = max(1, min(479, x)), max(1, min(479, y))
            x, y = x//60, (480-y)//60
            mouse_target = (x, y)
            mouse_piece = gameBoard.gameBoard[mouse_target]
            if mouse_piece != 0:
                mouse_piece.on_mouse = True

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            x, y = max(1, min(479, x)), max(1, min(479, y))
            x, y = x//60, (480-y)//60
            if mouse_piece != 0:
                if mouse_piece.colour == turn:
                    success = gameBoard.move(mouse_piece, (x, y))
                    if success == True:
                        turn = 'black' if turn == 'white' else 'white'

            # Reset mouse variables
            mouse_target = None
            if mouse_piece != 0:
                mouse_piece.on_mouse = False
            mouse_piece = None

    gameBoard.show()

    if mouse_piece:
        if np.mod(mouse_target[0], 2)-np.mod(mouse_target[1], 2) == 0:
            draw.rect(gameDisplay, light_selected,
                      (60*mouse_target[0], 420-60*mouse_target[1], 60, 60))
        else:
            draw.rect(gameDisplay, dark_selected,
                      (60*mouse_target[0], 420-60*mouse_target[1], 60, 60))

        gameDisplay.blit(mouse_piece.image, np.array(
            pygame.mouse.get_pos())-30)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
