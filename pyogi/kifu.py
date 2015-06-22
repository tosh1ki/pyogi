#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime as dt

import pdb

from .board import Board


regexp_moves = re.compile('\'指し手と消費時間\n(.+)\n', re.S)
regexp_datetime = re.compile('^\$START_TIME:([\d/:\s\w]+)\n', re.S | re.M)
regexp_player = re.compile('\'対局者名\nN\+\n(.+?)\nN-\n(.+?)\n', re.S)


class Kifu:

    '''Class for handling kifu

    Args
    -------------------
    kifu_txt : str
        kifu text of shogiwars format

    Member variable
    -------------------
    kifu_txt
    moves
    sente_win
    datetime
    description
    '''

    def __init__(self, kifu_txt):
        self.kifu_txt = kifu_txt
        self.moves = []
        self.sente_win = None
        self.datetime = None
        self.description = ''
        self.players = []
        self.times = []
        self.teai = ''

        self.board = Board()
        self.reset_board()

        self.extracted = self.extract_infomation()

    def __repr__(self):
        return 'pyogi.kifu object'

    def __str__(self):
        return self.kifu_txt

    def reset_board(self, teai='hirate'):
        self.board.set_initial_state(teai=teai)
        self.teai = teai

    def extract_infomation(self):
        '''Extract infomations from kifu text.
        '''
        match = re.search(regexp_moves, self.kifu_txt)
        if match and len(match.groups()) > 0:
            move_txt = match.groups()[0]
        else:
            return False

        self.moves = move_txt.split('\n')[::2]
        times = move_txt.split('\n')[1::2]
        self.times = list(map(lambda x: int(x[1:]), times))
        self.tesu = len(self.moves)
        self.is_sennichite = self.kifu_txt.endswith('%SENNICHITE')
        self.sente_win = self.tesu % 2 == 1

        match = re.search(regexp_datetime, self.kifu_txt)
        if match:
            self.datetime = match.groups()[0]

        match = re.search(regexp_player, self.kifu_txt)
        self.players = list(match.groups())

        return True

    def print_state(self, tesu=-1, mode='cui'):
        '''Print state of the game
        '''
        new_board = Board()
        new_board.set_initial_state(teai=self.teai)
        
        for n, move in enumerate(self.moves):
            if tesu == -1 or n < tesu:
                if not move.startswith('%'):
                    new_board.move(move)
                else:
                    print(move)

        if mode == 'cui':
            print(new_board)
            print()
        else:
            new_board.plot_state_mpl()

    def get_state(self, tesu=-1):
        '''Get state of game at specific tesu.

        Args
        -------------------
        tesu : int, optional (defaults = -1)
           Returns last state of game if tesu == -1
        '''
        pass

    def get_forking(self, target):
        '''先手と後手それぞれが何手目に王飛両取りをかけられたかを探索し，
        それをリストにまとめて返す．両取りをかけられていなければNoneを返す．
        [TODO] 英訳

        Returns
        -------------------
        sente_forked : list
        gote_forked  : list
        '''
        sente_forked = []
        gote_forked = []
        sente_forked_and_picked = []
        gote_forked_and_picked = []

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
                    self.print_state(tesu=n-1, mode='mpl')
                    self.board.plot_state_mpl()
                if n - 1 in gote_forked and res_move[1] in target:
                    gote_forked_and_picked.append(n + 1)
                    self.print_state(tesu=n-1, mode='mpl')
                    self.board.plot_state_mpl()

        return [sente_forked, gote_forked,
                sente_forked_and_picked, gote_forked_and_picked]


if __name__ == '__main__':

    kifu_path = './../testgetfork.csa'
    with open(kifu_path, 'r') as f:
        kifu_txt = f.read()

    kifu = Kifu(kifu_txt)
    results = kifu.get_forking(['OU', 'HI'])
