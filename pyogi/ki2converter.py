#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .board import *


SYMBOL_TO_CODE = {'▲': SENTE, '△': GOTE}
KANJI_TO_INT = dict(zip(tuple('一二三四五六七八九'), range(1, 10)))
ZEN_TO_INT =   dict(zip(tuple('１２３４５６７８９'), range(1, 10)))
KANJI_TO_PIECE = {v: k for k, v in piece_kanji.items()}
TURN_PIECE_REVERSED = {v: k for k, v in TURN_PIECE.items()}

class Ki2converter:
    '''Converter from KI2 format to CSA format.
    '''
    def __init__(self):
        self.ki2_txt = ''
        self.moves_ki2 = []
        self.comments = []
        self.infos = []

    def from_path(self, ki2path):

        with open(ki2path, 'r', encoding='shiftjis') as f:
            lines = f.readlines()
       
        self.from_lines(lines)
        self.ki2_txt = ''.join(lines)
 
    def from_txt(self, ki2_txt):
        '''

        ki2_txt : str
            str object of KI2 format
        '''
        self.from_lines(ki2_txt.split('\n'))

    def from_lines(self, lines):
        moves = []
        comments = []
        infos = []

        for line in lines:
            if line.startswith('*'):
                comments.append(line[1:])

            elif line.startswith('▲') or line.startswith('△'):
                line = re.sub('  ', '\u3000', line)
                tesu_line = len(re.findall('[▲△]', line))

                if tesu_line >= 2:
                    moves_line = [line[6*i : 6*(i+1)] 
                                  for i in range(tesu_line+1)]

                    moves.extend(moves_line)

                elif len(line) > 3:
                    moves.append(line)

            else:
                infos.append(line)

        self.moves_ki2 = [re.sub('(\u3000|\n)', '', move) for move in moves]
        while '' in self.moves_ki2:
            self.moves_ki2.remove('')

        self.infos = ''.join(infos)
        self.comments = ''.join(comments)

    def to_csa(self):
    
        self.board = Board()
        self.board.set_initial_state()

        for move_ki2 in self.moves_ki2:
            print(move_ki2)
            move_csa = self.move_ki2_to_csa(move_ki2)

            self.board.move(move_csa)
            print(self.board)


    def move_ki2_to_csa(self, move_ki2):
        '''Convert codes of KI2 format to that of CSA format
        '''
        
        replace_list = [
            ['成桂', '圭'],
            ['成香', '杏'],
            ['成銀', '全'],
            ['龍',   '竜']
        ]
        for l in replace_list:
            move_ki2 = move_ki2.replace(l[0], l[1])
        
        regex = re.compile('([▲△])(同|\d[一二三四五六七八九])(.)(.+)?')
        matched = re.search(regex, move_ki2).groups()
        print(matched)

        code = SYMBOL_TO_CODE[matched[0]]

        if matched[1] == '同':
            i = int(self.board.last_move_txt[3]) - 1
            j = int(self.board.last_move_txt[4]) - 1
        else:
            i = ZEN_TO_INT[matched[1][0]] - 1
            j = KANJI_TO_INT[matched[1][1]] - 1

        piece = KANJI_TO_PIECE[matched[2]]

        teban = int(code == '+')
        direction = 2*teban - 1

        pieces_index = self.board.get_piece_indexes(piece)[1 - teban]
        prev_pos_candidates = []

        ## Search candidate pieces that can move to (i, j)
        for pi, pj in pieces_index:
            koma_act = PIECE_TO_ACT[piece]
            for act in koma_act:
                for move in act:

                    next_i = pi + move[0] * direction
                    next_j = pj + move[1] * direction

                    ## if next_i or next_j is outside of the board
                    if (next_i < 0 or 9 <= next_i or
                        next_j < 0 or 9 <= next_j):
                        break
                    
                    print(i, j, next_i, next_j)

                    if i == next_i and j == next_j:
                        prev_pos_candidates.append([pi, pj])
                    
        ## If promote
        if matched[3] and re.findall('(?<!不)成', matched[3]):
            piece = TURN_PIECE_REVERSED[piece]

        if matched[3] and '打' in matched[3]:
            prev_pos_candidates = [[-1, -1]]

        ## Put piece from mochigoma
        if not prev_pos_candidates:
            prev_pos_candidates = [[-1, -1]]
            
        n_candidates = len(prev_pos_candidates)
        if n_candidates == 1:
            prev_pos = prev_pos_candidates[0]
        elif n_candidates >= 2:
            if matched[3]:
                if '右' in matched[3]:
                    prev_pos = min(prev_pos_candidates,
                                   key = lambda x: x[0] * direction)

                elif '左' in matched[3]:
                    prev_pos = max(prev_pos_candidates,
                                   key = lambda x: x[0] * direction)

                elif '上' in matched[3]:
                    prev_pos = max(prev_pos_candidates,
                                   key = lambda x: x[1] * direction)

                elif '直' in matched[3]:
                    prev_pos_list = [p for p in prev_pos_candidates
                                     if p[0] ==  i]
 
                    prev_pos = max(prev_pos_list,
                                   key = lambda x: x[1] * direction)           
                elif '寄' in matched[3]:
                    prev_pos_list = [p for p in prev_pos_candidates
                                     if p[1] ==  j]
                    if len(prev_pos_list) >= 2:
                        raise RuntimeError('Too many candidates')
                    else:
                        prev_pos = prev_pos_list[0]

                elif '引' in matched[3]:
                    prev_pos_list = [p for p in prev_pos_candidates
                                     if direction*(p[1] - j) < 0]
                    if len(prev_pos_list) >= 2:
                        raise RuntimeError('Too many candidates')
                    else:
                        prev_pos = prev_pos_list[0]
                        
                else:
                    raise RuntimeError('未知の符号')

        else:
            raise RuntimeError('Cannot find prev position.')

        move_csa = ''.join([
            code,
            str(prev_pos[0] + 1),
            str(prev_pos[1] + 1),
            str(i + 1),
            str(j + 1),
            piece
        ])

        return move_csa
