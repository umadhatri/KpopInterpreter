import ply
import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'ID', 'NUMBER', 'STRING', 'BOOLEAN', 'OP', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
    'ANNYEONG', 'IDOL', 'KPOP', 'FIGHTING', 'SARANGHAE', 'DAEBAK', 'DANCE', 'COMEBACK',
    'SHINEE', 'GG', 'IKON', 'BTS', 'BP', 'TWICE', 'RV', 'EXO', 'BB', 'JYP', 'SJ', 'SKZ',
    'RECORD', 'PLAYBACK'
)

# Regular expression rules for simple tokens
t_OP       = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_SHINEE   = r'shinee'
t_GG       = r'gg'
t_IKON     = r'ikon'
t_BTS      = r'bts'
t_BP       = r'bp'
t_TWICE    = r'twice'
t_RV       = r'rv'
t_EXO      = r'exo'
t_DAEBAK   = r'daebak'
t_DANCE    = r'dance'
t_COMEBACK = r'comeback'
t_ANNYEONG = r'annyeong'
t_IDOL     = r'idol'
t_KPOP     = r'kpop'
t_FIGHTING = r'fighting'
t_SARANGHAE = r'saranghae'
t_BB      = r'bb'
t_JYP     = r'jyp'
t_SKZ     = r'skz'
t_SJ      = r'sj'

# Define a rule for ID and reserved words
reserved = {
    'annyeong': 'ANNYEONG',
    'idol': 'IDOL',
    'kpop': 'KPOP',
    'fighting': 'FIGHTING',
    'saranghae': 'SARANGHAE',
    'daebak': 'DAEBAK',
    'dance': 'DANCE',
    'comeback': 'COMEBACK',
    'exo': 'EXO',
    'shinee': 'SHINEE',
    'gg': 'GG',
    'ikon': 'IKON',
    'bts': 'BTS',
    'bp': 'BP',
    'twice': 'TWICE',
    'rv': 'RV',
    'sj': 'SJ',
    'bb': 'BB',
    'jyp': 'JYP',
    'skz': 'SKZ',
    'record' : 'RECORD',
    'playback' : 'PLAYBACK'
}

# Define a rule for booleans
def t_BOOLEAN(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

# Define a rule for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule for strings
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value.strip('\"')
    return t

# Define a rule for new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string for record and playback
t_RECORD = r'record'
t_PLAYBACK = r'playback'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"LexerError: Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

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
        saranghae("x is greater than 5") kpop
      } daebak {
        saranghae("x is less than 5") kpop
      }
      idol name = gg "" kpop
      saranghae("What's your name? ") kpop
      record(name) kpop
      playback("Hello, ") kpop
      playback(name) kpop
      playback("! Welcome to K-pop Programming!\\n") kpop
    }
    '''

    # Test the lexer
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)