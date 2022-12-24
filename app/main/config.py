import os


# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AWS_ACCESSKEY  = 'AKIAVXZXAG3GYFRSL733'
    AWS_SECRETKEY = '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'
    BUCKET_URL = 'files.backend.projects'
