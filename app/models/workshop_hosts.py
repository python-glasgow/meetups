import sqlalchemy as s

from app.extensions import db


class WorkshopHosts(db.Model):
    workshop_host_id = s.Column(s.Integer, primary_key=True)

    fk_workshop_id = s.Column(s.Integer, s.ForeignKey("workshops.workshop_id"))

    name = s.Column(s.String, default="")
    bio = s.Column(s.String, default="")

    extra_field_one_label = s.Column(s.String, default="")
    extra_field_one_value = s.Column(s.String, default="")

    extra_field_two_label = s.Column(s.String, default="")
    extra_field_two_value = s.Column(s.String, default="")

    extra_field_three_label = s.Column(s.String, default="")
    extra_field_three_value = s.Column(s.String, default="")

    @classmethod
    def get_by_id(cls, workshop_host_id):
        se_ = s.select(cls).where(cls.workshop_host_id == workshop_host_id)
        re_ = db.session.execute(se_).scalars().first()
        return re_

    @classmethod
    def get_by_workshop_id(cls, workshop_id):
        se_ = s.select(cls).where(cls.fk_workshop_id == workshop_id)
        re_ = db.session.execute(se_).scalars().all()
        return re_

    @classmethod
    def create(
        cls,
        workshop_id,
        name,
        bio="",
        extra_field_one_label="",
        extra_field_one_value="",
        extra_field_two_label="",
        extra_field_two_value="",
        extra_field_three_label="",
        extra_field_three_value="",
    ):
        ins_ = (
            s.insert(cls)
            .values(
                fk_workshop_id=workshop_id,
                name=name,
                bio=bio,
                extra_field_one_label=extra_field_one_label,
                extra_field_one_value=extra_field_one_value,
                extra_field_two_label=extra_field_two_label,
                extra_field_two_value=extra_field_two_value,
                extra_field_three_label=extra_field_three_label,
                extra_field_three_value=extra_field_three_value,
            )
            .returning(cls)
        )
        re_ = db.session.execute(ins_).scalars().first()
        db.session.commit()
        return re_

    @classmethod
    def update(
        cls,
        workshop_host_id,
        name,
        bio="",
        extra_field_one_label="",
        extra_field_one_value="",
        extra_field_two_label="",
        extra_field_two_value="",
        extra_field_three_label="",
        extra_field_three_value="",
    ):
        up_ = (
            s.update(cls)
            .where(cls.workshop_host_id == workshop_host_id)
            .values(
                name=name,
                bio=bio,
                extra_field_one_label=extra_field_one_label,
                extra_field_one_value=extra_field_one_value,
                extra_field_two_label=extra_field_two_label,
                extra_field_two_value=extra_field_two_value,
                extra_field_three_label=extra_field_three_label,
                extra_field_three_value=extra_field_three_value,
            )
        )
        db.session.execute(up_)
        db.session.commit()

    @classmethod
    def delete(cls, workshop_host_id):
        de_ = s.delete(cls).where(cls.workshop_host_id == workshop_host_id)
        db.session.execute(de_)
        db.session.commit()

    @classmethod
    def delete_by_workshop_id(cls, workshop_id):
        de_ = s.delete(cls).where(cls.fk_workshop_id == workshop_id)
        db.session.execute(de_)
        db.session.commit()
