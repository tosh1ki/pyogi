#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime as dt
import copy

import pdb

from .board import Board
from .pieces_act import KOMAOCHI_CSA_TO_CODE

REGEXP_MOVES = re.compile('\'指し手と消費時間\n(.+)\n', re.S)
REGEXP_DATETIME = re.compile('^\$START_TIME:([\d/:\s\w]+)\n', re.S | re.M)
REGEXP_PLAYERS = re.compile('\'対局者名\nN\+\n(.+?)\nN-\n(.+?)\n', re.S)


class Kifu:

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
    '''

    def __init__(self, kifu_txt):
        self.kifu_txt = kifu_txt
        self.moves = []

        self.sente_win = None
        self.is_sennichite = None
        self.is_jishogi = None

        self.datetime = None
        self.description = ''
        self.players = []
        self.times = []
        self.teai = 'hirate'

        self.board = Board()
        self.extracted = self.extract_infomation()
        self.reset_board(teai=self.teai)

    def __repr__(self):
        return 'pyogi.kifu object'

    def __str__(self):
        return self.kifu_txt

    def set_players_name(self, names):
        self.players = names
        self.board.players = names

    def reset_board(self, teai='hirate'):
        self.board.set_initial_state(teai=teai)
        self.teai = teai

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
        self.sente_win = self.tesu % 2 == 1

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
        new_board = copy.deepcopy(self.board)
        new_board.set_initial_state(teai=new_board.teai)

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

    def get_forking(self, target, display=True):
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
        sente_forked = []
        gote_forked = []
        sente_forked_and_picked = []
        gote_forked_and_picked = []
        appended = False

        for n, move in enumerate(self.moves):
            if not move.startswith('%'):
                res_move = self.board.move(move)
                results = self.board.is_forking(target, display=False)

                # If forking pieces of target
                if results[0]:
                    sente_forked.append(n + 1)
                if results[1]:
                    gote_forked.append(n + 1)

                # If forked at previous state and picked piece of target,
                # save and plot state.
                if n - 1 in sente_forked and res_move[1] in target:
                    sente_forked_and_picked.append(n + 1)
                    appended = True

                if n - 1 in gote_forked and res_move[1] in target:
                    gote_forked_and_picked.append(n + 1)
                    appended = True

                if appended and display:
                    self.print_state(tesu=n-1, mode='mpl')
                    self.board.plot_state_mpl()

                appended = False

        return [sente_forked, gote_forked,
                sente_forked_and_picked, gote_forked_and_picked]
