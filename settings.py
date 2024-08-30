from dataclasses import dataclass, asdict, field
import json
from pathlib import Path


@dataclass
class Settings:
    days_scan: int = 1
    floor_profit: int = 1
    refresh_time: int = 120
    region: str = 'BR'
    match_status: str = 'prematch'    # List of match status ('prematch','inplay','all') others
    bookmakers: dict = field(default_factory=dict)  # Get all from API


    def save(self):
        with open('settings.json','w') as f:
            json.dump(asdict(self), f, indent = 4)


    @classmethod
    def load(cls) -> 'Settings':
        if Path('settings.json').exists():
            with open('settings.json','r') as f:
                data = json.load(f)
                return cls(**data)
        else:
            return cls()
    

