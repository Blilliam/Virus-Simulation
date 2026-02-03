import pathlib
import tomllib

class Config:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def load(path = "infectioninfo.toml"):
        p = pathlib.Path(path)
        with p.open("rb") as f:
            data = tomllib.load(f)

        return Config(data)
    
    def get(self, *keys, default = None):
        cur = self.data
        
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur