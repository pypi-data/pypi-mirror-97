from openmodule.database.database import register_bases
from openmodule_test.database_models import Base

register_bases(Base)

from openmodule.database.env import *