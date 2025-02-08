import sqlalchemy as s

from app.extensions import db


class Events(db.Model):
    event_id = s.Column(s.Integer, primary_key=True)

    title = s.Column(s.String(255))
    description = s.Column(s.String)
    datetime = s.Column(s.DateTime)
    location = s.Column(s.String(255))

    rel_workshops = s.orm.relationship("Workshops")
    rel_talks = s.orm.relationship("Talks")

    @classmethod
    def get_all(cls):
        se_ = s.select(cls).order_by(cls.datetime)
        re_ = db.session.execute(se_).scalars().all()
        return re_

    @classmethod
    def get_by_id(cls, event_id):
        se_ = s.select(cls).where(cls.event_id == event_id)
        re_ = db.session.execute(se_).scalars().first()
        return re_

    @classmethod
    def create(cls, title, description, datetime, location):
        ins_ = (
            s.insert(cls)
            .values(
                title=title,
                description=description,
                datetime=datetime,
                location=location,
            )
            .returning(cls)
        )
        re_ = db.session.execute(ins_).scalars().first()
        db.session.commit()
        return re_

    @classmethod
    def update(
        cls, event_id, title=None, description=None, datetime=None, location=None
    ):
        up_ = (
            s.update(cls)
            .where(cls.event_id == event_id)
            .values(
                title=title,
                description=description,
                datetime=datetime,
                location=location,
            )
        )
        db.session.execute(up_)
        db.session.commit()

    @classmethod
    def delete(cls, event_id):
        from app.models import Talks, Workshops

        select_talks = s.select(Talks).where(Talks.fk_event_id == event_id)
        talks = db.session.execute(select_talks).scalars().all()
        for talk in talks:
            Talks.delete(talk.talk_id)

        select_workshops = s.select(Workshops).where(Workshops.fk_event_id == event_id)
        workshops = db.session.execute(select_workshops).scalars().all()
        for workshop in workshops:
            Workshops.delete(workshop.workshop_id)

        de_ = s.delete(cls).where(cls.event_id == event_id)
        db.session.execute(de_)
        db.session.commit()
