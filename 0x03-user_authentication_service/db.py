#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the DB
        """
        db_session = self._session
        new_user: User = User(email=email, hashed_password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    # BEFORE COMMITTING GO BACK TO THE TOP AND CHANGE
    # sqlalchemy.exc to sqlalchemy.orm.exc

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user based on keyword arguments
        """
        db_session = self._session
        raw_columns = User.__table__.columns
        columns = [str(field).split('.')[1] for field in raw_columns]
        for i in kwargs:
            if i not in columns:
                raise InvalidRequestError
        user: User = db_session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> User:
        """ Updates a user specified by user_id
        """
        db_session = self._session
        user = db_session.query(User).filter_by(id=user_id).first()
        for key, value in kwargs.items():
            setattr(user, key, value)
        db_session.commit()
