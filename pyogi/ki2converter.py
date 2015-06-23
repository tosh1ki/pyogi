#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .board import *


SYMBOL_TO_CODE = {'▲': TEBAN_CODE[0], '△': TEBAN_CODE[1]}
KANJI_TO_INT = dict(zip(tuple('一二三四五六七八九'), range(1, 10)))
ZEN_TO_INT = dict(zip(tuple('１２３４５６７８９'), range(1, 10)))
KANJI_TO_PIECE = {v: k for k, v in piece_kanji.items()}
TURN_PIECE_REVERSED = {v: k for k, v in TURN_PIECE.items()}
REGEX_MOVE = re.compile('([▲△](?:同\u3000)?[^▲△\s]+)')


class Ki2converter:

    '''Converter from KI2 format to CSA format.
    '''

    def __init__(self):
        self.ki2_txt = ''
        self.moves_ki2 = []
        self.comments = []
        self.infos = []

    def from_path(self, ki2path):

        try:
            with open(ki2path, 'r', encoding='shiftjis') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(ki2path, 'r', encoding='CP932') as f:
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
            # Comment line
            if line.startswith('*'):
                comments.append(line[1:])

            # Move line
            elif line.startswith('▲') or line.startswith('△'):
                line = re.sub('  ', '\u3000', line)
                tesu_line = len(re.findall('[▲△]', line))

                if tesu_line >= 2:
                    moves_line = re.findall(REGEX_MOVE, line)
                    moves.extend(moves_line)

                elif len(line) > 3:
                    moves.append(line)

            # Header information
            else:
                infos.append(line)

        self.moves_ki2 = [re.sub('(\u3000|\n)', '', move) for move in moves]
        while '' in self.moves_ki2:
            self.moves_ki2.remove('')

        self.infos = ''.join(infos)
        self.comments = ''.join(comments)

    def extract_header_infos(self):
        header_infos = {}
        queries = [
            ['sente', '^先手：(.+)'],
            ['gote', '^後手：(.+)'],
            ['start_time', '^開始日時：(.+)'],
            ['site', '^場所：(.+)'],
            ['event', '^棋戦：(.+)'],
            ['opening', '^戦型：(.+)'],
            ['time', '^持ち時間：(.+)']
        ]
        for query in queries:
            match = re.findall(query[1], self.ki2_txt, re.M)

            if match:
                header_infos[query[0]] = match[0]

        # Detect teai
        if '手合割：平手' in self.ki2_txt:
            teai = 'hirate'
        elif '手合割：角落ち' in self.ki2_txt:
            teai = 'kakuoti'
        elif '手合割：飛車落ち' in self.ki2_txt:
            teai = 'hisyaoti'
        elif '手合割：飛香落ち' in self.ki2_txt:
            teai = 'hikyouoti'
        elif '手合割：香落ち' in self.ki2_txt:
            teai = 'kyouoti'
        elif '手合割：右香落ち' in self.ki2_txt:
            teai = 'migikyouoti'
        elif '手合割：二枚落ち' in self.ki2_txt:
            teai = 'nimaioti'
        elif '手合割：三枚落ち' in self.ki2_txt:
            teai = 'sanmaioti'
        elif '手合割：四枚落ち' in self.ki2_txt:
            teai = 'yonmaioti'
        elif '手合割：六枚落ち' in self.ki2_txt:
            teai = 'rokumaioti'
        elif '手合割：その他' in self.ki2_txt:
            return -1
        else:
            if not '手合割' in self.ki2_txt:
                teai = 'hirate'
            else:
                raise RuntimeError('invalid teai')

        header_infos['teai'] = teai

        return header_infos

    def to_csa(self):

        self.board = Board()
        header_infos = self.extract_header_infos()

        if header_infos == -1:
            return None

        self.board.set_initial_state(teai=header_infos['teai'])

        # とりあえず
        if '上手' in self.ki2_txt:
            return None

        csa_kifu = [
            '\'バージョン',
            'V2.2',
            '\'対局者名',
            'N+', header_infos['sente'],
            'N-', header_infos['gote'],
            '\'棋譜情報',
            '\'棋戦名',
            '$EVENT:' + header_infos.get('event', ''),
            '\'対局場所',
            '$SITE:' + header_infos.get('site', ''),
            '\'開始日時',
            '$START_TIME:' + header_infos.get('start_time', ''),
            '\'持ち時間:' + header_infos.get('time', ''),
            '\'$TIME_LIMIT:',
            '\'先手番', '+',
            '\'指し手と消費時間'
        ]

        # Move pieces
        for move_ki2 in self.moves_ki2:
            move_csa = self.move_ki2_to_csa(move_ki2)
            self.board.move(move_csa)

            csa_kifu.append(move_csa)
            csa_kifu.append('T0')

        if self.ki2_txt.endswith('勝ち\n'):
            csa_kifu.append('%TORYO')
        elif self.ki2_txt.endswith('千日手\n'):
            csa_kifu.append('%SENNICHITE')

        csa = '\n'.join(csa_kifu)

        return csa

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

        # print(matched)

        code = SYMBOL_TO_CODE[matched[0]]

        if matched[1] == '同':
            i = int(self.board.last_move_txt[3]) - 1
            j = int(self.board.last_move_txt[4]) - 1
        else:
            i = ZEN_TO_INT[matched[1][0]] - 1
            j = KANJI_TO_INT[matched[1][1]] - 1

        piece = KANJI_TO_PIECE[matched[2]]

        teban = int(code == '+')
        direction = 2 * teban - 1

        pieces_index = self.board.get_piece_indexes(piece)[1 - teban]
        prev_pos_candidates = []

        # Search candidate pieces that can move to (i, j)
        for pi, pj in pieces_index:
            koma_act = PIECE_TO_ACT[piece]
            for act in koma_act:
                for move in act:

                    next_i = pi + move[0] * direction
                    next_j = pj + move[1] * direction

                    # If next_i or next_j is outside of the board
                    if (next_i < 0 or 9 <= next_i or
                            next_j < 0 or 9 <= next_j):
                        break

                    # If conflict with the piece of move_ki2
                    if i == next_i and j == next_j:
                        prev_pos_candidates.append([pi, pj])

                    # If conflict with other pieces
                    if self.board[next_i][next_j] != empty_str:
                        break

        # If promote
        if matched[3] and re.findall('(?<!不)成', matched[3]):
            piece = TURN_PIECE_REVERSED[piece]

        if matched[3] and '打' in matched[3]:
            prev_pos_candidates = [[-1, -1]]

        # Put piece from mochigoma
        if not prev_pos_candidates:
            prev_pos_candidates = [[-1, -1]]

        n_candidates = len(prev_pos_candidates)
        if n_candidates == 1:
            prev_pos = prev_pos_candidates[0]

        elif n_candidates >= 2:
            if matched[3]:
                if '右' in matched[3]:
                    if piece in ['HI', 'KA', 'RY', 'UM']:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction >= 0,
                            prev_pos_candidates)
                    else:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction > 0,
                            prev_pos_candidates)
                elif '左' in matched[3]:
                    if piece in ['HI', 'KA', 'RY', 'UM']:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction <= 0,
                            prev_pos_candidates)
                    else:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction < 0,
                            prev_pos_candidates)

                if '上' in matched[3] or '行' in matched[3]:
                    prev_pos_candidates = filter(
                        lambda x: (x[1] - j) * direction > 0,
                        prev_pos_candidates
                    )
                elif '直' in matched[3]:
                    prev_pos_candidates = filter(
                        lambda x: x[0] == i and (x[1] - j) * direction > 0,
                        prev_pos_candidates
                    )
                elif '寄' in matched[3]:
                    prev_pos_candidates = filter(
                        lambda x: x[1] == j,
                        prev_pos_candidates
                    )
                elif '引' in matched[3]:
                    prev_pos_candidates = filter(
                        lambda x: (x[1] - j) * direction < 0,
                        prev_pos_candidates
                    )

                if (piece in ['HI', 'KA', 'RY', 'UM'] and
                            ('右' in matched[3] or '左' in matched[3])
                        ):
                    if '右' in matched[3]:
                        lr = -1
                    elif '左' in matched[3]:
                        lr = 1

                    prev_pos_candidates = [
                        max(prev_pos_candidates,
                            key=lambda x: lr * direction * x[0])
                    ]

                prev_pos_candidates = list(prev_pos_candidates)
                if (not prev_pos_candidates or
                        len(prev_pos_candidates) >= 2):
                    raise RuntimeError('Parse Error')

                prev_pos = prev_pos_candidates[0]
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
