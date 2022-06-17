from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    PrimaryKeyConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    last_login = Column(DateTime, nullable=True)

    groups = relationship('Group', back_populates='owner', cascade='all, delete-orphan')
    group_membership = relationship('GroupMembership', back_populates='players', cascade='all, delete-orphan')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invite_code = Column(String, nullable=True)

    owner = relationship('User', back_populates='groups')

    def __repr__(self):
        return f'Group(id={self.id!r}, name={self.name!r}, owner={self.owner.username!r})'


class GroupMembership(Base):
    __tablename__ = 'group_membership'
    __table_args__ = (
        PrimaryKeyConstraint('group_id', 'user_id'),
    )

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, nullable=True, default='ACTIVE')


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Session:
    pass


class SessionParticipants:
    pass



