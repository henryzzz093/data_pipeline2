from database.models.util import DBSetup
from database.constants import ConnectionKwargs

if __name__ == "__main__":

    for conn_kwargs in ConnectionKwargs:
        print(conn_kwargs)
        setup = DBSetup(**conn_kwargs.value)
        setup.run()
