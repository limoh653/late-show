from flask import request, session,jsonify
from flask_restful import Resource

from config import app, db, api
from models import Episode,Appearance,Guest

# Route to get all episodes
@app.route('/episodes',methods=['GET'])
def get_episodes():
    
    # Query all episodes from the database
    episodes=Episode.query.all()

    episodes_list=[episode.to_dict()for episode in episodes]

    return jsonify(episodes_list),200

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    # Query the episode by ID, including the appearances
    episode = Episode.query.filter(Episode.id == id).first()

    # Check if the episode exists
    if episode is None:
        return jsonify({"error": "Episode not found"}), 404

    episode_data = {
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [
            {
                "id": appearance.id,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                },
                "rating": appearance.rating
            }
            for appearance in episode.appearance
        ]
    }

    return jsonify(episode_data), 200

@app.route('/guests', methods=['GET'])
def get_guests():
    # Query all guests from the database
    guests = Guest.query.all()

    # Manually build a list of dictionaries
    guests_list = [
        {
            'id': guest.id,
            'name': guest.name,
            'occupation': guest.occupation
        }
        for guest in guests
    ]

    # Return the list as JSON
    return jsonify(guests_list), 200

@app.route('/appearances', methods=['POST'])
def create_appearance():
    # Extract the request data
    data = request.get_json()

    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    # Validate the data (rating should be between 1 and 5, and episode_id and guest_id must be present)
    if not rating or not (1 <= rating <= 5):
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

    if not episode_id or not guest_id:
        return jsonify({"errors": ["Both episode_id and guest_id are required"]}), 400

    episode = Episode.query.get(episode_id)
    guest = Guest.query.get(guest_id)

    if not episode or not guest:
        return jsonify({"errors": ["Episode or Guest not found"]}), 404

        # Create a new Appearance instance
    new_appearance = Appearance(
        rating=rating,
        episode_id=episode_id,
        guest_id=guest_id
        )

        # Add and commit the new appearance to the database
    db.session.add(new_appearance)
    db.session.commit()

        # Format the response data
    response_data = {
        "id": new_appearance.id,
        "rating": new_appearance.rating,
        "guest_id": new_appearance.guest_id,
        "episode_id": new_appearance.episode_id,
        "episode": {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }
    return jsonify(response_data), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)

   