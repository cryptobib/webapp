#!/usr/bin/env python2

import os, sys
os.chdir(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..")
)
sys.path.append(".")

import gluon.shell
from gluon.storage import Storage

def main():
    env = Storage(gluon.shell.env("crypto", import_models = True))
    env.db.import_from_csv_file(sys.stdin)
    env.db.commit()

if __name__ == "__main__":
    main()
