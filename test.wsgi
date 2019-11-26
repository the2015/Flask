# wsgi配置文件
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from manage import app

application = app
