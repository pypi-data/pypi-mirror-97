from tkinter import *
import tkinter as tk
import re


def if_h(Text_widget, color):
    Text_widget.tag_remove("tag_ifh", "1.0", END)
    if_first = "1.0"
    while True:
        if_first = Text_widget.search("\yif\y", if_first, nocase=False, stopindex=END, regexp=True)
        if not if_first:
            break
        str_last = if_first + "+" + str(len("if")) + "c"
        Text_widget.tag_add("tag_ifh", if_first, str_last)
        if_first = str_last
    Text_widget.tag_config("tag_ifh", foreground=color)

def else_h(Text_widget, color):
    Text_widget.tag_remove("tag_elseh", "1.0", END)
    else_first = "1.0"
    while True:
        else_first = Text_widget.search("\yelse\y", else_first, nocase=False, stopindex=END, regexp=True)
        if not else_first:
            break
        str_last = else_first + "+" + str(len("else")) + "c"
        Text_widget.tag_add("tag_elseh", else_first, str_last)
        else_first = str_last
    Text_widget.tag_config("tag_elseh", foreground=color)


def elif_h(Text_widget, color):
    Text_widget.tag_remove("tag_elifh", "1.0", END)
    elif_first = "1.0"
    while True:
        elif_first = Text_widget.search("\yelif\y", elif_first, nocase=False, stopindex=END, regexp=True)
        if not elif_first:
            break
        str_last = elif_first + "+" + str(len("elif")) + "c"
        Text_widget.tag_add("tag_elifh", elif_first, str_last)
        elif_first = str_last
    Text_widget.tag_config("tag_elifh", foreground=color)


def try_h(Text_widget, color):
    Text_widget.tag_remove("tag_tryh", "1.0", END)
    try_first = "1.0"
    while True:
        try_first = Text_widget.search("\ytry\y", try_first, nocase=False, stopindex=END, regexp=True)
        if not try_first:
            break
        str_last = try_first + "+" + str(len("try")) + "c"
        Text_widget.tag_add("tag_tryh", try_first, str_last)
        try_first = str_last
    Text_widget.tag_config("tag_tryh", foreground=color)


def except_h(Text_widget, color):
    Text_widget.tag_remove("tag_excepth", "1.0", END)
    except_first = "1.0"
    while True:
        except_first = Text_widget.search("\yexcept\y", except_first, nocase=False, stopindex=END, regexp=True)
        if not except_first:
            break
        str_last = except_first + "+" + str(len("except")) + "c"
        Text_widget.tag_add("tag_excepth", except_first, str_last)
        except_first = str_last
    Text_widget.tag_config("tag_excepth", foreground=color)


def finally_h(Text_widget, color):
    Text_widget.tag_remove("tag_finallyh", "1.0", END)
    finally_first = "1.0"
    while True:
        finally_first = Text_widget.search("\yfinally\y", finally_first, nocase=False, stopindex=END, regexp=True)
        if not finally_first:
            break
        str_last = finally_first + "+" + str(len("finally")) + "c"
        Text_widget.tag_add("tag_finallyh", finally_first, str_last)
        finally_first = str_last
    Text_widget.tag_config("tag_finallyh", foreground=color)


def for_h(Text_widget, color):
    Text_widget.tag_remove("tag_forh", "1.0", END)
    for_first = "1.0"
    while True:
        for_first = Text_widget.search("\yfor\y", for_first, nocase=False, stopindex=END, regexp=True)
        if not for_first:
            break
        str_last = for_first + "+" + str(len("for")) + "c"
        Text_widget.tag_add("tag_forh", for_first, str_last)
        for_first = str_last
    Text_widget.tag_config("tag_forh", foreground=color)


def while_h(Text_widget, color):
    Text_widget.tag_remove("tag_whileh", "1.0", END)
    while_first = "1.0"
    while True:
        while_first = Text_widget.search("\ywhile\y", while_first, nocase=False, stopindex=END, regexp=True)
        if not while_first:
            break
        str_last = while_first + "+" + str(len("while")) + "c"
        Text_widget.tag_add("tag_whileh", while_first, str_last)
        while_first = str_last
    Text_widget.tag_config("tag_whileh", foreground=color)


def print_h(Text_widget, color):
    Text_widget.tag_remove("tag_printh", "1.0", END)
    print_first = "1.0"
    while True:
        print_first = Text_widget.search("\yprint\y", print_first, nocase=False, stopindex=END, regexp=True)
        if not print_first:
            break
        str_last = print_first + "+" + str(len("print")) + "c"
        Text_widget.tag_add("tag_printh", print_first, str_last)
        print_first = str_last
    Text_widget.tag_config("tag_printh", foreground=color)


