import ply.yacc as yacc
from lexer import tokens, lexer

precedence = (
    ('left', 'BTS', 'BP'),
    ('left', 'TWICE', 'RV'),
    ('left', 'IKON'), 
    ('left', 'BB', 'JYP', 'SJ', 'SKZ')
)

def p_program(p):
    '''program : ANNYEONG ID LPAREN RPAREN block'''
    p[0] = ('program', p[2], p[5])

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = p[2]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment
                 | fighting
                 | dance
                 | comeback
                 | saranghae'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : IDOL ID OP expression KPOP'''
    p[0] = ('assign', p[2], p[4])

def p_fighting(p):
    '''fighting : FIGHTING LPAREN expression RPAREN block
                | FIGHTING LPAREN expression RPAREN block DAEBAK block'''
    if len(p) == 6:
        p[0] = ('fighting', p[3], p[5], None)
    else:
        p[0] = ('fighting', p[3], p[5], p[7])

def p_dance(p):
    '''dance : DANCE LPAREN expression RPAREN block'''
    p[0] = ('dance', p[3], p[5])

def p_comeback(p):
    '''comeback : COMEBACK LPAREN assignment expression KPOP expression RPAREN block'''
    p[0] = ('comeback', p[3], p[4], p[6], p[8])

def p_saranghae(p):
    '''saranghae : SARANGHAE LPAREN expression RPAREN KPOP'''
    p[0] = ('saranghae', p[3])

def p_expression(p):
    '''expression : ID
                  | NUMBER
                  | STRING
                  | BOOLEAN
                  | SHINEE NUMBER
                  | GG STRING
                  | EXO BOOLEAN
                  | expression IKON expression
                  | expression BTS expression
                  | expression BP expression
                  | expression TWICE expression
                  | expression RV expression
                  | expression SJ expression
                  | expression BB expression
                  | expression JYP expression
                  | expression SKZ expression'''
    if len(p) == 2:
        if p.slice[1].type == 'BOOLEAN':
            p[0] = ('boolean', p[1])
        elif p.slice[1].type == 'NUMBER':
            p[0] = ('number', p[1])
        elif p.slice[1].type == 'STRING':
            p[0] = ('string', p[1])
        else:
            p[0] = ('id', p[1])
    elif len(p) == 3:
        if p[1] == 'shinee':
            p[0] = ('number', p[2])
        elif p[1] == 'gg':
            p[0] = ('string', p[2])
        elif p[1] == 'exo':
            p[0] = ('boolean', p[2])
    elif len(p) == 4:
        p[0] = (p[2], p[1], p[3])

def p_error(p):
    if p:
        print(f"SyntaxError: Unexpected token '{p.value}' of type {p.type} at line {p.lineno}, position {p.lexpos}")
    else:
        print("SyntaxError: Unexpected end of input")

parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    data = '''
    annyeong main() {
      idol x = shinee 10 kpop
      idol y = gg "Hello, K-pop!" kpop
      idol z = exo true kpop
      fighting(x ikon shinee 5) {
        saranghae(x bts 10) kpop
      } daebak {
        saranghae(y) kpop
      }
      dance(x bp shinee 0) {
        saranghae(x bts 20) kpop
        idol x = x bp shinee 1 kpop
      }
      comeback(idol i = shinee 0 kpop i bp shinee 5 kpop i bts shinee 1) {
        saranghae(i) kpop
      }
      fighting(x bb shinee 5) {
        saranghae(x bts shinee 10) kpop
      } daebak {
        saranghae(x) kpop
      }
    }
    '''
    result = parser.parse(data, lexer=lexer)
    print(result)
