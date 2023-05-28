from pocketbase import PocketBase
import os
from dotenv import load_dotenv

load_dotenv()

client = PocketBase(os.environ['PB_HOST'])
admin_data = client.admins.auth_with_password(os.environ['PB_USERNAME'], os.environ['PB_PASSWORD'])
