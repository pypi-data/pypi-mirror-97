# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

from aostools import *
from aostools.tools import get_elf_bin_file
import os
import shutil

class Burn(Command):
    common = True
    helpSummary = "Burn elf or binary file into Flash"
    helpUsage = """
%prog 
"""
    helpDescription = """
Burn elf or binary file into Flash
"""
    def _Options(self, p):
        p.add_option('-b', '--board',
                     dest='board_name', action='store', type='str', default=None,
                     help='get burn tools from selected board')

    def Execute(self, opt, args):
        yoc = YoC()
        solution = yoc.getSolution(opt.board_name)
        if solution == None:
            put_string("The current directory is not a solution!")
            exit(0)
        if not solution.flash_program or not os.path.isfile(solution.flash_program):
            put_string("Can not find flash program tool for this solution(or board or chip)!")
            exit(0)
        self.burn_script(solution.flash_program)
        
    def burn_script(self, script_file):
        cmdstr = script_file
        elf_file, bin_file = get_elf_bin_file('SConstruct')
        if elf_file:
            cmdstr += " --elf=%s" % os.path.abspath(elf_file)
        if bin_file:
            cmdstr += " --bin=%s" % os.path.abspath(bin_file)
        os.system(cmdstr)

