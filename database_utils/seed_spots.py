from dotenv import load_dotenv

from database_utils.postgres_client import create_postgres_client

SPOTS = [
    {
        "name": "Jimmy's",
        "slug": "jimmys",
        "latitude": -5.008847,
        "longitude": 103.743860,
        "city": "Krui",
        "region": "South Sumatra",
        "country": "Indonesia",
        "difficulty": "[advanced,kamikaze]",
        "bottom_material": "reef",
        "wave_direction": "right",
        "wave_type": "barrel",
        "length_of_ride": "[50,100]",
        "paddle_out": ["jetty"],
        "long_paddle": False,
        "has_channel": True,
        "crowded": "sometimes",
        "hazards": ["close-outs", "shallow reef", "powerful waves"],
        "preferred_swell_direction": "[210,225]",
        "preferred_wind_direction": "[210,280]",
        "preferred_tide": "[high,high]",
        "likes_glassy": True,
    },
    {
        "name": "The Peak",
        "slug": "the_peak",
        "latitude": -5.203105,
        "longitude": 103.919097,
        "city": "Krui",
        "region": "South Sumatra",
        "country": "Indonesia",
        "difficulty": "[advanced,advanced]",
        "bottom_material": "reef",
        "wave_direction": "A-frame; mostly a right",
        "wave_type": "barrel",
        "length_of_ride": "[25,50]",
        "paddle_out": ["beach"],
        "long_paddle": False,
        "has_channel": True,
        "crowded": "often",
        "hazards": ["shallow reef", "urchins"],
        "preferred_swell_direction": "[180,210]",
        "preferred_wind_direction": "[130,160]",
        "preferred_tide": "[low,mid]",
        "likes_glassy": False,
    },
]

INSERT_SQL = """
    INSERT INTO spots (
        name, slug, latitude, longitude, city, region, country,
        difficulty, bottom_material, wave_direction, wave_type, length_of_ride,
        paddle_out, long_paddle, has_channel, crowded, hazards,
        preferred_swell_direction, preferred_wind_direction, preferred_tide, likes_glassy
    ) VALUES (
        %(name)s, %(slug)s, %(latitude)s, %(longitude)s, %(city)s, %(region)s, %(country)s,
        %(difficulty)s::difficulty_range, %(bottom_material)s, %(wave_direction)s,
        %(wave_type)s::wave_type_category, %(length_of_ride)s::numrange,
        %(paddle_out)s, %(long_paddle)s, %(has_channel)s, %(crowded)s::crowd_level, %(hazards)s,
        %(preferred_swell_direction)s::numrange, %(preferred_wind_direction)s::numrange,
        %(preferred_tide)s::tide_range, %(likes_glassy)s
    )
    ON CONFLICT (name) DO NOTHING
"""


def seed_spots():
    conn = create_postgres_client()
    with conn.cursor() as cur:
        for spot in SPOTS:
            cur.execute(INSERT_SQL, spot)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_dotenv()
    seed_spots()
    print(f"Seeded {len(SPOTS)} spots")