def yield_h(Text_widget, color):
    Text_widget.tag_remove("tag_yieldh", "1.0", END)
    yield_first = "1.0"
    while True:
        yield_first = Text_widget.search("\yyield\y", yield_first, nocase=False, stopindex=END, regexp=True)
        if not yield_first:
            break
        str_last = yield_first + "+" + str(len("yield")) + "c"
        Text_widget.tag_add("tag_yieldh", yield_first, str_last)
        yield_first = str_last
    Text_widget.tag_config("tag_yieldh", foreground=color)

def pass_h(Text_widget, color):
    Text_widget.tag_remove("tag_passh", "1.0", END)
    pass_first = "1.0"
    while True:
        pass_first = Text_widget.search("\ypass\y", pass_first, nocase=False, stopindex=END, regexp=True)
        if not pass_first:
            break
        str_last = pass_first + "+" + str(len("pass")) + "c"
        Text_widget.tag_add("tag_passh", pass_first, str_last)
        pass_first = str_last
    Text_widget.tag_config("tag_passh", foreground=color)


def break_h(Text_widget, color):
    Text_widget.tag_remove("tag_breakh", "1.0", END)
    break_first = "1.0"
    while True:
        break_first = Text_widget.search("\ybreak\y", break_first, nocase=False, stopindex=END, regexp=True)
        if not break_first:
            break
        str_last = break_first + "+" + str(len("break")) + "c"
        Text_widget.tag_add("tag_breakh", break_first, str_last)
        break_first = str_last
    Text_widget.tag_config("tag_breakh", foreground=color)


def continue_h(Text_widget, color):
    Text_widget.tag_remove("tag_continueh", "1.0", END)
    continue_first = "1.0"
    while True:
        continue_first = Text_widget.search("\ycontinue\y", continue_first, nocase=False, stopindex=END, regexp=True)
        if not continue_first:
            break
        str_last = continue_first + "+" + str(len("continue")) + "c"
        Text_widget.tag_add("tag_continueh", continue_first, str_last)
        continue_first = str_last
    Text_widget.tag_config("tag_continueh", foreground=color)


def del_h(Text_widget, color):
    Text_widget.tag_remove("tag_delh", "1.0", END)
    del_first = "1.0"
    while True:
        del_first = Text_widget.search("\ydel\y", del_first, nocase=False, stopindex=END, regexp=True)
        if not del_first:
            break
        str_last = del_first + "+" + str(len("del")) + "c"
        Text_widget.tag_add("tag_delh", del_first, str_last)
        del_first = str_last
    Text_widget.tag_config("tag_delh", foreground=color)


def assert_h(Text_widget, color):
    Text_widget.tag_remove("tag_asserth", "1.0", END)
    assert_first = "1.0"
    while True:
        assert_first = Text_widget.search("\yassert\y", assert_first, nocase=False, stopindex=END, regexp=True)
        if not assert_first:
            break
        str_last = assert_first + "+" + str(len("assert")) + "c"
        Text_widget.tag_add("tag_asserth", assert_first, str_last)
        assert_first = str_last
    Text_widget.tag_config("tag_asserth", foreground=color)


def input_h(Text_widget, color):
    Text_widget.tag_remove("tag_inputh", "1.0", END)
    input_first = "1.0"
    while True:
        input_first = Text_widget.search("\yinput\y", input_first, nocase=False, stopindex=END, regexp=True)
        if not input_first:
            break
        str_last = input_first + "+" + str(len("input")) + "c"
        Text_widget.tag_add("tag_inputh", input_first, str_last)
        input_first = str_last
    Text_widget.tag_config("tag_inputh", foreground=color)


def import_h(Text_widget, color):
    Text_widget.tag_remove("tag_importh", "1.0", END)
    import_first = "1.0"
    while True:
        import_first = Text_widget.search("\yimport\y", import_first, nocase=False, stopindex=END, regexp=True)
        if not import_first:
            break
        str_last = import_first + "+" + str(len("import")) + "c"
        Text_widget.tag_add("tag_importh", import_first, str_last)
        import_first = str_last
    Text_widget.tag_config("tag_importh", foreground=color)



def from_h(Text_widget, color):
    Text_widget.tag_remove("tag_fromh", "1.0", END)
    from_first = "1.0"
    while True:
        from_first = Text_widget.search("\yfrom\y", from_first, nocase=False, stopindex=END, regexp=True)
        if not from_first:
            break
        str_last = from_first + "+" + str(len("from")) + "c"
        Text_widget.tag_add("tag_fromh", from_first, str_last)
        from_first = str_last
    Text_widget.tag_config("tag_fromh", foreground=color)


def with_h(Text_widget, color):
    Text_widget.tag_remove("tag_withh", "1.0", END)
    with_first = "1.0"
    while True:
        with_first = Text_widget.search("\ywith\y", with_first, nocase=False, stopindex=END, regexp=True)
        if not with_first:
            break
        str_last = with_first + "+" + str(len("with")) + "c"
        Text_widget.tag_add("tag_withh", with_first, str_last)
        with_first = str_last
    Text_widget.tag_config("tag_withh", foreground=color)


