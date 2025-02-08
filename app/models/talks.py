import sqlalchemy as s

from app.extensions import db


class Talks(db.Model):
    talk_id = s.Column(s.Integer, primary_key=True)

    fk_event_id = s.Column(s.Integer, s.ForeignKey("events.event_id"))

    title = s.Column(s.String(255))
    description = s.Column(s.String(255))

    rel_talk_resources = s.orm.relationship("TalkResources")
    rel_talk_speakers = s.orm.relationship("TalkSpeakers")

    @classmethod
    def get_by_id(cls, talk_id):
        se_ = s.select(cls).where(cls.talk_id == talk_id)
        re_ = db.session.execute(se_).scalars().first()
        return re_

    @classmethod
    def get_by_event_id(cls, event_id):
        se_ = s.select(cls).where(cls.fk_event_id == event_id)
        re_ = db.session.execute(se_).scalars().all()
        return re_

    @classmethod
    def create(cls, title, description, event_id):
        ins_ = (
            s.insert(cls)
            .values(
                title=title,
                description=description,
                fk_event_id=event_id,
            )
            .returning(cls)
        )
        re_ = db.session.execute(ins_).scalars().first()
        db.session.commit()
        return re_

    @classmethod
    def update(cls, talk_id, title=None, description=None):
        up_ = (
            s.update(cls)
            .where(cls.talk_id == talk_id)
            .values(
                title=title,
                description=description,
            )
        )
        db.session.execute(up_)
        db.session.commit()

    @classmethod
    def delete(cls, talk_id):
        from app.models import TalkResources, TalkSpeakers

        TalkResources.delete_by_talk_id(talk_id)
        TalkSpeakers.delete_by_talk_id(talk_id)

        de_ = s.delete(cls).where(cls.talk_id == talk_id)
        db.session.execute(de_)
        db.session.commit()
