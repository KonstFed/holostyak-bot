import db_utils
import json
if __name__=="__main__":
    f = open("configs/config.json")
    config = json.load(f)
    db = db_utils.db_manager(config["db"])
    db.create_table("ideas")
