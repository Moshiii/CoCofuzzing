import fuzzutil.util as util
import fuzzutil.mutate as mutate
import javalang
import json
import random
import os

def mutate_by_option(opt, data):

    # data = util.format_code(data)
    try:
        if opt == 'a':
            data = mutate.dead_store(data)
        if opt == 'b':
            data = mutate.apply_redundent_math(data)
        elif opt == 'c':
            data = mutate.apply_plus_zero_math(data)
        elif opt == 'd':
            data = mutate.duplication(data)
        elif opt == 'e':
            data = mutate.dead_branch_if_else(data)
        elif opt == 'f':
            data = mutate.dead_branch_while(data)
        elif opt == 'g':
            data = mutate.dead_branch_if(data)
        elif opt == 'h':
            data = mutate.dead_branch_for(data)
        elif opt == 'i':
            data = mutate.dead_branch_switch(data)
        elif opt == 'j':
            data = mutate.replace_name(data)
    except:
        return ""
    # util.verify_method_syntax(data)
    return data
