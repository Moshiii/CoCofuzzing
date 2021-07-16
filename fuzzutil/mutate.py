import sys 
sys.path.append("..") 
import fuzzutil.util as util
import random

reserved_kws = ["abstract", "assert", "boolean",
                "break", "byte", "case", "catch", "char", "class", "const",
                "continue", "default", "do", "double", "else", "extends", "false",
                "final", "finally", "float", "for", "goto", "if", "implements",
                "import", "instanceof", "int", "interface", "long", "native",
                "new", "null", "package", "private", "protected", "public",
                "return", "short", "static", "strictfp", "super", "switch",
                "synchronized", "this", "throw", "throws", "transient", "true",
                "try", "void", "volatile", "while"]

reserved_cls = ["ArrayDeque", "ArrayList", "Arrays", "BitSet", "Calendar", "Collections", "Currency",
                "Date", "Dictionary", "EnumMap", "EnumSet", "Formatter", "GregorianCalendar", "HashMap",
                "HashSet", "Hashtable", "IdentityHashMap", "LinkedHashMap", "LinkedHashSet",
                "LinkedList", "ListResourceBundle", "Locale", "Observable",
                "PriorityQueue", "Properties", "PropertyPermission",
                "PropertyResourceBundle", "Random", "ResourceBundle", "ResourceBundle.Control",
                "Scanner", "ServiceLoader", "SimpleTimeZone", "Stack",
                "StringTokenizer", "Timer", "TimerTask", "TimeZone",
                "TreeMap", "TreeSet", "UUID", "Vector", "WeakHashMap"
                ]

reserved_kws = reserved_kws + reserved_cls


def replace_name(data):
    tree = util.get_tree(data)
    var_list = util.get_local_vars(tree)
    var_list = [var for var, var_type in var_list if var_type in (
        "int", "float", "double", "long", "byte", "short", "boolean", "char", "String")]
    for t in var_list:
        if t in reserved_kws:
            continue
        var = util.get_radom_var_name()
        # print(var)
        data = data.replace(t, var)
    return data


def replace_type(data):
    tree = util.get_tree(data)
    types = util.get_all_type(tree)
    # print(types)
    for t in types:
        if t in reserved_kws:
            continue
        var = util.get_radom_var_name()
        # print(var)
        data = data.replace(t, var)
    return data


def apply_redundent_math(data):
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    tree = util.get_tree(data)
    var_list = util.get_local_vars(tree)
    var_list = [var for var, var_type in var_list if var_type in (
        "int", "float", "double", "long")]
    if var_list==[]:
        return ""
    for var in var_list:
        redundent_term = str(util.get_random_int(-100, 100))
        mutant = str(var) + ' = ' + str(var) + ' + ' + str(redundent_term) + \
                 ";" + str(var) + ' = ' + str(var) + ' - ' + str(redundent_term) + ";"
        insertion_index = 0

        for idx, statement in enumerate(statements):
            if var in statement and idx < len(statements) - 1:
                insertion_index = idx + 1
        statements.insert(idx + 1, mutant)
    data = header + ''.join(statements) + "}"
    return data


def apply_plus_zero_math(data):
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    tree = util.get_tree(data)
    var_list = util.get_local_vars(tree)
    var_list = [var for var, var_type in var_list if var_type in (
        "int", "float", "double", "long")]
    if var_list==[]:
        return ""
    for var in var_list:
        mutant = str(var) + ' = ' + str(var) + ' + ' + str(0) + ";"
        insertion_index = 0

        for idx, statement in enumerate(statements):
            if var in statement and idx < len(statements) - 1:
                insertion_index = idx + 1
        statements.insert(idx + 1, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_store(data):
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    var_name = util.get_radom_var_name()
    mutant = util.get_random_type_name_and_value_statment()
    statements.insert(util.get_random_int(0, len(statements)), mutant)
    data = header + ''.join(statements) + "}"
    return data

def format(data):
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    data = header + ''.join(statements) + "}"
    return data


def duplication(data):
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    assign_statements = []
    for idx, s in enumerate(statements):
        if "for(" in s or "while(" in s or "if(" in s or "return" in s:
            continue
        if not "=" in s:
            continue
        else:
            if "VariableDeclarator" in str(util.get_tree(s)):
                s = " ".join(s.split(" ")[1:])
                if s[:2] == "[]":
                    s = s[2:]
                if "<" in s and ">" in s:
                    continue
            assign_statements.append([idx, s])
    rand_idx = util.get_random_int(0, len(assign_statements)-1)
    position = assign_statements[rand_idx][0]
    mutant = assign_statements[rand_idx][1]
    statements.insert(position+1, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_branch_if_else(data):
    rand_idx = 0
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)

    mutant = util.get_branch_if_else_mutant()

    statements.insert(rand_idx, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_branch_if(data):
    rand_idx = 0
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)

    mutant = util.get_branch_if_mutant()

    statements.insert(rand_idx, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_branch_while(data):
    rand_idx = 0
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)

    mutant = util.get_branch_while_mutant()

    statements.insert(rand_idx, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_branch_for(data):
    rand_idx = 0
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)

    mutant = util.get_branch_for_mutant()

    statements.insert(rand_idx, mutant)
    data = header + ''.join(statements) + "}"
    return data


def dead_branch_switch(data):
    rand_idx = 0
    header = util.get_method_header(data)
    statements = util.get_method_statement(data)
    var_name = util.get_radom_var_name()

    mutant = util.get_branch_switch_mutant()
    statements.insert(rand_idx, mutant)
    data = header + ''.join(statements) + "}"
    return data

