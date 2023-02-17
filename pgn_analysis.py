import chess.pgn
import chess.engine
import time

pgn_file = 'lichess.pgn'


def convert_sec(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def format_moves(pv):
    return ', '.join([move.uci() for move in pv])


def process_game(game):
    i = 0
    board = game.board()
#    res = game.headers['Result']

    for move in game.mainline_moves():
        i += 1
        move_str = str(board.san(move))
        
        if i % 2 == 1:
            move_str = str(i // 2 + 1) + '. ' + move_str
        else:
            move_str = str(i // 2) + '...' + move_str

        pos = board.fen()
        info = engine.analyse(board, chess.engine.Limit(depth=14))        
        board.push(move)
        
        print(f"Score: {info['score'].white().score() / 100}")
        print(f"Best line: {format_moves(info['pv'])}")
        print(move_str, pos)
        print("")


def process_pgn(file):
    t1 = time.time()
    total = 0

    pgn = open(file)
    game = chess.pgn.read_game(pgn)

    while game:
        total += 1
        process_game(game)
        print(total, convert_sec(time.time() - t1))
        
        game = chess.pgn.read_game(pgn)


if __name__ == '__main__':
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    process_pgn(pgn_file)
    engine.quit()
    print('done!')
