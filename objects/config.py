from dataclasses import dataclass
import json
import warnings

file_locate = './config.json'

@dataclass
class Config:
    tg_chat_id: int
    sferum_groups: list[int]
    _existing_groups: list[int]
    
    @property
    def existing_groups(self) -> list[int]:
        return self._existing_groups
    
    @existing_groups.setter
    def existing_groups(self, value: list) -> None:
        warnings.warn("existing_groups can't be modified (except starting)! be careful with using that shit pls", ValueError)
        self._existing_groups = value
        
def GET() -> Config:
    with open(file_locate, "r", encoding="utf-8") as file:
        data = json.load(file)
        return Config(**data)

def SAVE(new_config: Config) -> None:
    json_dict = new_config.__dict__
    with open(file_locate, "w", encoding="utf-8") as file:
        json.dump(json_dict, file, indent=4, ensure_ascii=False)