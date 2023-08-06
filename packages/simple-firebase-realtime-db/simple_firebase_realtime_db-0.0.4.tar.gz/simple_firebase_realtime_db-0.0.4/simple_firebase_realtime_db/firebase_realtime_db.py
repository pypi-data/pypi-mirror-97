# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, List, Dict, Callable, Hashable

# Pip
from firebase_admin import db, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.db import Reference, ListenerRegistration, Event, Query

from jsoncodable import JSONCodable
from noraise import noraise

# Local
from .types import JSONData

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: FirebaseRealtimeDB ------------------------------------------------------ #

class FirebaseRealtimeDB:

    # ---------------------------------------------------------- Initialize ---------------------------------------------------------- #

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


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

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
        return cls.ref(path).get(shallow=shallow)

    @classmethod
    @noraise(default_return_value=False)
    def set(
        cls,
        data: Union[JSONCodable, JSONData],
        path: str
    ) -> bool:
        cls.ref(path).set(cls.__get_json_data(data))

        return True

    @classmethod
    @noraise(default_return_value=False)
    def update(
        cls,
        data: Dict[str, Union[JSONCodable, JSONData]],
        path: str
    ) -> bool:
        cls.ref(path).update({ k:cls.__get_json_data(v) for k, v in data.items() })

        return True

    @classmethod
    @noraise()
    def listen(
        cls,
        callback: Callable[[Event], None],
        path: str
    ) -> Optional[ListenerRegistration]:
        return cls.ref(path).listen(callback)

    @classmethod
    @noraise()
    def transaction(
        cls,
        update_callback: Callable[[JSONData], Union[JSONCodable, JSONData]],
        path: str
    ) -> Optional[JSONData]:
        @noraise()
        def __update_callback(old_value: JSONData) -> JSONData:
            return cls.__get_json_data(update_callback(old_value))

        return cls.ref(path).transaction(__update_callback)

    @classmethod
    @noraise()
    def query(
        cls,
        path: str,
        where: str,
        equals_to: Hashable
    ) -> List[JSONData]:
        return cls.ref(path).order_by_child(where).equal_to(equals_to).get()

    @classmethod
    @noraise(default_return_value=False)
    def delete(
        cls,
        path: str
    ) -> bool:
        cls.ref(path).delete()

        return True

    @staticmethod
    def ref(
        path: Optional[str] = None
    ) -> Reference:
        path = path or ''

        return db.reference('/{}'.format(path.strip('/')))


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __get_json_data(value: Union[JSONCodable, JSONData]) -> JSONData:
        return value.json if isinstance(value, JSONCodable) else value


# ---------------------------------------------------------------------------------------------------------------------------------------- #