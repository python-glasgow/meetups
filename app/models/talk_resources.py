import sqlalchemy as s

from app.extensions import db


class TalkResources(db.Model):
    talk_resource_id = s.Column(s.Integer, primary_key=True)

    fk_talk_id = s.Column(s.Integer, s.ForeignKey("talks.talk_id"))

    type = s.Column(s.String(30))
    source = s.Column(s.String)

    @classmethod
    def get_by_id(cls, talk_resource_id):
        se_ = s.select(cls).where(cls.talk_resource_id == talk_resource_id)
        re_ = db.session.execute(se_).scalars().first()
        return re_

    @classmethod
    def get_by_talk_id(cls, talk_id):
        se_ = s.select(cls).where(cls.fk_talk_id == talk_id)
        re_ = db.session.execute(se_).scalars().all()
        return re_

    @classmethod
    def create(cls, type_, source, talk_id):
        ins_ = (
            s.insert(cls)
            .values(
                fk_talk_id=talk_id,
                type=type_,
                source=source,
            )
            .returning(cls)
        )
        re_ = db.session.execute(ins_).scalars().first()
        db.session.commit()
        return re_

    @classmethod
    def update(cls, talk_resource_id, type_=None, source=None):
        up_ = (
            s.update(cls)
            .where(cls.talk_resource_id == talk_resource_id)
            .values(
                type=type_,
                source=source,
            )
        )
        db.session.execute(up_)
        db.session.commit()

    @classmethod
    def delete(cls, talk_resource_id):
        de_ = s.delete(cls).where(cls.talk_resource_id == talk_resource_id)
        db.session.execute(de_)
        db.session.commit()

    @classmethod
    def delete_by_talk_id(cls, talk_id):
        de_ = s.delete(cls).where(cls.fk_talk_id == talk_id)
        db.session.execute(de_)
        db.session.commit()