def float_h(Text_widget, color):
    Text_widget.tag_remove("tag_floath", "1.0", END)
    float_first = "1.0"
    while True:
        float_first = Text_widget.search("\yfloat\y", float_first, nocase=False, stopindex=END, regexp=True)
        if not float_first:
            break
        str_last = float_first + "+" + str(len("float")) + "c"
        Text_widget.tag_add("tag_floath", float_first, str_last)
        float_first = str_last
    Text_widget.tag_config("tag_floath", foreground=color)


def float_h(Text_widget, color):
    Text_widget.tag_remove("tag_floath", "1.0", END)
    float_first = "1.0"
    while True:
        float_first = Text_widget.search("\yfloat\y", float_first, nocase=False, stopindex=END, regexp=True)
        if not float_first:
            break
        str_last = float_first + "+" + str(len("float")) + "c"
        Text_widget.tag_add("tag_floath", float_first, str_last)
        float_first = str_last
    Text_widget.tag_config("tag_floath", foreground=color)


def complex_h(Text_widget, color):
    Text_widget.tag_remove("tag_complexh", "1.0", END)
    complex_first = "1.0"
    while True:
        complex_first = Text_widget.search("\ycomplex\y", complex_first, nocase=False, stopindex=END, regexp=True)
        if not complex_first:
            break
        str_last = complex_first + "+" + str(len("complex")) + "c"
        Text_widget.tag_add("tag_complexh", complex_first, str_last)
        complex_first = str_last
    Text_widget.tag_config("tag_complexh", foreground=color)


def open_h(Text_widget, color):
    Text_widget.tag_remove("tag_openh", "1.0", END)
    open_first = "1.0"
    while True:
        open_first = Text_widget.search("\yopen\y", open_first, nocase=False, stopindex=END, regexp=True)
        if not open_first:
            break
        str_last = open_first + "+" + str(len("open")) + "c"
        Text_widget.tag_add("tag_openh", open_first, str_last)
        open_first = str_last
    Text_widget.tag_config("tag_openh", foreground=color)



def as_h(Text_widget, color):
    Text_widget.tag_remove("tag_ash", "1.0", END)
    as_first = "1.0"
    while True:
        as_first = Text_widget.search("\yas\y", as_first, nocase=False, stopindex=END, regexp=True)
        if not as_first:
            break
        str_last = as_first + "+" + str(len("as")) + "c"
        Text_widget.tag_add("tag_ash", as_first, str_last)
        as_first = str_last
    Text_widget.tag_config("tag_ash", foreground=color)


def in_h(Text_widget, color):
    Text_widget.tag_remove("tag_inh", "1.0", END)
    in_first = "1.0"
    while True:
        in_first = Text_widget.search("\yin\y", in_first, nocase=False, stopindex=END, regexp=True)
        if not in_first:
            break
        str_last = in_first + "+" + str(len("in")) + "c"
        Text_widget.tag_add("tag_inh", in_first, str_last)
        in_first = str_last
    Text_widget.tag_config("tag_inh", foreground=color)


def or_h(Text_widget, color):
    Text_widget.tag_remove("tag_orh", "1.0", END)
    or_first = "1.0"
    while True:
        or_first = Text_widget.search("\yor\y", or_first, nocase=False, stopindex=END, regexp=True)
        if not or_first:
            break
        str_last = or_first + "+" + str(len("or")) + "c"
        Text_widget.tag_add("tag_orh", or_first, str_last)
        or_first = str_last
    Text_widget.tag_config("tag_orh", foreground=color)


def and_h(Text_widget, color):
    Text_widget.tag_remove("tag_andh", "1.0", END)
    and_first = "1.0"
    while True:
        and_first = Text_widget.search("\yand\y", and_first, nocase=False, stopindex=END, regexp=True)
        if not and_first:
            break
        str_last = and_first + "+" + str(len("and")) + "c"
        Text_widget.tag_add("tag_andh", and_first, str_last)
        and_first = str_last
    Text_widget.tag_config("tag_andh", foreground=color)


def def_h(Text_widget, color):
    Text_widget.tag_remove("tag_defh", "1.0", END)
    def_first = "1.0"
    while True:
        def_first = Text_widget.search("\ydef\y", def_first, nocase=False, stopindex=END, regexp=True)
        if not def_first:
            break
        str_last = def_first + "+" + str(len("def")) + "c"
        Text_widget.tag_add("tag_defh", def_first, str_last)
        def_first = str_last
    Text_widget.tag_config("tag_defh", foreground=color)


def class_h(Text_widget, color):
    Text_widget.tag_remove("tag_classh", "1.0", END)
    class_first = "1.0"
    while True:
        class_first = Text_widget.search("\yclass\y", class_first, nocase=False, stopindex=END, regexp=True)
        if not class_first:
            break
        str_last = class_first + "+" + str(len("class")) + "c"
        Text_widget.tag_add("tag_classh", class_first, str_last)
        class_first = str_last
    Text_widget.tag_config("tag_classh", foreground=color)


