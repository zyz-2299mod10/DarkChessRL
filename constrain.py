class rule:
    width = 8
    height = 4
    num_cell = width * height
    red_pieces = ['K'] + ['G']*2 + ['M']*2 + ['R']*2 + ['N']*2 + ['C']*2 + ['P']*5
    black_pieces = ['k'] + ['g']*2 + ['m']*2 + ['r']*2 + ['n']*2 + ['c']*2 + ['p']*5
    rank = {'k':6, 'g':5, 'm':4, 'r':3, 'n':2, 'c':1, 'p':0,
            'K':6, 'G':5, 'M':4, 'R':3, 'N':2, 'C':1, 'P':0}