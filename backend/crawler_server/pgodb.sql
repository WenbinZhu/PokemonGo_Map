CREATE TABLE POKEMON_MAP (
    encounter_id    DOUBLE PRECISION,
    expire          DOUBLE PRECISION,
    pokemon_id      INT,
    latitude        DOUBLE PRECISION,
    longitude      DOUBLE PRECISION,
    PRIMARY KEY (encounter_id)
);


CREATE INDEX expire_idx on POKEMON_MAP (expire);
CREATE INDEX pokemon_id_idx on POKEMON_MAP (pokemon_id);
CREATE INDEX latitude_idx on POKEMON_MAP (latitude);
CREATE INDEX longitude_idx on POKEMON_MAP (longitude);
