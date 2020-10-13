import ply.lex as lex

tokens = [
  'SPIN',
  'DOT',
  'CONJ',
  'DISJ',
  'ID',
  'LBR',
  'RBR'
]


t_SPIN = r'\:-'
t_DOT = r'\.'
t_CONJ = r'\,'
t_DISJ = r'\;'
t_ID = r'[A-Za-z_][A-Za-z_0-9]*'
t_LBR = r'\('
t_RBR = r'\)'


t_ignore = ' \t'


def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  exit(0)


lexer = lex.lex()