def str_h(Text_widget, color):
    Text_widget.tag_remove("tag_strh", "1.0", END)
    str_first = "1.0"
    while True:
        str_first = Text_widget.search("\ystr\y", str_first, nocase=False, stopindex=END, regexp=True)
        if not str_first:
            break
        str_last = str_first + "+" + str(len("str")) + "c"
        Text_widget.tag_add("tag_strh", str_first, str_last)
        str_first = str_last
    Text_widget.tag_config("tag_strh", foreground=color)


def int_h(Text_widget, color):
    Text_widget.tag_remove("tag_inth", "1.0", END)
    int_first = "1.0"
    while True:
        int_first = Text_widget.search("\yint\y", int_first, nocase=False, stopindex=END, regexp=True)
        if not int_first:
            break
        str_last = int_first + "+" + str(len("int")) + "c"
        Text_widget.tag_add("tag_inth", int_first, str_last)
        int_first = str_last
    Text_widget.tag_config("tag_inth", foreground=color)


def list_h(Text_widget, color):
    Text_widget.tag_remove("tag_listh", "1.0", END)
    list_first = "1.0"
    while True:
        list_first = Text_widget.search("\ylist\y", list_first, nocase=False, stopindex=END, regexp=True)
        if not list_first:
            break
        str_last = list_first + "+" + str(len("list")) + "c"
        Text_widget.tag_add("tag_listh", list_first, str_last)
        list_first = str_last
    Text_widget.tag_config("tag_listh", foreground=color)


def tuple_h(Text_widget, color):
    Text_widget.tag_remove("tag_tupleh", "1.0", END)
    tuple_first = "1.0"
    while True:
        tuple_first = Text_widget.search("\ytuple\y", tuple_first, nocase=False, stopindex=END, regexp=True)
        if not tuple_first:
            break
        str_last = tuple_first + "+" + str(len("tuple")) + "c"
        Text_widget.tag_add("tag_tupleh", tuple_first, str_last)
        tuple_first = str_last
    Text_widget.tag_config("tag_tupleh", foreground=color)


def set_h(Text_widget, color):
    Text_widget.tag_remove("tag_seth", "1.0", END)
    set_first = "1.0"
    while True:
        set_first = Text_widget.search("\yset\y", set_first, nocase=False, stopindex=END, regexp=True)
        if not set_first:
            break
        str_last = set_first + "+" + str(len("set")) + "c"
        Text_widget.tag_add("tag_seth", set_first, str_last)
        set_first = str_last
    Text_widget.tag_config("tag_seth", foreground=color)


def dict_h(Text_widget, color):
    Text_widget.tag_remove("tag_dicth", "1.0", END)
    dict_first = "1.0"
    while True:
        dict_first = Text_widget.search("\ydict\y", dict_first, nocase=False, stopindex=END, regexp=True)
        if not dict_first:
            break
        str_last = dict_first + "+" + str(len("dict")) + "c"
        Text_widget.tag_add("tag_dicth", dict_first, str_last)
        dict_first = str_last
    Text_widget.tag_config("tag_dicth", foreground=color)


def lambda_h(Text_widget, color):
    Text_widget.tag_remove("tag_lambdah", "1.0", END)
    lambda_first = "1.0"
    while True:
        lambda_first = Text_widget.search("\ylambda\y", lambda_first, nocase=False, stopindex=END, regexp=True)
        if not lambda_first:
            break
        str_last = lambda_first + "+" + str(len("lambda")) + "c"
        Text_widget.tag_add("tag_lambdah", lambda_first, str_last)
        lambda_first = str_last
    Text_widget.tag_config("tag_lambdah", foreground=color)


def True_h(Text_widget, color):
    Text_widget.tag_remove("tag_Trueh", "1.0", END)
    True_first = "1.0"
    while True:
        True_first = Text_widget.search("\yTrue\y", True_first, nocase=False, stopindex=END, regexp=True)
        if not True_first:
            break
        str_last = True_first + "+" + str(len("True")) + "c"
        Text_widget.tag_add("tag_Trueh", True_first, str_last)
        True_first = str_last
    Text_widget.tag_config("tag_Trueh", foreground=color)


def False_h(Text_widget, color):
    Text_widget.tag_remove("tag_Falseh", "1.0", END)
    False_first = "1.0"
    while True:
        False_first = Text_widget.search("\yFalse\y", False_first, nocase=False, stopindex=END, regexp=True)
        if not False_first:
            break
        str_last = False_first + "+" + str(len("False")) + "c"
        Text_widget.tag_add("tag_Falseh", False_first, str_last)
        False_first = str_last
    Text_widget.tag_config("tag_Falseh", foreground=color)


def None_h(Text_widget, color):
    Text_widget.tag_remove("tag_Noneh", "1.0", END)
    None_first = "1.0"
    while True:
        None_first = Text_widget.search("\yNone\y", None_first, nocase=False, stopindex=END, regexp=True)
        if not None_first:
            break
        str_last = None_first + "+" + str(len("None")) + "c"
        Text_widget.tag_add("tag_Noneh", None_first, str_last)
        None_first = str_last
    Text_widget.tag_config("tag_Noneh", foreground=color)


