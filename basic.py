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
    ?start: [wave+]

    preamble: STR
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
test_num = """
 ************************************************************************

 Wave period (sec) =  5.000000E+00        Wavenumber (kL) =  1.610271E-01
 ------------------------------------------------------------------------

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
big_test_num = """
 
 ************************************************************************

 Wave period (sec) =  5.000000E+00        Wavenumber (kL) =  1.610271E-01
 ------------------------------------------------------------------------


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




 HYDRODYNAMIC PRESSURE IN FLUID DOMAIN

  Wave Heading (deg) :      0

       x           y           z         Mod[Pf(x,y,z)]  Pha[Pf(x,y,z)]

    1.50E+00    0.00E+00    0.00E+00        9.97320E-01             -14
    1.50E+00    0.00E+00   -5.00E-01        9.21303E-01             -14




 VELOCITY VECTOR IN FLUID DOMAIN

  Wave Heading (deg) :      0

     x         y         z         Mod(Vx)  Pha    Mod(Vy)  Pha    Mod(Vz)  Pha

  1.50E+00  0.00E+00  0.00E+00   1.615E-01 -102  3.418E-10   -2  1.606E-01  -14
  1.50E+00  0.00E+00 -5.00E-01   1.478E-01 -103  4.029E-10   -1  1.447E-01  -13




 SURGE, SWAY & YAW DRIFT FORCES (Momentum Conservation)

  Wave Heading (deg) :      0         0

     I      Mod[F(I)]    Pha[F(I)]

     1    7.44534E-07          180
     2    0.00000E+00           90
     6    0.00000E+00           90




 SURGE, SWAY, HEAVE, ROLL, PITCH & YAW DRIFT FORCES (Pressure Integration)

  Wave Heading (deg) :      0         0

     I      Mod[F(I)]    Pha[F(I)]      Mod[F(I)]    Pha[F(I)]

     1    1.08822E-05            0
     2    8.05918E-08         -180
     3    2.39719E-01            0
     4    1.05340E-07            0    1.20517E-08            0
     5    3.41717E-06          180    1.33919E-06            0
     6    3.52224E-10          180    6.11750E-10          180


 ************************************************************************

 Wave period (sec) =  3.700000E+00        Wavenumber (kL) =  2.940598E-01
 ------------------------------------------------------------------------


    ADDED-MASS AND DAMPING COEFFICIENTS
     I     J         A(I,J)         B(I,J)

     1     1   7.813995E-01   2.845588E-02
     1     5  -3.245812E-02   3.141996E-03
     2     2   7.813997E-01   2.845593E-02
     2     4   3.245835E-02  -3.141998E-03
     3     3   2.145597E+00   6.548616E-01
     4     2   3.158745E-02  -3.080902E-03
     4     4   2.208701E-01   3.401789E-04
     5     1  -3.158716E-02   3.080927E-03
     5     5   2.208701E-01   3.401880E-04
     6     6   7.962724E-14   3.310131E-18




    HASKIND EXCITING FORCES AND MOMENTS

  Wave Heading (deg) :      0

     I     Mod[Xh(I)]     Pha[Xh(I)]

     1   6.211544E-01             89
     2   0.000000E+00             90
     3   2.110719E+00              5
     4   0.000000E+00             90
     5   6.858572E-02             89
     6   0.000000E+00             90




    DIFFRACTION EXCITING FORCES AND MOMENTS

  Wave Heading (deg) :      0

     I     Mod[Xh(I)]     Pha[Xh(I)]

     1   6.231561E-01             89
     2   0.000000E+00             90
     3   2.110149E+00              5
     4   0.000000E+00             90
     5   6.746944E-02             89
     6   0.000000E+00             90




    RESPONSE AMPLITUDE OPERATORS

  Wave Heading (deg) :      0

     I    Mod[RAO(I)]    Pha[RAO(I)]

     1    9.06628E-01            -90
     2    0.00000E+00             90
     3    1.02787E+00              0
     4    0.00000E+00             90
     5    5.58180E-01            -90
     6    0.00000E+00             90




 HYDRODYNAMIC PRESSURE IN FLUID DOMAIN

  Wave Heading (deg) :      0

       x           y           z         Mod[Pf(x,y,z)]  Pha[Pf(x,y,z)]

    1.50E+00    0.00E+00    0.00E+00        9.90278E-01             -25
    1.50E+00    0.00E+00   -5.00E-01        8.57017E-01             -25




 VELOCITY VECTOR IN FLUID DOMAIN

  Wave Heading (deg) :      0

     x         y         z         Mod(Vx)  Pha    Mod(Vy)  Pha    Mod(Vz)  Pha

  1.50E+00  0.00E+00  0.00E+00   2.849E-01 -112  3.125E-10   38  2.913E-01  -25
  1.50E+00  0.00E+00 -5.00E-01   2.582E-01 -113  3.195E-10  -77  2.447E-01  -27




 SURGE, SWAY & YAW DRIFT FORCES (Momentum Conservation)

  Wave Heading (deg) :      0         0

     I      Mod[F(I)]    Pha[F(I)]

     1    4.10795E-05            0
     2    0.00000E+00           90
     6    0.00000E+00           90




 SURGE, SWAY, HEAVE, ROLL, PITCH & YAW DRIFT FORCES (Pressure Integration)

  Wave Heading (deg) :      0         0

     I      Mod[F(I)]    Pha[F(I)]      Mod[F(I)]    Pha[F(I)]

     1    1.26523E-04         -180
     2    2.55890E-08            0
     3    4.20329E-01            0
     4    9.40293E-08            0    8.58955E-08            0
     5    9.46610E-05            0    1.07883E-04            0
     6    2.80758E-09            0    1.24359E-10            0

"""
