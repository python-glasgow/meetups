import sqlalchemy as s

from app.extensions import db


class Workshops(db.Model):
    workshop_id = s.Column(s.Integer, primary_key=True)

    fk_event_id = s.Column(s.Integer, s.ForeignKey("events.event_id"))

    title = s.Column(s.String(255))
    description = s.Column(s.String)

    rel_workshop_resources = s.orm.relationship("WorkshopResources")
    rel_workshop_hosts = s.orm.relationship("WorkshopHosts")

    @classmethod
    def get_by_id(cls, workshop_id):
        se_ = s.select(cls).where(cls.workshop_id == workshop_id)
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
            s.insert(cls).values(
                fk_event_id=event_id,
                title=title,
                description=description,
            )
        ).returning(cls)
        re_ = db.session.execute(ins_).scalars().first()
        db.session.commit()
        return re_

    @classmethod
    def update(cls, workshop_id, title=None, description=None, hosts=None):
        up_ = (
            s.update(cls)
            .where(cls.workshop_id == workshop_id)
            .values(
                title=title,
                description=description,
            )
        )
        db.session.execute(up_)
        db.session.commit()

    @classmethod
    def delete(cls, workshop_id):
        from app.models import WorkshopResources, WorkshopHosts

        WorkshopResources.delete_by_workshop_id(workshop_id)
        WorkshopHosts.delete_by_workshop_id(workshop_id)

        de_ = s.delete(cls).where(cls.workshop_id == workshop_id)
        db.session.execute(de_)
        db.session.commit()