def nonlocal_h(Text_widget, color):
    Text_widget.tag_remove("tag_nonlocalh", "1.0", END)
    nonlocal_first = "1.0"
    while True:
        nonlocal_first = Text_widget.search("\ynonlocal\y", nonlocal_first, nocase=False, stopindex=END, regexp=True)
        if not nonlocal_first:
            break
        str_last = nonlocal_first + "+" + str(len("nonlocal")) + "c"
        Text_widget.tag_add("tag_nonlocalh", nonlocal_first, str_last)
        nonlocal_first = str_last
    Text_widget.tag_config("tag_nonlocalh", foreground=color)



def raise_h(Text_widget, color):
    Text_widget.tag_remove("tag_raiseh", "1.0", END)
    raise_first = "1.0"
    while True:
        raise_first = Text_widget.search("\yraise\y", raise_first, nocase=False, stopindex=END, regexp=True)
        if not raise_first:
            break
        str_last = raise_first + "+" + str(len("raise")) + "c"
        Text_widget.tag_add("tag_raiseh", raise_first, str_last)
        raise_first = str_last
    Text_widget.tag_config("tag_raiseh", foreground=color)



def return_h(Text_widget, color):
    Text_widget.tag_remove("tag_returnh", "1.0", END)
    return_first = "1.0"
    while True:
        return_first = Text_widget.search("\yreturn\y", return_first, nocase=False, stopindex=END, regexp=True)
        if not return_first:
            break
        str_last = return_first + "+" + str(len("return")) + "c"
        Text_widget.tag_add("tag_returnh", return_first, str_last)
        return_first = str_last
    Text_widget.tag_config("tag_returnh", foreground=color)



def global_h(Text_widget, color):
    Text_widget.tag_remove("tag_globalh", "1.0", END)
    global_first = "1.0"
    while True:
        global_first = Text_widget.search("\yglobal\y", global_first, nocase=False, stopindex=END, regexp=True)
        if not global_first:
            break
        str_last = global_first + "+" + str(len("global")) + "c"
        Text_widget.tag_add("tag_globalh", global_first, str_last)
        global_first = str_last
    Text_widget.tag_config("tag_globalh", foreground=color)



def Exception_h(Text_widget, color):
    Text_widget.tag_remove("tag_Exceptionh", "1.0", END)
    Exception_first = "1.0"
    while True:
        Exception_first = Text_widget.search("\yException\y", Exception_first, nocase=False, stopindex=END, regexp=True)
        if not Exception_first:
            break
        str_last = Exception_first + "+" + str(len("Exception")) + "c"
        Text_widget.tag_add("tag_Exceptionh", Exception_first, str_last)
        Exception_first = str_last
    Text_widget.tag_config("tag_Exceptionh", foreground=color)


def single_qouts_h(Text_widget, color):
    f_get = Text_widget.get(1.0, END)
    y2 = re.findall(r"'(.*?)'", f_get)
    bg = -1
    Text_widget.tag_remove("tag_qs", "1.0", END)
    for i in y2:
        bg += 1
        qs_first = "1.0"
        while True:
            qs_first = Text_widget.search(f"'{y2[bg]}'", qs_first, nocase=False, stopindex=END, regexp=True)
            if not qs_first:
                break
            str_last = qs_first + "+" + str(len(f"'{y2[bg]}'")) + "c"
            Text_widget.tag_add("tag_qs", qs_first, str_last)
            qs_first = str_last
        Text_widget.tag_config("tag_qs", foreground=color)


def double_qouts_h(Text_widget, color):
    f_get = Text_widget.get(1.0, END)
    if True:
        try:
            y = re.findall(r'"(.*?)"', f_get)
            br = -1
            Text_widget.tag_remove("tag_qt", "1.0", END)
            for i in y:
                br += 1
                qt_first = "1.0"
                while True:
                    qt_first = Text_widget.search(f'"{y[br]}"', qt_first, nocase=False, stopindex=END, regexp=True)
                    if not qt_first:
                        break
                    str_last = qt_first + "+" + str(len(f'"{y[br]}"')) + "c"
                    Text_widget.tag_add("tag_qt", qt_first, str_last)
                    qt_first = str_last
                Text_widget.tag_config("tag_qt", foreground=color)
        except:
            pass  



def function_h(Text_widget, color):
    fine = Text_widget.get(1.0, END)
    y3 = re.findall(r'\.\w+', fine)
    bgg = -1
    Text_widget.tag_remove("tag_fnny", "1.0", END)
    for i in y3:
        bgg += 1
        fnn_first = "1.0"
        while True:
            fnn_first = Text_widget.search(f'{y3[bgg]}', fnn_first, nocase=False, stopindex=END, regexp=True)
            if not fnn_first:
                break
            str_last = fnn_first + "+" + str(len(f'{y3[bgg]}')) + "c"
            Text_widget.tag_add("tag_fnny", fnn_first, str_last)
            fnn_first = str_last
        Text_widget.tag_config("tag_fnny", foreground=color)



