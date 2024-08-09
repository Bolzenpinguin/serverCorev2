import os


class Config:
    DEBUG = True
    DATABASE_URI = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'calender.db')
