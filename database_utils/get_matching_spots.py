MATCH_SQL = """
    SELECT slug
    FROM spots
    WHERE preferred_swell_direction @> %(swell_direction)s::numeric
      AND preferred_wind_direction @> %(wind_direction)s::numeric
      AND preferred_tide @> %(tide)s::tide_level
    ORDER BY slug
"""


def get_matching_spots(conn, swell_direction, wind_direction, tide):
    with conn.cursor() as cur:
        cur.execute(
            MATCH_SQL,
            {
                "swell_direction": swell_direction,
                "wind_direction": wind_direction,
                "tide": tide,
            },
        )
        return [row["slug"] for row in cur.fetchall()]
