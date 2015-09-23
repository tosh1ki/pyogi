import re
import datetime as dt
from itertools import chain
import numpy as np

from .board cimport Board
from .pieces_act import KOMA_INFOS
from .teai_options import KOMAOCHI_CSA_TO_CODE

import pdb

from cpython cimport bool as bool_t


REGEXP_MOVES = re.compile('\'指し手と消費時間\n(.+)\n', re.S)
REGEXP_DATETIME = re.compile('^\$START_TIME:([\d/:\s\w]+)\n', re.S | re.M)
REGEXP_PLAYERS = re.compile('\'対局者名\nN\+\n(.+?)\nN-\n(.+?)\n', re.S)
REGEXP_OPENING = re.compile('\'戦型:(.+?)\n', re.S)


cdef class Kifu:

    '''Class for handling kifu

    Args
    -------------------
    kifu_txt : str
        kifu text of shogiwars format

    Member variable
    -------------------
    kifu_txt : str
    moves : list of str
    times
    board
    sente_win : bool
    is_sennichite
    datetime
    description
    teai
    opening
    '''
    cdef:
        readonly str kifu_txt, datetime, description, opening
        public str teai
        public list moves, players, times
        readonly bool_t sente_win, gote_win, is_sennichite, is_jishogi, is_chudan, extracted
        readonly Board board
        readonly int tesu

    def __init__(self):
        self.kifu_txt = ''
        self.moves = []

        self.sente_win = None
        self.gote_win = None
        self.is_sennichite = None
        self.is_jishogi = None
        self.is_chudan = None

        self.datetime = None
        self.description = ''
        self.players = []
        self.times = []
        self.teai = 'hirate'
        self.extracted = None
        self.opening = ''

        self.board = Board()

    cpdef int from_csa(self, str csa_txt):
        self.kifu_txt = csa_txt
        self.extracted = self.extract_infomation()
        self.reset_board()

    def __repr__(self):
        return 'pyogi.kifu object'

    def __str__(self):
        return self.kifu_txt

    cpdef int set_players_name(self, list names):
        self.players = names
        self.board.players = names

    def reset_board(self):
        self.board.set_initial_state(teai=self.teai)

    def extract_infomation(self):
        '''Extract infomations from kifu text.
        '''
        match = re.search(REGEXP_MOVES, self.kifu_txt)
        if match and len(match.groups()) > 0:
            move_txt = match.groups()[0]
        else:
            return False

        self.moves = move_txt.split('\n')[::2]
        self.tesu = len(self.moves)

        times = move_txt.split('\n')[1::2]
        self.times = list(map(lambda x: int(x[1:]), times))

        self.is_sennichite = self.kifu_txt.endswith('%SENNICHITE')
        self.is_jishogi = self.kifu_txt.endswith('%JISHOGI')
        self.is_chudan = self.kifu_txt.endswith('%CHUDAN')

        if self.kifu_txt.endswith('%TORYO'):
            self.sente_win = (self.tesu % 2 == 1)
            self.gote_win = (self.tesu % 2 == 0)
        else:
            self.sente_win = False
            self.gote_win = False


        komaochi_match = re.findall('^PI.+$', self.kifu_txt, re.M)
        if komaochi_match:
            komaochi_txt = komaochi_match[0]
            self.teai = KOMAOCHI_CSA_TO_CODE[komaochi_txt]            

        match = re.search(REGEXP_DATETIME, self.kifu_txt)
        if match:
            self.datetime = match.groups()[0]

        match = re.search(REGEXP_PLAYERS, self.kifu_txt)
        if len(match.groups()) == 2:
            self.set_players_name(list(match.groups()))

        match = re.search(REGEXP_OPENING, self.kifu_txt)
        if match:
            self.opening = match.groups()[0]

        return True

    def print_state(self, tesu=-1, mode='cui'):
        '''Print state of the kifu

        Args
        -------------------
        tesu : int, optional (default = -1)
            This function prints board at `tesu`.
        mode : str, optional (default = 'cui')
            'cui' : Print state using command line
            'mpl' : Print state using matplotlib
        '''
        new_board = Board()
        new_board.players = self.board.players
        new_board.set_initial_state(teai=self.board.teai)

        for n, move in enumerate(self.moves):
            if tesu == -1 or n < tesu:
                if not move.startswith('%'):
                    new_board.move(move)
                else:
                    print(move)

        if mode == 'cui':
            print(new_board)
            print()
        elif mode == 'mpl':
            new_board.plot_state_mpl()
        else:
            raise RuntimeError('Invalid mode', mode)

    cpdef get_forking(self, list target, bool_t display=True):
        '''Returns list of a time which there is a piece forked.

        For example, if this function is called like 
        `kifu.get_forking(target=['OU', 'HI'])`,
        this returns a list of time at which state there is a piece forked.
        If there is no piece forked, it returns None.

        Returns
        -------------------
        sente_forked : list
        gote_forked  : list
        sente_forked_and_picked : list
        gote_forked_and_picked : list
        '''
        cdef:
            list sente_forked_list = []
            list gote_forked_list = []
            list sente_forked_and_picked = []
            list gote_forked_and_picked = []
            bool_t appended = False, sente_forked, gote_forked
            int n
            str move
            list results

        for n, move in enumerate(self.moves):
            if not move.startswith('%'):
                res_move = self.board.move(move)
                sente_forked, gote_forked = self.board.is_forking(target, display=False)

                # If forking pieces of target
                if sente_forked:
                    sente_forked_list.append(n + 1)
                if gote_forked:
                    gote_forked_list.append(n + 1)

                # If forked at previous state and picked piece of target,
                # save and plot state.
                if n - 1 in sente_forked_list and res_move[1] in target:
                    sente_forked_and_picked.append(n + 1)
                    appended = True

                if n - 1 in gote_forked_list and res_move[1] in target:
                    gote_forked_and_picked.append(n + 1)
                    appended = True

                if appended and display:
                    self.print_state(tesu=n-1, mode='mpl')
                    self.board.plot_state_mpl()

                appended = False

        return [sente_forked_list, gote_forked_list,
                sente_forked_and_picked, gote_forked_and_picked]

    def make_features(self):
        new_board = Board()
        new_board.players = self.board.players
        new_board.set_initial_state(teai=self.board.teai)

        sum_list = [[[] for _ in range(9)] for _ in range(9)]

        counts_list = []

        for move_csa in self.moves:
            new_board.move(move_csa)

            for i in range(9):
                for j in range(9):
                    grid = new_board[i][j]
                    
                    if not (grid.is_empty() or grid.which_player == '-'):
                        sum_list[i][j].append(grid.koma.csa)

        
        for koma_csa in KOMA_INFOS.csa.pipe(list):
            count_koma = [[None for _ in range(9)] for _ in range(9)]

            for i in range(9):
                for j in range(9):
                    count_koma[i][j] = sum_list[i][j].count(koma_csa)

            counts_list.extend(count_koma)

        return np.array(list(chain.from_iterable(counts_list)))
