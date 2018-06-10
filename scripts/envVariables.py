import dotenv
import os


environmentParameters = dotenv.main.dotenv_values('.env')
os.environ.update(environmentParameters)
config = os.environ

URI = config.get('URI')
GITTER_TOKEN = config.get('GITTER_TOKEN')
DOMAIN_API = config.get('DOMAIN_API')
JWT_TOKEN = config.get('JWT_TOKEN')
