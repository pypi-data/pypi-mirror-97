import os
import re
import readline as rl
import sys

from easyshare.es.ui import print_tabulated, StyledString
from easyshare.logging import init_logging, get_logger
from easyshare.utils.rl import rl_load, rl_set_completer_quote_characters, rl_set_rl_attempted_completion_over

log = get_logger(__name__)

_SHELL_TOKEN_REGEX = re.compile(r'("(?:.)+|(?:\\ |\S)+)$')

ROOT = "/hd/Music/Main"
SUGGESTIONS = [os.path.join(ROOT, f) for f in os.listdir(ROOT)] + [
    "/home/stefano/Temp/questionario_montangero"
]

suggestion_idx = 0
suggestions = []

prompt = "> "
current_line = ""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs, flush=True)


def input_loop():
    while True:
        try:
            input(prompt)
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue

def generate_suggestions(token: str):
    return [s for s in SUGGESTIONS if s.startswith(token)]

def display_suggestions(substitution, matches, longest_match_length):
    """ Display the current suggestions """
    # Simulate the default behaviour of readline, but:
    # 1. Separate the concept of suggestion/rendered suggestion: in this
    #    way we can render a colored suggestion while using the readline
    #    core for treat it as a simple string
    # 2. Internally handles the max_columns constraints

    print("")  # break the prompt line

    # print the suggestions (without the dummy addition for avoid completion)
    print_tabulated([StyledString(os.path.basename(s)) for s in suggestions], longest_match_length)

    # Manually print what was displayed (prompt plus content)
    print(prompt + current_line, end="", flush=True)

def next_suggestion(token: str, count: int):
    global suggestion_idx
    global suggestions
    global current_line

    # def qc():
    #     try:
    #         libreadline = ctypes.CDLL("libreadline.so")
    #
    #         rl_completion_quote_character = ctypes.c_int.in_dll(
    #             libreadline,
    #             "rl_completion_quote_character"
    #         )
    #         eprint(f"rl_completion_quote_character: {rl_completion_quote_character}")
    #         #
    #         # rl_completer_quote_characters = ctypes.c_char_p.in_dll(
    #         #     libreadline,
    #         #     "rl_completer_quote_characters"
    #         # )
    #         # log.d(f"rl_completer_quote_characters is {rl_completer_quote_characters.value}")
    #
    #
    #         return rl_completion_quote_character.value
    #     except Exception as e:
    #         log.w(f"rl_completion_quote_character set failed: {e}")
    #         return None

    eprint(f"token: {token}")
    # quoting_char = rl_get_completion_quote_character()
    # quoting_char = qc()
    # eprint(f"quoting with: {quoting_char}")

    current_line = rl.get_line_buffer()
    stripped_current_line = current_line.lstrip()

    if count == 0:
        suggestions = generate_suggestions(token)
        suggestion_idx = 0

    if count < len(suggestions):
        sug = suggestions[suggestion_idx]
        # sug = sug.replace(" ", "\\ ")
        eprint(f"[{suggestion_idx}]: {sug}")
        suggestion_idx += 1
        return sug

    return None

def init_rl():
    rl.parse_and_bind("tab: complete")
    rl.parse_and_bind("set completion-query-items 50")
    # rl.set_completer_delims(rl.get_completer_delims().replace("-", "").replace("\\", " "))
    rl.set_completer_delims(" ")
    rl.set_completer(next_suggestion)
    # rl.set_completion_display_matches_hook(display_suggestions)

    rl_set_completer_quote_characters()
    rl_set_rl_attempted_completion_over()
    # rl_set_rl_char_is_quoted_p()


def main():
    init_rl()
    input_loop()

if __name__ == "__main__":
    init_logging(5)
    rl_load()
    main()