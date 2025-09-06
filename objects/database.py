import json

file_locate = './simple_database.json'
    
def GET() -> dict:
    with open(file_locate, "r", encoding="utf-8") as file:
        return json.load(file)
    
def SAVE(new_db: dict) -> None:
    with open(file_locate, "w", encoding="utf-8") as file:
        json.dump(new_db, file, indent=4, ensure_ascii=False)
        