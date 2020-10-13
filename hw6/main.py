from pyparsing import *

import sys


def _temp1(p):
    res = ''
    for i in p:
        if isinstance(i, list):
            res += "(TYPE " + _temp1(i) + ")"
        else:
            res += i + " "
    return res.strip()


def print_list(t):
    if len(t) == 0:
        return "(cons nil nil)"
    elif len(t) == 1:
        return "(cons {} nil)".format(t[0])
    else:
        return "(cons {} {})".format(t[0], t[1])


def print_res(dk: dict):
    dk = dk[0]
    for key, item in dk.items():
        if key != "module":
            print(str(key) + ":")
            for i in item:
                print(str(i))
        else:
            print(str(key) + ": " + str(item))


def syntax():
    no_var = (NotAny("type") + NotAny("module") + Regex("[a-z_][A-Za-z_0-9]*")).setParseAction(lambda t: "(ID {})".format(t[0]))
    var = NotAny("type") + NotAny("module") + Regex("[A-Z][A-Za-z_0-9]*").setParseAction(lambda t: "(ID {})".format(t[0]))
    id = no_var | var
    lbr = Suppress('(')
    rbr = Suppress(')')
    dot = Suppress('.')
    atom = Forward()
    wrapper = Forward()
    lst = Forward()
    atom_complex = (id | lst | wrapper).setParseAction(lambda t: t)
    wrapper <<= lbr + atom + rbr | lbr + atom_complex + rbr
    atom <<= (no_var + ZeroOrMore(atom_complex)).\
        setParseAction(lambda t: "(ATOM " + ' '.join(t.asList()) + ")")
    disj = Forward()
    conj = Forward()
    factor = lbr + disj + rbr | atom
    conj << (factor + Optional(',' + conj)).setParseAction(lambda t: t[0] if len(t) == 1 else "(CONJ " + str(t[0]) + str(t[2]) + ")")
    disj << (conj + Optional(';' + disj)).setParseAction(lambda t: t[0] if len(t) == 1 else "(DISJ " + str(t[0]) + str(t[2]) + ")")
    expression = (atom + Optional(Suppress(':-') + disj) + dot).\
        setParseAction(lambda t: "(HEAD " + t[0] + ")" + ("" if len(t) == 1 else " (BODY " + t.asList()[1] + ")"))
    exp_loop = ZeroOrMore(expression)("expression")
    alv = atom | lst | var
    list_ins = Forward()
    list_ins <<= (Suppress(',') + alv + Optional(list_ins)).\
        setParseAction(lambda t: "(cons " + t[0] + " " + (t[1] if len(t) == 2 else 'nil') + ') ')
    lst <<= ((Suppress('[') + Optional(alv + Optional(list_ins)) + Suppress(']')) |
             (Suppress('[') + alv + Suppress('|') + var + Suppress(']')))("list"). \
        setParseAction(lambda t:  print_list(t))
    type_ = Forward()
    type_ <<= Group((atom | id | lbr + type_ + rbr) + ZeroOrMore('->' + (atom | id | lbr + type_ + rbr)))
    types = (Suppress(Keyword("type")) + id + type_ + dot). \
        setParseAction(lambda t: '(NAME '+ t[0] + ') (TYPE ' + _temp1(t[1].asList()) + ")")
    type_loop = ZeroOrMore(types)("types")
    module = (Suppress(Keyword("module")) + no_var + dot)("module")
    program = (Optional(module) + type_loop + exp_loop + stringEnd()). \
        setParseAction(lambda t: {"module": '' if isinstance(t.module, str) else t.module[0],
                                  "types": '' if isinstance(t.types, str) else t.types,
                                  "expression": t.expression})
    return program


if __name__ == "__main__":
    a = dict()
    if len(sys.argv) != 2:
        print("Передайте в аргументы название файла с прологом")
    else:
        file_name = sys.argv[1]
        with open(file_name, "r") as reader:
            data = reader.read()
            expr = syntax()
            try:
                result = expr.parseString(data)
                print_res(result)
            except ParseException as e:
                print("Error")
                print(e)