def colon_h(Text_widget, color):
    Text_widget.tag_remove("tag_colonh", "1.0", END)
    colon_first = "1.0"
    while True:
        colon_first = Text_widget.search(":", colon_first, nocase=False, stopindex=END)
        if not colon_first:
            break
        str_last = colon_first + "+" + str(len(":")) + "c"
        Text_widget.tag_add("tag_colonh", colon_first, str_last)
        colon_first = str_last
    Text_widget.tag_config("tag_colonh", foreground=color)


def plus_h(Text_widget, color):
    Text_widget.tag_remove("tag_plush", "1.0", END)
    plus_first = "1.0"
    while True:
        plus_first = Text_widget.search("+", plus_first, nocase=False, stopindex=END)
        if not plus_first:
            break
        str_last = plus_first + "+" + str(len("+")) + "c"
        Text_widget.tag_add("tag_plush", plus_first, str_last)
        plus_first = str_last
    Text_widget.tag_config("tag_plush", foreground=color)

def minus_h(Text_widget, color):
    Text_widget.tag_remove("tag_minush", "1.0", END)
    minus_first = "1.0"
    while True:
        minus_first = Text_widget.search("-", minus_first, nocase=False, stopindex=END)
        if not minus_first:
            break
        str_last = minus_first + "+" + str(len("-")) + "c"
        Text_widget.tag_add("tag_minush", minus_first, str_last)
        minus_first = str_last
    Text_widget.tag_config("tag_minush", foreground=color)

def star_h(Text_widget, color):
    Text_widget.tag_remove("tag_multiplyh", "1.0", END)
    multiply_first = "1.0"
    while True:
        multiply_first = Text_widget.search("*", multiply_first, nocase=False, stopindex=END)
        if not multiply_first:
            break
        str_last = multiply_first + "+" + str(len("*")) + "c"
        Text_widget.tag_add("tag_multiplyh", multiply_first, str_last)
        multiply_first = str_last
    Text_widget.tag_config("tag_multiplyh", foreground=color)

def divide_h(Text_widget, color):
    Text_widget.tag_remove("tag_dividehy", "1.0", END)
    divide_first = "1.0"
    while True:
        divide_first = Text_widget.search("/", divide_first, nocase=False, stopindex=END)
        if not divide_first:
            break
        str_last = divide_first + "+" + str(len("/")) + "c"
        Text_widget.tag_add("tag_dividehy", divide_first, str_last)
        divide_first = str_last
    Text_widget.tag_config("tag_dividehy", foreground=color)


def one_h(Text_widget, color):
    Text_widget.tag_remove("tag_oneh", "1.0", END)
    one_first = "1.0"
    while True:
        one_first = Text_widget.search("1", one_first, nocase=False, stopindex=END)
        if not one_first:
            break
        str_last = one_first + "+" + str(len("1")) + "c"
        Text_widget.tag_add("tag_oneh", one_first, str_last)
        one_first = str_last
    Text_widget.tag_config("tag_oneh", foreground=color)

def two_h(Text_widget, color):
    Text_widget.tag_remove("tag_twoh", "1.0", END)
    two_first = "1.0"
    while True:
        two_first = Text_widget.search("2", two_first, nocase=False, stopindex=END)
        if not two_first:
            break
        str_last = two_first + "+" + str(len("2")) + "c"
        Text_widget.tag_add("tag_twoh", two_first, str_last)
        two_first = str_last
    Text_widget.tag_config("tag_twoh", foreground=color)

def three_h(Text_widget, color):
    Text_widget.tag_remove("tag_threeh", "1.0", END)
    three_first = "1.0"
    while True:
        three_first = Text_widget.search("3", three_first, nocase=False, stopindex=END)
        if not three_first:
            break
        str_last = three_first + "+" + str(len("3")) + "c"
        Text_widget.tag_add("tag_threeh", three_first, str_last)
        three_first = str_last
    Text_widget.tag_config("tag_threeh", foreground=color)

def four_h(Text_widget, color):
    Text_widget.tag_remove("tag_fourh", "1.0", END)
    four_first = "1.0"
    while True:
        four_first = Text_widget.search("4", four_first, nocase=False, stopindex=END)
        if not four_first:
            break
        str_last = four_first + "+" + str(len("4")) + "c"
        Text_widget.tag_add("tag_fourh", four_first, str_last)
        four_first = str_last
    Text_widget.tag_config("tag_fourh", foreground=color)

def five_h(Text_widget, color):
    Text_widget.tag_remove("tag_fiveh", "1.0", END)
    five_first = "1.0"
    while True:
        five_first = Text_widget.search("5", five_first, nocase=False, stopindex=END)
        if not five_first:
            break
        str_last = five_first + "+" + str(len("5")) + "c"
        Text_widget.tag_add("tag_fiveh", five_first, str_last)
        five_first = str_last
    Text_widget.tag_config("tag_fiveh", foreground=color)

