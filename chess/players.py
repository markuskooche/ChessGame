from chess.player import Player, ComputerizedPlayer
from random import choice, shuffle

# CHECKMATE: int = 1000
# STALEMATE: int = 0


class HumanPlayer(Player):
    """
    A 'HumanPlayer' is controlled by a human and reacts to inputs on the board.
    It is only as smart as the human player behind it. It allows only legal moves but does not test whether a 'King'
    is in check after this move or whether a piece is pinned due to a check.
    The player behind the computer is responsible for these operations.
    """

    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)
        self.next_move = None

    # pins are not checked at a HumanPlayer
    # the player is responsible for this himself
    def legal_moves(self, board: object) -> object:
        """
        Returns allowed moves but does not recognize chess or pinned pieces.
        """

        return self.legal_moves_simple(board)

    def best_move(self, board: object) -> object:
        if self.next_move is not None:
            return self.next_move
        else:
            return None

    def set_move(self, move: object):
        self.next_move = move


class RandomPlayer(ComputerizedPlayer):
    """
    A 'RandomPlayer' is a computerized player and inherits from 'ComputerizedPlayer'.
    It calculates a random allowed move.
    """

    def __init__(self, color: str):
        super().__init__(color=color, name='Random')

    def best_move(self, board: object) -> object:
        """
        Returns a random legal move.
        """

        move = None

        try:
            move = choice(self.legal_moves(board))
        except IndexError:
            print('There are no more figures that have legal moves!')
            # sys.exit()

        return move


class GreedyPlayer(ComputerizedPlayer):
    """
    A 'GreedyPlayer' is a computerized player and inherits from 'ComputerizedPlayer'.
    It always chooses the best current move by looking one step further.
    """

    def __init__(self, color: str):
        super().__init__(color=color, name='Greedy')

    def best_move(self, board: object) -> object:
        """
        Returns a greedy move.
        """

        # to handle black and white players
        turn_multiplier = 1 if self.color == 'white' else -1

        max_score = - self.CHECKMATE
        best_move = None

        for player_move in self.legal_moves(board):
            board.move_piece(player_move)

            # if the enemy has no legal ‚moves after this move before
            if not self.enemy.is_checkmate:
                score = self.CHECKMATE
            elif self.enemy.is_stalemate:
                score = self.STALEMATE
            else:
                score = turn_multiplier * ComputerizedPlayer.score_board(board)

            if score > max_score:
                max_score = score
                best_move = player_move

            board.undo_move()

        return best_move


class MiniMaxIterativePlayer(ComputerizedPlayer):
    """
    A 'MiniMaxIterativePlayer' is a computerized player and inherits from 'ComputerizedPlayer'.
    He looks two moves ahead and chooses his own best move from them.
    """

    def __init__(self, color: str):
        super().__init__(color=color, name='MiniMaxIterative')

    def best_move(self, board: object) -> object:
        """
        Returns the best move after two iterations
        """

        # to handle black and white players
        turn_multiplier = 1 if self.color == 'white' else -1

        enemy_min_max_score = self.CHECKMATE
        best_player_move = None

        # without shuffle he would prefer the rook, because it is in the first place
        valid_moves = self.legal_moves(board)
        shuffle(valid_moves)

        for player_move in valid_moves:
            board.move_piece(player_move)
            enemy_moves = self.enemy.legal_moves(board)
            enemy_max_score = - self.CHECKMATE

            for enemy_move in enemy_moves:
                board.move_piece(enemy_move)

                # if the enemy has no legal ‚moves after this move before
                if self.enemy.is_checkmate:
                    score = - turn_multiplier * self.CHECKMATE
                elif self.enemy.is_stalemate:
                    score = self.STALEMATE
                else:
                    score = - turn_multiplier * ComputerizedPlayer.score_board(board)

                if score > enemy_max_score:
                    enemy_max_score = score

                board.undo_move()

            if enemy_max_score < enemy_min_max_score:
                enemy_min_max_score = enemy_max_score
                best_player_move = player_move

            board.undo_move()

        return best_player_move


class MiniMaxPlayer(ComputerizedPlayer):
    """
    A 'MiniMaxPlayer' is a computerized player and inherits from 'ComputerizedPlayer'.
    He chooses the best own move.
    """

    def __init__(self, color: str, max_depth=3):
        super().__init__(color=color, name='MiniMaxIterative')
        self.next_move = None
        self.MAX_DEPTH = max_depth

    def best_move(self, board: object) -> object:
        """
        Returns the best move by given depth.
        """

        # reset next move from before
        self.next_move = None

        is_white = self.color == 'white'
        self.find_move(board, is_white, self.MAX_DEPTH)

        return self.next_move

    def find_move(self, board: object, is_white: bool, depth: int):
        """
        A recursive method to find the best move by given depth.
        """
        
        if depth == 0:
            return self.score_board_improved(board)

        valid_moves = []

        if self.color == 'white':
            if is_white:
                valid_moves = self.legal_moves(board)
            else:
                valid_moves = self.enemy.legal_moves(board)

        elif self.color == 'black':
            if is_white:
                valid_moves = self.enemy.legal_moves(board)
            else:
                valid_moves = self.legal_moves(board)

        if is_white:
            max_score = - self.CHECKMATE

            for move in valid_moves:
                board.move_piece(move)
                # enemy_moves = self.enemy.legal_moves(board)
                score = self.find_move(board, False, depth - 1)

                if score > max_score:
                    max_score = score

                    if depth == self.MAX_DEPTH:
                        self.next_move = move

                board.undo_move()

            return max_score

        else:
            min_score = self.CHECKMATE

            for move in valid_moves:
                board.move_piece(move)
                # enemy_moves = self.enemy.legal_moves(board)
                score = self.find_move(board, True, depth - 1)

                if score < min_score:
                    min_score = score

                    if depth == self.MAX_DEPTH:
                        self.next_move = move

                board.undo_move()

            return min_score
