from pocketbase import PocketBase
import os
from dotenv import load_dotenv

load_dotenv()

client = PocketBase('http://127.0.0.1:8090')
admin_data = client.admins.auth_with_password(os.environ['PB_USERNAME'], os.environ['PB_PASSWORD'])