def six_h(Text_widget, color):
    Text_widget.tag_remove("tag_sixh", "1.0", END)
    six_first = "1.0"
    while True:
        six_first = Text_widget.search("6", six_first, nocase=False, stopindex=END)
        if not six_first:
            break
        str_last = six_first + "+" + str(len("6")) + "c"
        Text_widget.tag_add("tag_sixh", six_first, str_last)
        six_first = str_last
    Text_widget.tag_config("tag_sixh", foreground=color)

def seven_h(Text_widget, color):
    Text_widget.tag_remove("tag_sevenh", "1.0", END)
    seven_first = "1.0"
    while True:
        seven_first = Text_widget.search("7", seven_first, nocase=False, stopindex=END)
        if not seven_first:
            break
        str_last = seven_first + "+" + str(len("7")) + "c"
        Text_widget.tag_add("tag_sevenh", seven_first, str_last)
        seven_first = str_last
    Text_widget.tag_config("tag_sevenh", foreground=color)

def eight_h(Text_widget, color):
    Text_widget.tag_remove("tag_eighth", "1.0", END)
    eight_first = "1.0"
    while True:
        eight_first = Text_widget.search("8", eight_first, nocase=False, stopindex=END)
        if not eight_first:
            break
        str_last = eight_first + "+" + str(len("8")) + "c"
        Text_widget.tag_add("tag_eighth", eight_first, str_last)
        eight_first = str_last
    Text_widget.tag_config("tag_eighth", foreground=color)

def nine_h(Text_widget, color):
    Text_widget.tag_remove("tag_nineh", "1.0", END)
    nine_first = "1.0"
    while True:
        nine_first = Text_widget.search("9", nine_first, nocase=False, stopindex=END)
        if not nine_first:
            break
        str_last = nine_first + "+" + str(len("9")) + "c"
        Text_widget.tag_add("tag_nineh", nine_first, str_last)
        nine_first = str_last
    Text_widget.tag_config("tag_nineh", foreground=color)

def zero_h(Text_widget, color):
    Text_widget.tag_remove("tag_zeroh", "1.0", END)
    zero_first = "1.0"
    while True:
        zero_first = Text_widget.search("0", zero_first, nocase=False, stopindex=END)
        if not zero_first:
            break
        str_last = zero_first + "+" + str(len("0")) + "c"
        Text_widget.tag_add("tag_zeroh", zero_first, str_last)
        zero_first = str_last
    Text_widget.tag_config("tag_zeroh", foreground=color)



def greater_than_h(Text_widget, color):
    Text_widget.tag_remove("tag_moreh", "1.0", END)
    more_first = "1.0"
    while True:
        more_first = Text_widget.search(">", more_first, nocase=False, stopindex=END)
        if not more_first:
            break
        str_last = more_first + "+" + str(len(">")) + "c"
        Text_widget.tag_add("tag_moreh", more_first, str_last)
        more_first = str_last
    Text_widget.tag_config("tag_moreh", foreground=color)


def less_than_h(Text_widget, color):
    Text_widget.tag_remove("tag_lessh", "1.0", END)
    less_first = "1.0"
    while True:
        less_first = Text_widget.search("<", less_first, nocase=False, stopindex=END)
        if not less_first:
            break
        str_last = less_first + "+" + str(len("<")) + "c"
        Text_widget.tag_add("tag_lessh", less_first, str_last)
        less_first = str_last
    Text_widget.tag_config("tag_lessh", foreground=color)



def bar_h(Text_widget, color):
    Text_widget.tag_remove("tag_barh", "1.0", END)
    bar_first = "1.0"
    while True:
        bar_first = Text_widget.search("|", bar_first, nocase=False, stopindex=END)
        if not bar_first:
            break
        str_last = bar_first + "+" + str(len("|")) + "c"
        Text_widget.tag_add("tag_barh", bar_first, str_last)
        bar_first = str_last
    Text_widget.tag_config("tag_barh", foreground=color)



def forward_slash_h(Text_widget, color):
    Text_widget.tag_remove("tag_foreh", "1.0", END)
    fore_first = "1.0"
    while True:
        fore_first = Text_widget.search("\\", fore_first, nocase=False, stopindex=END)
        if not fore_first:
            break
        str_last = fore_first + "+" + str(len("\\n")) + "c"
        Text_widget.tag_add("tag_foreh", fore_first, str_last)
        fore_first = str_last
    Text_widget.tag_config("tag_foreh", foreground=color)



def exclamation_h(Text_widget, color):
    Text_widget.tag_remove("tag_exclamationh", "1.0", END)
    exclamation_first = "1.0"
    while True:
        exclamation_first = Text_widget.search("!", exclamation_first, nocase=False, stopindex=END)
        if not exclamation_first:
            break
        str_last = exclamation_first + "+" + str(len("!")) + "c"
        Text_widget.tag_add("tag_exclamationh", exclamation_first, str_last)
        exclamation_first = str_last
    Text_widget.tag_config("tag_exclamationh", foreground=color)

