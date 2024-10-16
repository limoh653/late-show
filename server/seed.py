from app import app, db
from models import Episode, Guest, Appearance

# Make sure everything is done within an application context
with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create sample Episodes (10 entries)
    episodes = [
        Episode(date=f'2024-01-{i+1:02d}', number=100 + i) for i in range(10)
    ]

    # Create sample Guests (10 entries)
    guest_names = [
        'Michael J. Fox', 'Sandra Bernhard', 'Tom Hanks', 'Robin Williams', 'Eddie Murphy',
        'Meryl Streep', 'Will Smith', 'Jennifer Aniston', 'Chris Rock', 'Julia Roberts'
    ]
    guest_occupations = [
        'Actor', 'Comedian', 'Actor', 'Actor', 'Comedian', 
        'Actress', 'Actor', 'Actress', 'Comedian', 'Actress'
    ]
    guests = [
        Guest(name=guest_names[i], occupation=guest_occupations[i]) for i in range(10)
    ]

    # Create sample Appearances (10 entries with ratings between 1 and 5)
    appearances = [
        Appearance(rating=(i % 5) + 1, episode=episodes[i], guest=guests[i]) for i in range(10)
    ]

    # Add episodes, guests, and appearances to the session
    db.session.add_all(episodes)
    db.session.add_all(guests)
    db.session.add_all(appearances)

    # Commit the session to save everything to the database
    db.session.commit()

    print("Database seeded successfully with 10 episodes, 10 guests, and 10 appearances!")
