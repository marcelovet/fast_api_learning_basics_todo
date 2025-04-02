from setup import base


class Settings:
    def __init__(self):
        for setting in dir(base):
            if setting.isupper():
                setattr(self, setting, getattr(base, setting))


settings = Settings()
