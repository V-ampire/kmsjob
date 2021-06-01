\connect :DB_NAME
CREATE INDEX vacancy_idx ON vacancy USING GIN (to_tsvector('russian', name || ' ' || employer || ' ' || description));