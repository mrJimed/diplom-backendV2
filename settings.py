import os

from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.abspath(__file__))
env_vars = dotenv_values(os.path.join(current_dir, '.config.env'))

DB_CONNECTION = env_vars.get('DB_CONNECTION')
SECRET_KEY = env_vars.get('SECRET_KEY')

# email/smtp config
SMTP_PORT = int(env_vars.get('SMTP_PORT'))
SMTP_HOST = env_vars.get('SMTP_HOST')
FROM_EMAIL = env_vars.get('FROM_EMAIL')
EMAIL_PASSWORD = env_vars.get('EMAIL_PASSWORD')
