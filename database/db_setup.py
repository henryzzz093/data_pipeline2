from database.models.util import DBSetup
from database.constants import ConnectionKwargs

if __name__ == "__main__":

    for kwargs in ConnectionKwargs:
        setup = DBSetup(**kwargs.value)
        setup.run()
