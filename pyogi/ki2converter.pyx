import re

from .board cimport Board
from .pieces_act import PIECE_TO_ACT, TURN_PIECE_REVERSED, KANJI_TO_PIECE, KOMA_INFOS
from teai_options import KOMAOCHI_CODE_TO_CSA, TEAITXT_TO_TEAI

import pdb


cdef dict SYMBOL_TO_CODE = {'▲': '+', '△': '-'}
REGEX_MOVE = re.compile('([▲△](?:同\u3000)?[^▲△\s]+)')
REGEX_KI2_MOVE = re.compile('([▲△])(同|[\d一二三四五六七八九]{2})(.)(.+)?')
cdef list OGOMA = KOMA_INFOS.query('ogoma == True').csa.pipe(list)

cdef dict TO_INT = {str(r): r for r in range(1, 10)}
TO_INT.update(dict(zip(tuple('一二三四五六七八九'), range(1, 10))))
TO_INT.update(dict(zip(tuple('１２３４５６７８９'), range(1, 10))))


cdef class Ki2converter:

    '''Converter from KI2 format to CSA format.
    '''
    cdef:
        readonly str ki2_txt, comments, infos
        readonly list moves_ki2
        readonly Board board

    def __init__(self):
        self.ki2_txt = ''
        self.moves_ki2 = []
        self.comments = ''
        self.infos = ''
        self.board = Board()

    def from_path(self, ki2path):

        try:
            with open(ki2path, 'r', encoding='shiftjis') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(ki2path, 'r', encoding='CP932') as f:
                lines = f.readlines()

        self.from_lines(lines)
        self.ki2_txt = ''.join(lines)

    cpdef int from_txt(self, str ki2_txt):
        '''

        ki2_txt : str
            str object of KI2 format
        '''
        self.ki2_txt = ki2_txt
        self.from_lines(ki2_txt.split('\n'))

    cpdef int from_lines(self, list lines):
        cdef:
            str line, move
            int tesu_line

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
        header_infos = {'senteban': '+'}
        queries = [
            ['sente', '^\s*[先下]手：(.+)'],
            ['gote', '^\s*[後上]手：(.+)'],
            ['start_time', '^\s*開始日時：(.+)'],
            ['end_time', '^\s*終了日時：(.+)'],
            ['site', '^\s*場所：(.+)'],
            ['event', '^\s*棋戦：(.+)'],
            ['opening', '^\s*戦型：(.+)'],
            ['time', '^\s*持ち時間：(.+)']
        ]
        for query in queries:
            match = re.findall(query[1], self.ki2_txt, re.M)

            if match:
                header_infos[query[0]] = match[0]

        # Detect teai
        for t_teaitxt, t_teai in TEAITXT_TO_TEAI.items():
            if t_teaitxt in self.ki2_txt:
                teai = t_teai
                break
        else:
            if not '手合割' in self.ki2_txt:
                teai = 'hirate'
            else:
                raise RuntimeError('invalid teai')

        header_infos['teai'] = teai
        if teai == 'sonota':
            # とりあえず
            return -1

        elif teai != 'hirate':
            header_infos['csa_komaochi'] = KOMAOCHI_CODE_TO_CSA[teai]
            header_infos['senteban'] = '-'

        if not ('sente' in header_infos and 'gote' in header_infos):
            return -1

        return header_infos

    def to_csa(self):

        header_infos = self.extract_header_infos()

        if header_infos == -1:
            return None

        self.board.set_initial_state(teai=header_infos['teai'])

        # とりあえず
        if re.search('手合割：.{,2}落ち', self.ki2_txt):
            komaochi_txt = '\n' + header_infos['csa_komaochi']
        else:
            komaochi_txt = ' 初期配置'

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
            '\'戦型:' + header_infos.get('opening', ''),
            '\'開始局面' + komaochi_txt,
            '\'先手番', header_infos['senteban'],
            '\'指し手と消費時間'
        ]

        # Move pieces
        for move_ki2 in self.moves_ki2:
            move_csa = self.move_ki2_to_csa(move_ki2)

            # If move_ki2_to_csa cannot read `move_ki2`
            if not move_csa:
                print(self.board)
                raise Exception('Parse error at Kifu.move_ki2_to_csa')

            self.board.move(move_csa)

            csa_kifu.append(move_csa)
            csa_kifu.append('T0')

        if re.findall('勝ち\n*$', self.ki2_txt):
            csa_kifu.append('%TORYO')
        elif re.findall('千日手\n*$', self.ki2_txt):
            csa_kifu.append('%SENNICHITE')
        elif re.findall('持将棋\n*$', self.ki2_txt):
            csa_kifu.append('%JISHOGI')
        elif re.findall('中断\n*$', self.ki2_txt):
            csa_kifu.append('%CHUDAN')
        else:
            return None

        return '\n'.join(csa_kifu)

    def move_ki2_to_csa(self, move_ki2):
        '''Convert codes of KI2 format to that of CSA format
        '''
        prev_pos = None
        replace_list = [
            ['成桂', '圭'],
            ['成香', '杏'],
            ['成銀', '全'],
            ['龍',   '竜']
        ]
        for l in replace_list:
            move_ki2 = move_ki2.replace(l[0], l[1])
        
        reg = re.search(REGEX_KI2_MOVE, move_ki2)

        if reg:
            matched = reg.groups()
        else:
            print('move_ki2 is not matched to REGEX_KI2_MOVE')
            return None
        
        code = SYMBOL_TO_CODE[matched[0]]

        if matched[1] == '同':
            i = int(self.board.last_move_txt[3]) - 1
            j = int(self.board.last_move_txt[4]) - 1
        else:
            i = TO_INT[matched[1][0]] - 1
            j = TO_INT[matched[1][1]] - 1

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
                    if not self.board[next_i][next_j].is_empty():
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
                    if piece in OGOMA:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction >= 0,
                            prev_pos_candidates)
                    else:
                        prev_pos_candidates = filter(
                            lambda x: (i - x[0]) * direction > 0,
                            prev_pos_candidates)
                elif '左' in matched[3]:
                    if piece in OGOMA:
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


                # cf. http://www.shogi.or.jp/faq/kihuhyouki.html
                # "竜が2枚の場合はやはり動作を優先します。
                #  ただし、「直」は使わずに「左」「右」で記入します。"
                if (piece in OGOMA and 
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

                    print(self.board)
                    print(move_ki2)
                    raise RuntimeError('Parse Error')

                prev_pos = prev_pos_candidates[0]
        else:
            raise RuntimeError('Cannot find prev position.')


        if prev_pos and len(prev_pos) == 2:
            move_csa = ''.join([
                code,
                str(prev_pos[0] + 1),
                str(prev_pos[1] + 1),
                str(i + 1),
                str(j + 1),
                piece
            ])
        
            return move_csa

        else:
            print('Error: prev_pos is invalid, prev_pos=', prev_pos)
            return None
