from dataclasses import dataclass
import json

file_locate = './config.json'

@dataclass
class Config:
    tg_chat_id: int
    sferum_groups: list[int]
    
def GET() -> Config:
    with open(file_locate, "r", encoding="utf-8") as file:
        data = json.load(file)
        return Config(**data)

def SAVE(new_config: Config) -> None:
    json_dict = new_config.__dict__
    with open(file_locate, "w", encoding="utf-8") as file:
        json.dump(json_dict, file, indent=4, ensure_ascii=False)
        