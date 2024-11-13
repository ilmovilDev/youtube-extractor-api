from decouple import config


class Config():
    GROQ_API_KEY = config('GROQ_API_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}