def square_h(Text_widget, color):
    Text_widget.tag_remove("tag_astringh", "1.0", END)
    astring_first = "1.0"
    while True:
        astring_first = Text_widget.search("^", astring_first, nocase=False, stopindex=END)
        if not astring_first:
            break
        str_last = astring_first + "+" + str(len("^")) + "c"
        Text_widget.tag_add("tag_astringh", astring_first, str_last)
        astring_first = str_last
    Text_widget.tag_config("tag_astringh", foreground=color)

def fstring_h(Text_widget, color):
    Text_widget.tag_remove("tag_fstringh", "1.0", END)
    fstring_first = "1.0"
    while True:
        fstring_first = Text_widget.search("f'", fstring_first, nocase=False, stopindex=END)
        if not fstring_first:
            break
        str_last = fstring_first + "+" + str(len("f")) + "c"
        Text_widget.tag_add("tag_fstringh", fstring_first, str_last)
        fstring_first = str_last
    Text_widget.tag_config("tag_fstringh", foreground=color)

def rstring_h(Text_widget, color):
    Text_widget.tag_remove("tag_rstringh", "1.0", END)
    rstring_first = "1.0"
    while True:
        rstring_first = Text_widget.search("r'", rstring_first, nocase=False, stopindex=END)
        if not rstring_first:
            break
        str_last = rstring_first + "+" + str(len("r")) + "c"
        Text_widget.tag_add("tag_rstringh", rstring_first, str_last)
        rstring_first = str_last
    Text_widget.tag_config("tag_rstringh", foreground=color)

def percentage_h(Text_widget, color):
    Text_widget.tag_remove("tag_percentageh", "1.0", END)
    percentage_first = "1.0"
    while True:
        percentage_first = Text_widget.search("%", percentage_first, nocase=False, stopindex=END)
        if not percentage_first:
            break
        str_last = percentage_first + "+" + str(len("%")) + "c"
        Text_widget.tag_add("tag_percentageh", percentage_first, str_last)
        percentage_first = str_last
    Text_widget.tag_config("tag_percentageh", foreground=color)


def custom_h(Text_widget, characters, color):
    tagey = f'{characters}h'
    Text_widget.tag_remove(tagey, "1.0", END)
    ratata_first = "1.0"
    while True:
        ratata_first = Text_widget.search(f"\y{characters}\y", ratata_first, nocase=False, stopindex=END, regexp=True)
        if not ratata_first:
            break
        str_last = ratata_first + "+" + str(len(f"{characters}")) + "c"
        Text_widget.tag_add(tagey, ratata_first, str_last)
        ratata_first = str_last
    Text_widget.tag_config(tagey, foreground=color)


def custom_chars_h(Text_widget, char, color):
    tagey = f'{char}h'
    Text_widget.tag_remove(tagey, "1.0", END)
    ratata_first = "1.0"
    while True:
        ratata_first = Text_widget.search(f"{char}", ratata_first, nocase=False, stopindex=END)
        if not ratata_first:
            break
        str_last = ratata_first + "+" + str(len(f"{char}")) + "c"
        Text_widget.tag_add(tagey, ratata_first, str_last)
        ratata_first = str_last
    Text_widget.tag_config(tagey, foreground=color)


def custom_regex_h(Text_widget, pattern, color):
    tagey = f'{pattern}h'
    fine = Text_widget.get(1.0, END)
    y3 = re.findall(f'{pattern}', fine)
    bgh = -1
    Text_widget.tag_remove(tagey, "1.0", END)
    for i in y3:
        bgh += 1
        custom_first = "1.0"
        while True:
            custom_first = Text_widget.search(f'{y3[bgh]}', custom_first, nocase=False, stopindex=END)
            if not custom_first:
                break
            str_last = custom_first + "+" + str(len(f'{y3[bgh]}')) + "c"
            Text_widget.tag_add(tagey, custom_first, str_last)
            custom_first = str_last
        Text_widget.tag_config(tagey, foreground=color)


def each_h(Text_widget, color):
    f_gety = Text_widget.get(1.0, END)
    yyer = re.findall(r'\@\w+\b', f_gety)
    bg = -1
    Text_widget.tag_remove("finerrdr", "1.0", END)
    for i in yyer:
        bg += 1
        qs_first = "1.0"
        while True:
            qs_first = Text_widget.search(f"'{yyer[bg]}'", qs_first, nocase=False, stopindex=END, regexp=True)
            if not qs_first:
                break
            str_last = qs_first + "+" + str(len(f"'{yyer[bg]}'")) + "c"
            Text_widget.tag_add("finerrdr", qs_first, str_last)
            qs_first = str_last
        Text_widget.tag_config("finerrdr", foreground=color)













