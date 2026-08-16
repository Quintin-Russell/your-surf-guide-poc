-- Structured spot data. Semantic/prose data (descriptions) lives in the
-- vector store, not here -- this table is the "hard filter" layer.

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- gives us gen_random_uuid()

-- Enum declaration order IS the sort order range types below rely on.
-- Adding a value later means ALTER TYPE ... ADD VALUE BEFORE/AFTER, not a free edit.
CREATE TYPE difficulty_level AS ENUM ('beginner', 'intermediate', 'advanced', 'kamikaze');
CREATE TYPE crowd_level AS ENUM ('no', 'sometimes', 'often');
CREATE TYPE wave_type_category AS ENUM ('beachbreak', 'barrel', 'pointbreak', 'performance', 'a-frame');
CREATE TYPE tide_level AS ENUM ('low', '1/4', 'mid', '3/4', 'high');

-- Range types built on the enums' declared order, e.g. '[advanced,kamikaze]'
-- or '[low,mid]' -- same @>/&& operators as numrange.
CREATE TYPE difficulty_range AS RANGE (subtype = difficulty_level);
CREATE TYPE tide_range AS RANGE (subtype = tide_level);

CREATE TABLE spots (
    id                          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name                        text NOT NULL UNIQUE,
    slug                        text NOT NULL UNIQUE, -- must match the info/<slug>.txt filename and the Chroma "source" metadata

    latitude                    double precision NOT NULL,
    longitude                   double precision NOT NULL,
    city                        text NOT NULL,
    region                      text NOT NULL,
    country                     text NOT NULL,

    difficulty                  difficulty_range NOT NULL,
    bottom_material             text NOT NULL,
    wave_direction              text NOT NULL,
    wave_type                   wave_type_category NOT NULL,
    length_of_ride              numrange NOT NULL, -- length of ride in meters, e.g. '[50,75]'
    paddle_out                  text[] NOT NULL DEFAULT '{}',
    long_paddle                 boolean NOT NULL DEFAULT false,
    has_channel                 boolean NOT NULL DEFAULT false,
    crowded                     crowd_level NOT NULL,
    hazards                     text[] NOT NULL DEFAULT '{}',

    -- Compass degrees, 0-360. NOTE: numrange can't express a window that
    -- wraps past 360 back to 0 (e.g. 350-20). No wrap-around spots supported
    -- yet -- revisit (two ranges, or shift the domain) if one shows up.
    preferred_swell_direction   numrange NOT NULL,
    preferred_wind_direction    numrange NOT NULL,

    preferred_tide               tide_range NOT NULL,
    likes_glassy                boolean NOT NULL DEFAULT false,

    created_at                  timestamptz NOT NULL DEFAULT now(),
    updated_at                  timestamptz NOT NULL DEFAULT now()
);

-- Reject wrap-around ranges outright rather than silently storing garbage.
ALTER TABLE spots ADD CONSTRAINT preferred_swell_direction_no_wrap
    CHECK (lower(preferred_swell_direction) <= upper(preferred_swell_direction));
ALTER TABLE spots ADD CONSTRAINT preferred_wind_direction_no_wrap
    CHECK (lower(preferred_wind_direction) <= upper(preferred_wind_direction));

-- GiST indexes make "does X fall in this range" queries fast (@> operator)
-- instead of scanning every row -- matters once spot count grows.
CREATE INDEX idx_spots_swell_direction ON spots USING gist (preferred_swell_direction);
CREATE INDEX idx_spots_wind_direction ON spots USING gist (preferred_wind_direction);
CREATE INDEX idx_spots_difficulty ON spots USING gist (difficulty);
CREATE INDEX idx_spots_tide ON spots USING gist (preferred_tide);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_spots_updated_at
    BEFORE UPDATE ON spots
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
