from ply import lex, yacc

states = (
   ('string','exclusive'),
)

tokens = (
    'FUN', 'END', 'IF', 'CASE', 'OF', 'FOR',
    'NAME', 'STRING', 'NUMBER',
    'LARR', 'RARR',
    'LE', 'GE')

precedence = (
    ('right', '='),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'))

t_NUMBER = r'[0-9]+'

t_LARR = r'<-'
t_RARR = r'->'

t_LE = r'=<'
t_GE = r'>='

t_ignore = ' \t'
t_ignore_comment = r'--[^\n]*(?=\n|$)'

literals = [':', ',', ';', '.', '{', '}', '[', ']', '(', ')', '<', '>', '=', '#', '+', '-', '*', '/']
reserved = ['fun', 'end', 'if', 'case', 'of', 'for']


def t_ignore_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NAME(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value.upper()
    return t

def t_quote(t):
    r"\""
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.push_state('string')

def t_string_char(t):
    r"[^\n\\\"]+"

def t_string_backslash(t):
    r"\\[a-z]"

def t_string_quote(t):
    r"\""
    t.lexer.pop_state()
    t.value = t.lexer.lexdata[t.lexer.string_start:t.lexer.lexpos-1]
    t.type = "STRING"
    return t



def p_exp(p):
    """exp : number
           | string
           | tuple
           | atom
           | dict
           | list
           | prefix
           | fun
           | case
           | object
           | listcomp"""
    p[0] = p[1]


def p_listcomp(p):
    """listcomp : '[' exp FOR exp LARR exp ']'"""
    p[0] = ('listcomp', p[2], p[4], p[6])


def p_listcomp_guard(p):
    """listcomp : '[' exp FOR exp LARR exp IF exp ']'"""
    p[0] = ('listcomp', p[2], p[4], p[6], p[8])


def p_slices(p):
    """slices : slices ',' slice"""
    p[0] = p[1] + [p[3]]


def p_slices_single(p):
    """slices : slice"""
    p[0] = [p[1]]


def p_slice(p):
    """slice : exp"""
    p[0] = ('slice', (p[1],))


def p_slice2(p):
    """slice : exp ':' exp"""
    p[0] = ('slice', (p[1], p[3]))


def p_slice3(p):
    """slice : exp ':' exp ':' exp"""
    p[0] = ('slice', (p[1], p[3], p[5]))


def p_object(p):
    """object : prefix '{' slots '}'
              | prefix '{' emptylist '}'"""
    p[0] = ('object', p[1], p[3])


def p_slots(p):
    """slots : slots ',' slot"""
    p[0] = p[1] + [p[3]]


def p_slots_single(p):
    """slots : slot"""
    p[0] = [p[1]]


def p_slot_attribute(p):
    """slot : '.' name '=' exp"""
    p[0] = ('attribute', p[2], p[4])


def p_slot_subscript(p):
    """slot : '[' slices ']' '=' exp"""
    p[0] = ('subscript', p[2], p[5])


def p_clause(p):
    """clause : '(' explist ')' RARR explist
              | '(' emptylist ')' RARR explist"""
    p[0] = ('clause', p[2], [], p[5])


def p_clause_guard(p):
    """clause : '(' explist ')' IF explist RARR explist
              | '(' emptylist ')' IF explist RARR explist"""
    p[0] = ('clause', p[2], p[5], p[7])


def p_clauses(p):
    """clauses : clauses ';' clause"""
    p[0] = p[1] + [p[3]]


def p_clauses_single(p):
    """clauses : clause"""
    p[0] = [p[1]]


def p_lambda(p):
    """fun : FUN clauses END"""
    p[0] = ('fun', None, p[2])


def p_fun(p):
    """fun : FUN name clauses END"""
    p[0] = ('fun', p[2], p[3])


def p_case_clauses(p):
    """case_clauses : case_clauses ';' case_clause"""
    p[0] = p[1] + [p[3]]


def p_case_clauses_single(p):
    """case_clauses : case_clause"""
    p[0] = [p[1]]


def p_case_clause(p):
    """case_clause : exp RARR explist"""
    p[0] = ('case-clause', p[1], [], p[3])


def p_case_clause_guard(p):
    """case_clause : exp IF explist RARR explist"""
    p[0] = ('case-clause', p[1], p[3], p[5])


def p_case(p):
    """case : CASE exp OF case_clauses END"""
    p[0] = ('case', p[2], p[4])


def p_binop(p):
    """exp : exp '=' exp
           | exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp"""
    p[0] = ('binop', p[2], p[1], p[3])


def p_unop(p):
    """exp : '-' exp %prec UMINUS"""
    p[0] = ('unop', p[1], p[2])


def p_prefix(p):
    """prefix : var
              | call"""
    p[0] = p[1]


def p_prefix_exp(p):
    """prefix : '(' exp ')'"""
    p[0] = p[2]


def p_prefix_attribute(p):
    """prefix : prefix '.' name"""
    p[0] = ('attribute', p[1], p[3])


def p_prefix_subscript(p):
    """prefix : prefix '[' slices ']'"""
    p[0] = ('subscript', p[1], p[3])


def p_call(p):
    """call : prefix '(' explist ')'
            | prefix '(' emptylist ')'"""
    p[0] = ('call', p[1], p[3])


def p_atom(p):
    """atom : ':' NAME"""
    p[0] = ('atom', p[2])


def p_list(p):
    """list : '[' explist ']'
            | '[' emptylist ']'"""
    p[0] = ('list', p[2])


def p_tuple(p):
    """tuple : '{' explist '}'
             | '{' emptylist '}'"""
    p[0] = ('tuple', p[2])


def p_dict(p):
    """dict : '{' fieldlist '}'
            | '{' emptyfieldlist '}'"""
    p[0] = ('dict', p[2])


def p_explist(p):
    """explist : explist ',' exp"""
    p[0] = p[1] + [p[3]]


def p_explist_single(p):
    """explist : exp"""
    p[0] = [p[1]]


def p_emptylist(p):
    """emptylist :  """
    p[0] = []


def p_fieldlist(p):
    """fieldlist : fieldlist ',' field"""
    p[0] = p[1] + [p[3]]


def p_fieldlist_single(p):
    """fieldlist : field"""
    p[0] = [p[1]]


def p_fieldlist_empty(p):
    """emptyfieldlist : ':'"""
    p[0] = []


def p_field(p):
    """field : exp ':' exp"""
    p[0] = ('field', p[1], p[3])


def p_var(p):
    """var : name"""
    p[0] = ('var', p[1])


def p_name(p):
    """name : NAME"""
    p[0] = ('name', p[1])


def p_number(p):
    """number : NUMBER"""
    p[0] = ('number', p[1])


def p_string(p):
    """string : STRING"""
    p[0] = ('string', p[1])


lex.lex()
yacc.yacc(debug=0, write_tables=0)
