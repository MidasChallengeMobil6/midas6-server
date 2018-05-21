from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, ENUM
from app import db

status_enums = ["active", "block", "hidden"]

class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )

    name = db.Column(
        VARCHAR(128)
    )


    username = db.Column(
        VARCHAR(128),
        unique=True
    )

    email = db.Column(
        VARCHAR(128)
    )


    password = db.Column(
        VARCHAR(128)
    )

    joinDate = db.Column(
        DATETIME()
    )

    status = db.Column(
        ENUM(*status_enums),
        default=status_enums[0],
        server_default=status_enums[0]
    )