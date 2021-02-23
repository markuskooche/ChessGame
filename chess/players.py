from chess.player import Player, ComputerizedPlayer
from random import choice, shuffle

CHECKMATE: int = 1000
STALEMATE: int = 0


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

        max_score = -CHECKMATE
        best_move = None

        for player_move in self.legal_moves(board):
            board.move_piece(player_move)

            # if the enemy has no legal ‚moves after this move before
            if not self.enemy.is_checkmate:
                score = CHECKMATE
            elif self.enemy.is_stalemate:
                score = STALEMATE
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

        enemy_min_max_score = CHECKMATE
        best_player_move = None

        # without shuffle he would prefer the rook, because it is in the first place
        valid_moves = self.legal_moves(board)
        shuffle(valid_moves)

        for player_move in valid_moves:
            board.move_piece(player_move)
            enemy_moves = self.enemy.legal_moves(board)
            enemy_max_score = -CHECKMATE

            for enemy_move in enemy_moves:
                board.move_piece(enemy_move)

                # if the enemy has no legal ‚moves after this move before
                if self.enemy.is_checkmate:
                    score = - turn_multiplier * CHECKMATE
                elif self.enemy.is_stalemate:
                    score = STALEMATE
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

        enemy_min_max_score = CHECKMATE
        best_player_move = None

        # without shuffle he would prefer the rook, because it is in the first place
        valid_moves = self.legal_moves(board)
        shuffle(valid_moves)

        for player_move in valid_moves:
            board.move_piece(player_move)
            enemy_moves = self.enemy.legal_moves(board)

            if self.is_checkmate:
                enemy_max_score = - CHECKMATE
            elif self.is_stalemate:
                enemy_max_score = STALEMATE
            else:
                enemy_max_score = - CHECKMATE

                for enemy_move in enemy_moves:
                    board.move_piece(enemy_move)

                    # if the enemy has no legal ‚moves after this move before
                    if self.enemy.is_checkmate:
                        score = - turn_multiplier * CHECKMATE
                    elif self.enemy.is_stalemate:
                        score = STALEMATE
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
