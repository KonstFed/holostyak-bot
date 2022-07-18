import db_utils
import json
import os
if __name__=="__main__":
    abs_path = os.path.abspath(__file__)
    dname = os.path.dirname(abs_path)
    os.chdir(dname)
    f = open("configs/config.json")
    config = json.load(f)
    db = db_utils.db_manager(config["db"])
    db.create_table("ideas")
