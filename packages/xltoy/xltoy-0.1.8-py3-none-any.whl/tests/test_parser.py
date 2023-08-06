import pytest
from xltoy.parser import Parser
from xltoy.utils import split_sheet_coordinates

p = Parser(collector=None)

test_set = """
=3*A7+5
=+3
=3*Sheet1!$A$7+5
=3*'Sheet 1'!$A$7+5
=3*'O''Reilly''s sheet'!$A$7+5
=if(Sum(A1:A25)>42,Min(B1:B25),if(Sum(C1:C25)>3.14, (Min(C1:C25)+3)*18,Max(B1:B25)))
=sum(a1:a25,10,min(b1,c2,d3))
=if("T"&a2="TTime", "Ready", "Not ready")
=E3
=+8
=E4+Y6+AA3
=(E3+D3)/2
=+LOG(F11)
=(E4+D4)/2
=IF(D7,D7+E7,D7-E7)
=1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543))
=+IF(A4+B4, 1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543)), IF(A4+B4, 1, PRIVFUN(E4)))
=+IF(PARAM!$B$135=0, 1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543)), IF(PARAM!$B$135=1,PRIVFUN(FUNCT(INPUT_M!$G$62)+E$543),PRIVFUN((FUNCT(INPUT_M!$G$62)+SQRT(INPUT_M!$G$45)*E$543)/SQRT(1-INPUT_MATRIX!$G$45))))
=K13-MIN(L$10,0)+IF(SHEE1!M20=1,0,MIN(K10,0))+L15+L16
=+INTERBANK!FS221
=IF(J60=1,1,IF(RAND()<K59,1*K40,0))
=(+INTB!I268*INTB!H279+INTB!I269*INTB!H280)/(INTB!H279+INTB!H280)
=(+A2)
=+(((+5)))
=+(1-PAR!$B$109)*BLEND!I20+PAR!$B$109*BLEND!I23
=NEWRNGFUNCT(SHEET1!G42:G44,SHEET1!$X$42:$X$44)
=NEWCELLFUNCT(SHEET1!G42, SHEET2!G43)
=E12+IF(SCENARIO_MACRO!M20=1,E28,0)-(F46-F49)+RECOVERY_OPT!E78+IF(AND(F48>0,F47>F48),F48-F47,0)
=IF(AND(F48>0,F47>F48),F48-F47,0)
=PARAMETRI!$B$101*PARAMETRI!$B$102+RECOVERY_OPT!E60+MA!G59^MA!$X$59
=+(H230*PARAMETRI!$B$205+H231*PARAMETRI!$B$206+H232*PARAMETRI!$B$207+H233*PARAMETRI!$B$208+H234*PARAMETRI!$B$209+H235*PARAMETRI!$B$210+H236*PARAMETRI!$B$211)/+(G230*PARAMETRI!$B$205+G231*PARAMETRI!$B$206+G232*PARAMETRI!$B$207+G233*PARAMETRI!$B$208+G234*PARAMETRI!$B$209+G235*PARAMETRI!$B$210+G236*PARAMETRI!$B$211)-1
=E73*F83*(1-PARAMETRI!$B$64)*Time_step
""".splitlines()

@pytest.mark.parser
@pytest.mark.parametrize("s", filter(None,test_set))
def test_parser(s):
    assert p.parse(s)


@pytest.mark.parser
def test_split_sheet_coordinates():
    """maybe useless"""
    assert split_sheet_coordinates('E4')          == (None, 'E4')
    assert split_sheet_coordinates('MYSH!E4')     == ('MYSH','E4')
    assert split_sheet_coordinates("'M Y SH'!E4") == ('M Y SH', 'E4')

@pytest.mark.parser
def test_parser_cell_name():
    s = '=A1'
    parsed = p.parse(s)
    assert parsed.cell.pos == 'A1'

@pytest.mark.parser
def test_parser_cell_sheet():
    s = '=SHEET!$A$11'
    parsed = p.parse(s)
    assert parsed.cell.pos == '$A$11'
    assert parsed.cell.sheet == 'SHEET'

@pytest.mark.parser
def test_parser_cell_rng():
    s = '=SHEET!$A$11:$A$21'
    parsed = p.parse(s)
    assert parsed.range.start.sheet == 'SHEET'
    assert parsed.range.end.sheet == ''
    assert parsed.range.start.pos == '$A$11'
    assert parsed.range.end.pos == '$A$21'
