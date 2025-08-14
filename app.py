from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


def find_event(event_id: int):
    for e in events:
        if e.id == event_id:
            return e
    return None


def next_id() -> int:
    return max((e.id for e in events), default=0) + 1



@app.route("/", methods=["GET"])
def index():
    """JSON welcome message at root."""
    return jsonify({"message": "Welcome to the Events API"}), 200


@app.route("/events", methods=["GET"])
def list_events():
    """Return all events as JSON array."""
    return jsonify([e.to_dict() for e in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    """
    Create a new event from JSON body.
    Requires: {"title": "<string>"}
    Returns: 201 Created with the new event JSON.
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "Missing required field: title"}), 400

    new_event = Event(next_id(), title)
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """
    Update the title of an existing event.
    Body: {"title": "<string>"}
    Returns: 200 OK with updated event JSON, or 404/400 on error.
    """
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "Missing required field: title"}), 400

    event.title = title
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete an event by id.
    Returns: 204 No Content on success, or 404 if not found.
    """
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)