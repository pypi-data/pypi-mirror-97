import os
from pathlib import Path

from easyshare.logging import init_logging
from easyshare.utils.os import walk_preorder

if __name__ == "__main__":
    init_logging(4)
    PATH = "/home/stefano/Temp/Poweramp/poweramp/original"
    # print("-- TOPDOWN --")
    # for root, dirnames, files in os.walk(PATH, topdown=True):
    #     print(f"{root}")
    #
    #     for f in files:
    #         print(f"-> f = {f}")
    #
    #     for d in dirnames:
    #         print(f"-> f = {d}")
    #
    # print("---------------------")

    for f, stat in walk_preorder(Path(PATH), max_depth=1):
        print(str(f))