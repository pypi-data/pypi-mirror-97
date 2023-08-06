# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, Dict

# Pip
from firebase_admin import db, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.db import Reference

from jsoncodable import JSONCodable
from noraise import noraise

# Local
from .types import JSONData

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: FirebaseRealtimeDB ------------------------------------------------------ #

class FirebaseRealtimeDB:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @staticmethod
    def initialize(
        certificate_path: str,
        database_url: str
    ) -> None:
        initialize_app(
            Certificate(certificate_path),
            {
                'databaseURL': database_url
            }
        )


    @classmethod
    def exists(
        cls,
        path: str
    ) -> bool:
        return cls.get(path, shallow=True) is not None

    @classmethod
    @noraise()
    def get(
        cls,
        path: str,
        shallow: bool = False
    ) -> Optional[JSONData]:
        return cls.__ref(path).get(shallow=shallow)

    @classmethod
    @noraise(default_return_value=False)
    def set(
        cls,
        data: Union[JSONCodable, JSONData],
        path: str
    ) -> bool:
        ref = cls.__ref(path)

        if isinstance(data, JSONCodable):
            data = data.json

        ref.set(data)

        return True

    @classmethod
    @noraise(default_return_value=False)
    def delete(
        cls,
        path: str
    ) -> bool:
        cls.__ref(path).delete()

        return True


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __ref(
        path: str = ''
    ) -> Reference:
        return db.reference('/{}'.format(path.strip('/')))


# ---------------------------------------------------------------------------------------------------------------------------------------- #