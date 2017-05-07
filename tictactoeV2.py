from tttclasses import *

def main():
    total = [0,0,0]     ##p1, p2, draw
    turnswitch = False
    with tttai_learn() as p1:
        for i in range(10000):
            game = tttboard(turn = int(turnswitch) + 1)
            p1.board = game
            p2 = tttai_rand(game)
            result = 0
            while result == 0:
                if game.turn == 1:
                    result = p1.makeaimove(disp = True)
                    ##print('Learning AI made move.')
                else:
                    result = p2.makeaimove(disp = True)
                    ##print('Rand AI made move.')
            if result == 1:
                print('Learning AI won this round.')
                total[0] += 1
            elif result == 2:
                print('Rand AI won this round.')
                total[1] += 1
            else:
                total[2] += 1
            turnswitch = not turnswitch
    print('Learning AI won {} times. Rand AI won {} times.\nThey draw {} times.'.format(total[0], total[1], total[2]))
if __name__ == '__main__':
    main()