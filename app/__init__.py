from datetime import datetime
from pathlib import Path
from urllib import request

from flask import Flask, render_template, request, redirect, url_for

from app.extensions import db
from app.models import (
    Events,
    Talks,
    Workshops,
    TalkResources,
    WorkshopResources,
    TalkSpeakers,
    WorkshopHosts,
)
from app.services import ArchiveJson


def create_app():
    app = Flask(__name__)
    app.static_folder = "static"
    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        events = Events.get_all()
        return render_template("index.html", events=events)

    # EVENTS

    @app.get("/event/create")
    def event_create_get():
        return render_template("event-create.html")

    @app.post("/event/create")
    def event_create_post():
        from app.models import Events

        title = request.form["title"]
        description = request.form["description"]
        datetime_ = request.form["datetime"]
        location = request.form["location"]

        if datetime_:
            datetime_ = datetime.strptime(datetime_, "%Y-%m-%dT%H:%M")
        else:
            datetime_ = None

        new_event = Events.create(
            title=title,
            description=description,
            datetime=datetime_,  # 2025-02-05T18:30
            location=location,
        )

        return redirect(url_for("event", event_id=new_event.event_id))

    @app.get("/event/<int:event_id>")
    def event(event_id: int):
        event_ = Events.get_by_id(event_id)
        return render_template("event.html", event=event_)

    @app.post("/event/<int:event_id>/update")
    def event_update(event_id):
        Events.update(
            event_id=event_id,
            title=request.form["title"],
            description=request.form["description"],
            datetime=request.form["datetime"],
            location=request.form["location"],
        )

        return redirect(url_for("event", event_id=event_id))

    @app.get("/event/<int:event_id>/delete")
    def event_delete(event_id):
        Events.delete(event_id)
        return redirect(url_for("index"))

    # TALKS

    @app.get("/event/<int:event_id>/talk/create")
    def talk_create_get(
        event_id: int,
    ):
        event_ = Events.get_by_id(event_id)
        return render_template("talk-create.html", event=event_)

    @app.post("/event/<int:event_id>/talk/create")
    def talk_create_post(
        event_id: int,
    ):
        title = request.form.get("title")
        description = request.form.get("description")

        new_talk = Talks.create(
            title=title,
            description=description,
            event_id=event_id,
        )

        return redirect(url_for("talk", event_id=event_id, talk_id=new_talk.talk_id))

    @app.get("/event/<int:event_id>/talk/<int:talk_id>")
    def talk(event_id: int, talk_id: int):
        event_ = Events.get_by_id(event_id)
        talk_ = Talks.get_by_id(talk_id)
        return render_template("talk.html", event=event_, talk=talk_)

    @app.post("/event/<int:event_id>/talk/<int:talk_id>/update")
    def talk_update(event_id: int, talk_id: int):
        title = request.form.get("title")
        description = request.form.get("description")
        Talks.update(
            talk_id=talk_id,
            title=title,
            description=description,
        )
        return redirect(url_for("talk", event_id=event_id, talk_id=talk_id))

    @app.get("/event/<int:event_id>/talk/<int:talk_id>/delete")
    def talk_delete(event_id: int, talk_id: int):
        Talks.delete(talk_id)
        return redirect(url_for("event", event_id=event_id))

    # TALK SPEAKERS

    @app.post("/fetch/talk/speakers")
    def fetch_talk_speakers():
        jsond = request.get_json()

        event_id = jsond["event_id"]
        talk_id = jsond["talk_id"]

        talk_speakers = TalkSpeakers.get_by_talk_id(talk_id)

        return {
            "event_id": event_id,
            "talk_id": talk_id,
            "talk_speakers": [
                {
                    "talk_speaker_id": r.talk_speaker_id,
                    "name": r.name,
                    "bio": r.bio,
                    "extra_field_one_label": r.extra_field_one_label,
                    "extra_field_one_value": r.extra_field_one_value,
                    "extra_field_two_label": r.extra_field_two_label,
                    "extra_field_two_value": r.extra_field_two_value,
                    "extra_field_three_label": r.extra_field_three_label,
                    "extra_field_three_value": r.extra_field_three_value,
                }
                for r in talk_speakers
            ],
        }

    @app.post("/fetch/talk/speakers/create")
    def fetch_talk_speakers_create():
        jsond = request.get_json()

        talk_id = jsond["talk_id"]
        name = jsond["name"]
        bio = jsond["bio"]
        extra_field_one_label = jsond["extra_field_one_label"]
        extra_field_one_value = jsond["extra_field_one_value"]
        extra_field_two_label = jsond["extra_field_two_label"]
        extra_field_two_value = jsond["extra_field_two_value"]
        extra_field_three_label = jsond["extra_field_three_label"]
        extra_field_three_value = jsond["extra_field_three_value"]

        new_talk_speaker = TalkSpeakers.create(
            talk_id=talk_id,
            name=name,
            bio=bio,
            extra_field_one_label=extra_field_one_label,
            extra_field_one_value=extra_field_one_value,
            extra_field_two_label=extra_field_two_label,
            extra_field_two_value=extra_field_two_value,
            extra_field_three_label=extra_field_three_label,
            extra_field_three_value=extra_field_three_value,
        )

        return {
            "talk_id": talk_id,
            "talk_speaker_id": new_talk_speaker.talk_speaker_id,
            "name": name,
            "bio": bio,
            "extra_field_one_label": extra_field_one_label,
            "extra_field_one_value": extra_field_one_value,
            "extra_field_two_label": extra_field_two_label,
            "extra_field_two_value": extra_field_two_value,
            "extra_field_three_label": extra_field_three_label,
            "extra_field_three_value": extra_field_three_value,
        }

    @app.post("/fetch/talk/speakers/update")
    def fetch_talk_speakers_update():
        jsond = request.get_json()

        talk_speaker_id = jsond["talk_speaker_id"]
        name = jsond["name"]
        bio = jsond["bio"]
        extra_field_one_label = jsond["extra_field_one_label"]
        extra_field_one_value = jsond["extra_field_one_value"]
        extra_field_two_label = jsond["extra_field_two_label"]
        extra_field_two_value = jsond["extra_field_two_value"]
        extra_field_three_label = jsond["extra_field_three_label"]
        extra_field_three_value = jsond["extra_field_three_value"]

        TalkSpeakers.update(
            talk_speaker_id=talk_speaker_id,
            name=name,
            bio=bio,
            extra_field_one_label=extra_field_one_label,
            extra_field_one_value=extra_field_one_value,
            extra_field_two_label=extra_field_two_label,
            extra_field_two_value=extra_field_two_value,
            extra_field_three_label=extra_field_three_label,
            extra_field_three_value=extra_field_three_value,
        )

        return {
            "talk_speaker_id": talk_speaker_id,
            "name": name,
            "bio": bio,
            "extra_field_one_label": extra_field_one_label,
            "extra_field_one_value": extra_field_one_value,
            "extra_field_two_label": extra_field_two_label,
            "extra_field_two_value": extra_field_two_value,
            "extra_field_three_label": extra_field_three_label,
            "extra_field_three_value": extra_field_three_value,
        }

    @app.post("/fetch/talk/speakers/delete")
    def fetch_talk_speakers_delete():
        jsond = request.get_json()

        talk_speaker_id = jsond["talk_speaker_id"]

        TalkSpeakers.delete(talk_speaker_id)

        return {
            "talk_speaker_id": talk_speaker_id,
        }

    # TALK RESOURCES

    @app.post("/fetch/talk/resources")
    def fetch_talk_resources():
        jsond = request.get_json()

        event_id = jsond["event_id"]
        talk_id = jsond["talk_id"]

        talk_resources = TalkResources.get_by_talk_id(talk_id)

        return {
            "event_id": event_id,
            "talk_id": talk_id,
            "talk_resources": [
                {
                    "talk_resource_id": r.talk_resource_id,
                    "type": r.type,
                    "source": r.source,
                }
                for r in talk_resources
            ],
        }

    @app.post("/fetch/talk/resources/create")
    def fetch_talk_resources_create():
        jsond = request.get_json()

        talk_id = jsond["talk_id"]
        type_ = jsond["type"]
        source = jsond["source"]

        new_talk_resource = TalkResources.create(
            talk_id=talk_id,
            type_=type_,
            source=source,
        )

        return {
            "talk_id": talk_id,
            "talk_resource_id": new_talk_resource.talk_resource_id,
            "type": type_,
            "source": source,
        }

    @app.post("/fetch/talk/resources/update")
    def fetch_talk_resources_update():
        jsond = request.get_json()

        talk_resource_id = jsond["talk_resource_id"]
        type_ = jsond["type"]
        source = jsond["source"]

        TalkResources.update(
            talk_resource_id=talk_resource_id,
            type_=type_,
            source=source,
        )

        return {
            "talk_resource_id": talk_resource_id,
            "type": type_,
            "source": source,
        }

    @app.post("/fetch/talk/resources/delete")
    def fetch_talk_resources_delete():
        jsond = request.get_json()

        talk_resource_id = jsond["talk_resource_id"]

        TalkResources.delete(talk_resource_id)

        return {
            "talk_resource_id": talk_resource_id,
        }

    # WORKSHOP

    @app.get("/event/<int:event_id>/workshop/create")
    def workshop_create_get(
        event_id: int,
    ):
        event_ = Events.get_by_id(event_id)
        return render_template("workshop-create.html", event=event_)

    @app.post("/event/<int:event_id>/workshop/create")
    def workshop_create_post(
        event_id: int,
    ):
        title = request.form.get("title")
        description = request.form.get("description")

        new_workshop = Workshops.create(
            title=title,
            description=description,
            event_id=event_id,
        )

        return redirect(
            url_for("workshop", event_id=event_id, workshop_id=new_workshop.workshop_id)
        )

    @app.get("/event/<int:event_id>/workshop/<int:workshop_id>")
    def workshop(event_id: int, workshop_id: int):
        event_ = Events.get_by_id(event_id)
        workshop_ = Workshops.get_by_id(workshop_id)
        return render_template("workshop.html", event=event_, workshop=workshop_)

    @app.post("/event/<int:event_id>/workshop/<int:workshop_id>/update")
    def workshop_update(event_id: int, workshop_id: int):
        title = request.form.get("title")
        description = request.form.get("description")
        hosts = request.form.get("hosts")

        Workshops.update(
            workshop_id=workshop_id,
            title=title,
            description=description,
            hosts=hosts,
        )

        return redirect(url_for("workshop", event_id=event_id, workshop_id=workshop_id))

    @app.get("/event/<int:event_id>/workshop/<int:workshop_id>/delete")
    def workshop_delete(event_id: int, workshop_id: int):
        Workshops.delete(workshop_id)
        return redirect(url_for("event", event_id=event_id))

    # WORKSHOP HOSTS

    @app.post("/fetch/workshop/hosts")
    def fetch_workshop_hosts():
        jsond = request.get_json()

        event_id = jsond["event_id"]
        workshop_id = jsond["workshop_id"]

        workshop_hosts = WorkshopHosts.get_by_workshop_id(workshop_id)

        return {
            "event_id": event_id,
            "workshop_id": workshop_id,
            "workshop_hosts": [
                {
                    "workshop_host_id": r.workshop_host_id,
                    "name": r.name,
                    "bio": r.bio,
                    "extra_field_one_label": r.extra_field_one_label,
                    "extra_field_one_value": r.extra_field_one_value,
                    "extra_field_two_label": r.extra_field_two_label,
                    "extra_field_two_value": r.extra_field_two_value,
                    "extra_field_three_label": r.extra_field_three_label,
                    "extra_field_three_value": r.extra_field_three_value,
                }
                for r in workshop_hosts
            ],
        }

    @app.post("/fetch/workshop/hosts/create")
    def fetch_workshop_hosts_create():
        jsond = request.get_json()

        workshop_id = jsond["workshop_id"]
        name = jsond["name"]
        bio = jsond["bio"]
        extra_field_one_label = jsond["extra_field_one_label"]
        extra_field_one_value = jsond["extra_field_one_value"]
        extra_field_two_label = jsond["extra_field_two_label"]
        extra_field_two_value = jsond["extra_field_two_value"]
        extra_field_three_label = jsond["extra_field_three_label"]
        extra_field_three_value = jsond["extra_field_three_value"]

        new_workshop_host = WorkshopHosts.create(
            workshop_id=workshop_id,
            name=name,
            bio=bio,
            extra_field_one_label=extra_field_one_label,
            extra_field_one_value=extra_field_one_value,
            extra_field_two_label=extra_field_two_label,
            extra_field_two_value=extra_field_two_value,
            extra_field_three_label=extra_field_three_label,
            extra_field_three_value=extra_field_three_value,
        )

        return {
            "workshop_id": workshop_id,
            "workshop_host_id": new_workshop_host.workshop_host_id,
            "name": name,
            "bio": bio,
            "extra_field_one_label": extra_field_one_label,
            "extra_field_one_value": extra_field_one_value,
            "extra_field_two_label": extra_field_two_label,
            "extra_field_two_value": extra_field_two_value,
            "extra_field_three_label": extra_field_three_label,
            "extra_field_three_value": extra_field_three_value,
        }

    @app.post("/fetch/workshop/hosts/update")
    def fetch_workshop_hosts_update():
        jsond = request.get_json()

        workshop_host_id = jsond["workshop_host_id"]
        name = jsond["name"]
        bio = jsond["bio"]
        extra_field_one_label = jsond["extra_field_one_label"]
        extra_field_one_value = jsond["extra_field_one_value"]
        extra_field_two_label = jsond["extra_field_two_label"]
        extra_field_two_value = jsond["extra_field_two_value"]
        extra_field_three_label = jsond["extra_field_three_label"]
        extra_field_three_value = jsond["extra_field_three_value"]

        WorkshopHosts.update(
            workshop_host_id=workshop_host_id,
            name=name,
            bio=bio,
            extra_field_one_label=extra_field_one_label,
            extra_field_one_value=extra_field_one_value,
            extra_field_two_label=extra_field_two_label,
            extra_field_two_value=extra_field_two_value,
            extra_field_three_label=extra_field_three_label,
            extra_field_three_value=extra_field_three_value,
        )

        return {
            "workshop_host_id": workshop_host_id,
            "name": name,
            "bio": bio,
            "extra_field_one_label": extra_field_one_label,
            "extra_field_one_value": extra_field_one_value,
            "extra_field_two_label": extra_field_two_label,
            "extra_field_two_value": extra_field_two_value,
            "extra_field_three_label": extra_field_three_label,
            "extra_field_three_value": extra_field_three_value,
        }

    @app.post("/fetch/workshop/hosts/delete")
    def fetch_workshop_hosts_delete():
        jsond = request.get_json()

        workshop_host_id = jsond["workshop_host_id"]

        WorkshopHosts.delete(workshop_host_id)

        return {
            "workshop_host_id": workshop_host_id,
        }

    # WORKSHOP RESOURCES

    @app.post("/fetch/workshop/resources")
    def fetch_workshop_resources():
        jsond = request.get_json()

        event_id = jsond["event_id"]
        workshop_id = jsond["workshop_id"]

        workshop_resources = WorkshopResources.get_by_workshop_id(workshop_id)

        return {
            "event_id": event_id,
            "workshop_id": workshop_id,
            "workshop_resources": [
                {
                    "workshop_resource_id": r.workshop_resource_id,
                    "type": r.type,
                    "source": r.source,
                }
                for r in workshop_resources
            ],
        }

    @app.post("/fetch/workshop/resources/create")
    def fetch_workshop_resources_create():
        jsond = request.get_json()

        workshop_id = jsond["workshop_id"]
        type_ = jsond["type"]
        source = jsond["source"]

        new_workshop_resource = WorkshopResources.create(
            workshop_id=workshop_id,
            type_=type_,
            source=source,
        )

        return {
            "workshop_id": workshop_id,
            "workshop_resource_id": new_workshop_resource.workshop_resource_id,
            "type": type_,
            "source": source,
        }

    @app.post("/fetch/workshop/resources/update")
    def fetch_workshop_resources_update():
        jsond = request.get_json()

        workshop_resource_id = jsond["workshop_resource_id"]
        type_ = jsond["type"]
        source = jsond["source"]

        WorkshopResources.update(
            workshop_resource_id,
            type_=type_,
            source=source,
        )

        return {
            "workshop_resource_id": workshop_resource_id,
            "type": type_,
            "source": source,
        }

    @app.post("/fetch/workshop/resources/delete")
    def fetch_workshop_resources_delete():
        jsond = request.get_json()

        workshop_resource_id = jsond["workshop_resource_id"]

        WorkshopResources.delete(workshop_resource_id)

        return {
            "workshop_resource_id": workshop_resource_id,
        }

    @app.get("/write-to-archive")
    def write_to_archive():
        events = Events.get_all()
        archive_ = {
            "name": "The Python Glasgow Meetup Archive",
            "version": "1.0.0",
            "events": [
                {
                    "event_id": event_.event_id,
                    "title": event_.title,
                    "description": event_.description,
                    "datetime": event_.datetime.strftime("%Y-%m-%dT%H:%M"),
                    "location": event_.location,
                    "talks": [
                        {
                            "talk_id": talk_.talk_id,
                            "title": talk_.title,
                            "description": talk_.description,
                            "speakers": [
                                {
                                    "talk_speaker_id": s.talk_speaker_id,
                                    "name": s.name,
                                    "bio": s.bio,
                                    "extra_field_one_label": s.extra_field_one_label,
                                    "extra_field_one_value": s.extra_field_one_value,
                                    "extra_field_two_label": s.extra_field_two_label,
                                    "extra_field_two_value": s.extra_field_two_value,
                                    "extra_field_three_label": s.extra_field_three_label,
                                    "extra_field_three_value": s.extra_field_three_value,
                                }
                                for s in talk_.rel_talk_speakers
                            ],
                            "resources": [
                                {
                                    "talk_resource_id": r.talk_resource_id,
                                    "type": r.type,
                                    "source": r.source,
                                }
                                for r in talk_.rel_talk_resources
                            ],
                        }
                        for talk_ in event_.rel_talks
                    ],
                    "workshops": [
                        {
                            "workshop_id": workshop_.workshop_id,
                            "title": workshop_.title,
                            "description": workshop_.description,
                            "hosts": [
                                {
                                    "workshop_host_id": h.workshop_host_id,
                                    "name": h.name,
                                    "bio": h.bio,
                                    "extra_field_one_label": h.extra_field_one_label,
                                    "extra_field_one_value": h.extra_field_one_value,
                                    "extra_field_two_label": h.extra_field_two_label,
                                    "extra_field_two_value": h.extra_field_two_value,
                                    "extra_field_three_label": h.extra_field_three_label,
                                    "extra_field_three_value": h.extra_field_three_value,
                                }
                                for h in workshop_.rel_workshop_hosts
                            ],
                            "resources": [
                                {
                                    "workshop_resource_id": r.workshop_resource_id,
                                    "type": r.type,
                                    "source": r.source,
                                }
                                for r in workshop_.rel_workshop_resources
                            ],
                        }
                        for workshop_ in event_.rel_workshops
                    ],
                }
                for event_ in events
            ],
        }

        archive_file = ArchiveJson(Path(app.root_path).parent / "archive.json")
        archive_file.update(archive_)

        return redirect(url_for("index"))

    return app
