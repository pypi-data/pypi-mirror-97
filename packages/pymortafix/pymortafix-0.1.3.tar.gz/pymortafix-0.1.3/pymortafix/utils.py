from re import findall, match, sub

from colorifix.colorifix import erase
from pymortafix._getchar import _Getch


def _get_index_from_matching(matching):
    return [i for i, group in enumerate(matching.groups()) if group][0]


def multisub(sub_dict, string, sequential=False):
    """Infinite sub in one iteration # sub_dict: {what_to_sub:substitution}"""
    if not sequential:
        rgx = "|".join(f"({s})" for s in sub_dict.keys())
        return sub(
            rgx,
            lambda m: sub_dict.get(list(sub_dict)[_get_index_from_matching(m)]),
            string,
        )
    else:
        for rgx, substitution in sub_dict.items():
            string = sub(rgx, substitution, string)
        return string


def strict_input(
    text, wrong_text=None, choices=None, regex=None, flush=False, check=None
):
    """Get user input with some requirements"""
    inp = input(text)
    if flush:
        erase(len(findall(r"\n", text)) + 1)
    while (
        (not choices or choices and inp not in choices)
        and (not regex or regex and not match(regex, inp))
        and (not check or check and not check(inp))
    ):
        if wrong_text:
            inp = input(wrong_text)
        else:
            inp = input(text)
        if flush:
            erase(len(findall(r"\n", wrong_text or text)) + 1)
    return inp


def direct_input(choices):
    """Get user single char input w/o return, with optional restricted choices"""
    inkey = _Getch()
    k = inkey()
    while choices and k not in choices:
        k = inkey()
    return k
