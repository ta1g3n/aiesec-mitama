from mitama.db import BaseDatabase, relationship
from mitama.db.types import (
    Column,
    String,
    ForeignKey,
    Date,
    Integer,
    Text,
    LargeBinary
)

from mitama.models import Group


class Database(BaseDatabase):
    pass


TEL = 0
TWITTER = 1
LINE = 2
FACEBOOK = 3
LINKEDIN = 4

CONTACT_OPTION_TYPES = {
    TWITTER: "Twitter",
    LINE: "LINE",
    FACEBOOK: "Facebook",
    LINKEDIN: "LinkedIn",
    TEL: "電話、SMS",
}

LCP = 0
OGXD = 110
OGXML = 111
OGXPL = 112
OGXM = 113
ICXD = 120
ICXML = 121
ICXPL = 122
ICXM = 123
PDD = 130
PDML = 131
PDPL = 132
PDM = 133
EWAD = 140
EWAML = 141
EWAPL = 142
EWAM = 143
BOD = 200
BOM = 201
FD = 210
FM = 211
BDD = 220
BDM = 221
TMD = 230
TMM = 231
BCXPD = 240
BCXPM = 241
MC = 300
TEAM_LEADER = 400
TEAM_MEMBER = 401
EC = 500
OTHER = 1000

CARRER_TYPES = {
    LCP: "LCP - 委員長",
    "OGX - 送り出し事業部": {
        OGXD: "OGX Director - 統括",
        OGXPL: "OGX PL - プロジェクトリーダー",
        OGXM: "OGX Member - メンバー",
    },
    "ICX - 受け入れ事業部": {
        ICXD: "ICX Director - 統括",
        ICXPL: "ICX PL - プロジェクトリーダー",
        ICXM: "ICX Member - メンバー",
    },
    "F - 財務局": {
        FD: "F Director - 統括",
        FM: "F Member - メンバー",
    },
    "BD - 外部関係局": {
        BDD: "BD Director - 統括",
        BDM: "BD Member - メンバー",
    },
    "TM - 人事局": {
        TMD: "TM Director - 統括",
        TMM: "TM Member - メンバー",
    },
    "BCXP - 広報ブランド局": {
        BCXPD: "BCXP Director - 統括",
        BCXPM: "BCXP Member - メンバー",
    },
    "その他バックオフィス": {
        BOD: "BackOffice Director - 統括",
        BOM: "BackOffice Member - メンバー",
    },
    MC: "MC - 事務局",
    EC: "EC - 選挙管理委員会",
    TEAM_LEADER: "チームリーダー",
    TEAM_MEMBER: "チームメンバー",
    OTHER: "その他",
}

CARRER_TYPES_FLAT = dict()

for k, v in CARRER_TYPES.items():
    if isinstance(v, dict):
        for k_, v_ in v.items():
            CARRER_TYPES_FLAT[k_] = v_
    else:
        CARRER_TYPES_FLAT[k] = v


db = Database(prefix="alumni_index")


class Profile(db.Model):
    name = Column(String(255))
    ruby = Column(String(255))
    epoch = Column(Integer)
    image = Column(LargeBinary)
    email = Column(String(255))
    contactOption = Column(Integer)
    contactIdent = Column(String(255))


class Career(db.Model):
    profile = relationship(Profile, backref='careers')
    profile_id = Column(String(64), ForeignKey("alumni_index_profile._id"))
    grade = Column(Integer)
    career = Column(Integer)


class TravelHistory(db.Model):
    profile = relationship(Profile, backref='travel_histories')
    profile_id = Column(String(64), ForeignKey("alumni_index_profile._id"))
    year = Column(Integer)
    span = Column(Integer)
    place = Column(String(64))
    description = Column(Text)


class ExtraColumn(db.Model):
    name = Column(String(255))


class ExtraColumnValue(db.Model):
    column_id = Column(String(64), ForeignKey("alumni_index_extra_column._id"))
    profile_id = Column(String(64), ForeignKey("alumni_index_profile._id"))
    column = relationship("ExtraColumn")
    profile = relationship("Profile", backref="extra")
    value = Column(String(255))


class Bd(db.Model):
    group_id = Column(String(64), ForeignKey("mitama_group._id"))
    group = relationship(Group)

    @classmethod
    def is_bd(cls, user):
        for group in user.groups:
            try:
                cls.retrieve(group=group)
                return True
            except Exception:
                continue
        return False


db.create_all()
