import sys
sys.path.insert(0,"/var/www/html")
from app import create_app
application = create_app()