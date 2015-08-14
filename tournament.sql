-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c vagrant;

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournament (
    id SERIAL PRIMARY KEY
);

CREATE TABLE players (
   id SERIAL PRIMARY KEY,
   name TEXT NOT NULL

);

CREATE TABLE playerTournament (
    id SERIAL PRIMARY KEY,
    player INTEGER REFERENCES players (id),
    tournament INTEGER REFERENCES tournament (id)
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    tournament INTEGER REFERENCES tournament (id),
    winner INTEGER REFERENCES players (id),
    loser INTEGER REFERENCES players (id)
);

