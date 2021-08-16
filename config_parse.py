from configparser import ConfigParser


class GlobalConfig:
    def __init__(self):
        print('initializing config')
        self.api_key = None

    def populate(self):
        cfg = ConfigParser() 
        cfg.read('config.ini')
        self.api_key = cfg.get('api', 'key')


config = GlobalConfig()
config.populate()
print(config.api_key)
