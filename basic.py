"""
Building a better WAMIT user experience.

Notice this file is intended for teaching purpose hence the overly verbose comments.
Comments directed to individuals are marked with TO:XX for better readability.

Author(s): Jeff, Po-Yi
"""

"""TO:Po-Yi
Welcome to the world of Python and what I'd refer to scientific programming.

During your time as a researcher, you will be facing similar task of text
handling / data extraction / visualization / statistic summary and so on. Using
Python as your programming tool is suitable for multiple reasons: its faster
and light weight plus its also widely used in industry. Notice that you should
always try to question my code, don't be shy on asking / raising questions when
you read anyone's code, especially mine. In Python, and much the same in many
other programming paradigms, there are many ways of doing things right.

"""

"""
pip install lark parse
"""

import logging, sys
import numpy as np

from lark import Lark
from lark.indenter import Indenter
from io import StringIO


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.info('Library import complete')


""" TODO This grammar now fixed on one initial simple_table followed by
complex_table+, not the most accomodating grammar for our case but will do for now.
"""
numeric_grammar = r"""
    ?start: preamble [wave+]

    preamble: (STR | _DIVIDER)*
    wave: _ASTERISK_L wave_info _DIVIDER [simple_table (complex_table)+]
    wave_info: "Wave period (sec) = " NUM "Wavenumber (kL) = " NUM

    table: complex_table

    simple_table: TABLE_TITLE _NL [index row+]
    complex_table: TABLE_TITLE _NL additional_info _NL [index row+]


    index: [COLNAME+] _NL
    row: [NUM+] _NL
    additional_info: STR

    %import common.SIGNED_NUMBER -> NUM
    %import common.WS
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.UCASE_LETTER
    %import common.LETTER
    %import common.DIGIT

    %ignore WS
    TABLE_TITLE: (UCASE_LETTER) STR
    COLNAME: ("_"|LETTER) ("_"| LETTER | DIGIT | "[" | "]" | "(" | ")" | "," | "&")*
    STR: /.+/
    _NL: /(\r?\n[\t ]*)+/ | NEWLINE

    _ASTERISK_L: ("*")("*")+
    _DIVIDER: ("-")("-")+
"""

numeric_parser = Lark(numeric_grammar, parser='lalr')
input_file = open("./wamit_exampleOutput.out", "r")
data = input_file.read()
print(numeric_parser.parse(data).pretty())
