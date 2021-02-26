from mitama.db import BaseDatabase, relationship
from mitama.db.types import *

from mitama.models import Group


class Database(BaseDatabase):
    pass


TEL = 0
TWITTER = 1
LINE = 2
FACEBOOK = 3
LINKEDIN = 4

CONTACT_OPTION_TYPES = {
    TEL: "電話、SMS",
    TWITTER: "Twitter",
    LINE: "LINE",
    FACEBOOK: "Facebook",
    LINKEDIN: "LinkedIn"
}

LCP = 0
OGXEB = 110
OGXML = 111
OGXPL = 112
OGXM = 113
ICXEB = 120
ICXML = 121
ICXPL = 122
ICXM = 123
PDEB = 130
PDML = 131
PDPL = 132
PDM = 133
EWAEB = 140
EWAML = 141
EWAPL = 142
EWAM = 143
BO = 200

CARRER_TYPES = {
    LCP: "LCP",
    OGXEB: "OGX EB",
    OGXML: "OGX ML",
    OGXPL: "OGX PL",
    OGXM: "OGX Member",
    ICXEB: "ICX EB",
    ICXML: "ICX ML",
    ICXPL: "ICX PL",
    ICXM: "ICX Member",
    PDEB: "PD EB",
    PDML: "PD ML",
    PDPL: "PD PL",
    PDM: "PD Member",
    EWAEB: "EwA EB",
    EWAML: "EwA ML",
    EWAPL: "EwA PL",
    EWAM: "EwA Member",
    BO: "Back Office"
}

db = Database(prefix="alumni_index")

class Profile(db.Model):
    name = Column(String(255))
    ruby = Column(String(255))
    birthday = Column(Date)
    epoch = Column(Integer)
    career1 = Column(Integer)
    career2 = Column(Integer)
    career3 = Column(Integer)
    career4 = Column(Integer)
    image = Column(LargeBinary)
    email = Column(String(255))
    contactOption = Column(Integer)
    contactIdent = Column(String(255))

class ExtraColumn(db.Model):
    name = Column(String(255))

class ExtraColumnValue(db.Model):
    column_id = Column(String(64), ForeignKey("alumni_index_extra_column._id"))
    profile_id = Column(String(64), ForeignKey("alumni_index_profile._id"))
    column = relationship("ExtraColumn")
    profile = relationship("Profile", backref = "extra")
    value = Column(String(255))

class Bd(db.Model):
    group_id = Column(String(64), ForeignKey("mitama_group._id"))
    group = relationship(Group)
    @classmethod
    def is_bd(cls, user):
        for group in user.groups:
            try:
                cls.retrieve(group = group)
                return True
            except Exception:
                continue
        return False


db.create_all()
