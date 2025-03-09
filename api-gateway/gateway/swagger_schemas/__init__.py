from .auth import AUTH_SCHEMAS
from .users import USER_SCHEMAS
from .events import EVENT_SCHEMAS

ALL_SCHEMAS = {
    **AUTH_SCHEMAS,
    **USER_SCHEMAS,
    **EVENT_SCHEMAS,
}
