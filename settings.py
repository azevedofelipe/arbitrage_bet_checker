from dataclasses import dataclass, asdict, field
import json
from pathlib import Path
from utils.utils import create_driver, call_api


@dataclass
class Settings:
    days_scan: int = 1
    refresh_time: int = 120
    sports: list = field(default_factory=list)
    region: str = 'BR'
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
    

    def get_bookmakers(self):
        url = f'https://oddspedia.com/api/v1/getBookmakers?geoCode={self.region}&geoState=&language=en'
        driver = create_driver()
        json = call_api(driver,url)
        driver.quit()

        if json:
            books = json['data']
            for book in books:
                self.bookmakers[book['name']] = True

