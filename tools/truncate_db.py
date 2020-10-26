#!/usr/bin/env python2
import traceback
import os, sys
os.chdir(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..")
)
sys.path.append(".")

import gluon.shell
from gluon.storage import Storage

def main():
    if input("are you sure to erase everything (YES / NO)? ") == "YES":
        env = Storage(gluon.shell.env("crypto", import_models = True))
        for table_name in env.db.tables():
            try:
                print('Truncate "%s"' % table_name)
                env.db[table_name].truncate()
            except:
                print(env.db._lastsql)
                print(traceback.format_exc())
        env.db.commit()

if __name__ == "__main__":
    main()
