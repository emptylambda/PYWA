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
    ?start: [simple_table (complex_table)+]

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
    TABLE_TITLE: (UCASE_LETTER) (UCASE_LETTER | WS_INLINE | "-")*
    COLNAME: ("_"|LETTER) ("_"| LETTER | DIGIT | "[" | "]" | "(" | ")" | ",")*
    STR: /.+/
    _NL: /(\r?\n[\t ]*)+/ | NEWLINE
"""

numeric_parser = Lark(numeric_grammar, parser='lalr')
test_num = """

    ADDED-MASS AND DAMPING COEFFICIENTS
     I     J         A(I,J)         B(I,J)

     1     1   7.162926E-01   4.911184E-03
     1     5  -3.398149E-02   6.431871E-04
     2     2   7.162927E-01   4.911192E-03
     2     4   3.398167E-02  -6.431872E-04
     3     3   2.368622E+00   5.115258E-01
     4     2   3.299096E-02  -6.325951E-04
     4     4   2.207076E-01   8.284464E-05
     5     1  -3.299065E-02   6.325978E-04
     5     5   2.207078E-01   8.284810E-05
     6     6   7.920762E-14   1.727917E-19




    HASKIND EXCITING FORCES AND MOMENTS

  Wave Heading (deg) :      0

     I     Mod[Xh(I)]     Pha[Xh(I)]

     1   3.487235E-01             90
     2   0.000000E+00             90
     3   2.520755E+00              2
     4   0.000000E+00             90
     5   4.567020E-02             90
     6   0.000000E+00             90




    DIFFRACTION EXCITING FORCES AND MOMENTS

  Wave Heading (deg) :      0

     I     Mod[Xh(I)]     Pha[Xh(I)]

     1   3.498376E-01             90
     2   0.000000E+00             90
     3   2.520390E+00              2
     4   0.000000E+00             90
     5   4.506154E-02             90
     6   0.000000E+00             90




    RESPONSE AMPLITUDE OPERATORS

  Wave Heading (deg) :      0

     I    Mod[RAO(I)]    Pha[RAO(I)]

     1    9.40403E-01            -90
     2    0.00000E+00             90
     3    1.00671E+00              0
     4    0.00000E+00             90
     5    5.06202E-01             90
     6    0.00000E+00             90

"""
