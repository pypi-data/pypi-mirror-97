from . import exceptions
from . import session

__all__ = (
    *exceptions.__all__,
    *session.__all__,
)

__version__ = '20.03.10'


def get_user_agent():
    return 'Backend.AI Client for Python {0}'.format(__version__)
