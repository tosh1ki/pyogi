#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def get_ki2_list(parser):

    parser.add_argument('-p', '--path_2chkifu',
                        default='~/data/shogi/2chkifu/',
                        help='2chkifu.zipを展開したディレクトリ')
    args = parser.parse_args()
    path_2chkifu = args.path_2chkifu

    sub_dir_list = ['00001', '10000', '20000', '30000', '40000']
    path_ki2_list = []

    # Extract paths of KI2 files
    for sub_dir in sub_dir_list:
        path_dir = os.path.expanduser(os.path.join(path_2chkifu, sub_dir))
        ki2files = os.listdir(path_dir)

        for ki2file in ki2files:
            path_ki2_list.append(os.path.join(path_dir, ki2file))

    return path_ki2_list
