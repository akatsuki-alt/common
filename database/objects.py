from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy import *


Base = declarative_base()

