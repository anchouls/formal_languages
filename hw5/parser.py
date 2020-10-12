import ply.yacc as yacc

from lex import tokens


def p_continue(p):
    '''continue : fact
                | fact continue '''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]


def p_fact(p):
    '''fact : atom SPIN expression DOT
            | atom DOT '''
    if len(p) == 3:
        p[0] = '(HEAD ' + p[1] + ') (DOT)'
    else:
        p[0] = '(HEAD '+p[1] + ') (SPIN) (BODY ' + p[3] + ') (DOT)'


def p_expression_disj(p):
    'expression : term DISJ expression'
    p[0] = '(DISJ ' + p[1] + ' ' + p[3] + ')'


def p_term_conj(p):
    'term : factor CONJ term'
    p[0] = '(CONJ ' + p[1] + ' ' + p[3] + ')'


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor(p):
    '''factor : atom
              | LBR expression RBR '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_atom(p):
    '''atom : ID
            | ID ids '''
    p[0] = '(ATOM (ID ' + p[1] + ')'
    if len(p) == 3:
        p[0] += p[2]
    p[0] += ')'


def p_ids(p):
    '''ids : atom
           | LBR ids RBR
           | ids ids '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + ' ' + p[2]
    else:
        p[0] = ''.join(p[1:])


def p_error(p):
    print('Syntax error')
    exit(0)


parser = yacc.yacc()




