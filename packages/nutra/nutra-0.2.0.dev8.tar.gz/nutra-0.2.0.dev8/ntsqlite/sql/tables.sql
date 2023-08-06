-- nt-sqlite, an sqlite3 database for nutratracker clients
-- Copyright (C) 2020  Shane Jaroch <nutratracker@gmail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

CREATE TABLE version( id integer PRIMARY KEY AUTOINCREMENT, version text NOT NULL, created date NOT NULL, notes text
);

INSERT INTO version(version, created, notes)
  VALUES ('0.0.0', '2020-09-22', 'initial release');

--
---------------------------------
-- Equations
---------------------------------

CREATE TABLE bmr_eqs (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

CREATE TABLE bf_eqs (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

--
--------------------------------
-- Profiles table
--------------------------------

CREATE TABLE profiles (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL UNIQUE,
  guid text NOT NULL DEFAULT (lower(hex (randomblob (16)))) UNIQUE,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  eula int DEFAULT 0,
  gender text,
  dob date,
  act_lvl int DEFAULT 2, -- [1, 2, 3, 4, 5]
  goal_wt real,
  goal_bf real,
  bmr_eq_id int DEFAULT 1,
  bf_eq_id int DEFAULT 1,
  FOREIGN KEY (bmr_eq_id) REFERENCES bmr_eqs (id) ON UPDATE CASCADE,
  FOREIGN KEY (bf_eq_id) REFERENCES bf_eqs (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Biometrics
--------------------------------

CREATE TABLE biometrics (
  -- TODO: support custom biometrics and sync?
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL UNIQUE,
  unit text,
  created int DEFAULT (strftime ('%s', 'now'))
);

CREATE TABLE biometric_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  guid text NOT NULL DEFAULT (lower(hex (randomblob (16)))) UNIQUE,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  date int DEFAULT (strftime ('%s', 'now')),
  tags text,
  notes text,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE
);

CREATE TABLE bio_log_entry (
  log_id int NOT NULL,
  biometric_id int NOT NULL,
  value real NOT NULL,
  PRIMARY KEY (log_id, biometric_id),
  FOREIGN KEY (log_id) REFERENCES biometric_log (id) ON UPDATE CASCADE,
  FOREIGN KEY (biometric_id) REFERENCES biometrics (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Recipes
--------------------------------

CREATE TABLE recipes (
  id integer PRIMARY KEY AUTOINCREMENT,
  guid text NOT NULL DEFAULT (lower(hex (randomblob (16)))) UNIQUE,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  name text NOT NULL
);

CREATE TABLE recipe_dat (
  recipe_id int NOT NULL,
  -- TODO: enforce FK constraint across two DBs?
  food_id int NOT NULL,
  grams real NOT NULL,
  notes text,
  PRIMARY KEY (recipe_id, food_id),
  FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Food (and recipe) logs
--------------------------------

CREATE TABLE meals (
  -- predefined, includes standard three, snacks, brunch, and 3 optional/extra meals
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

CREATE TABLE food_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  guid text NOT NULL DEFAULT (lower(hex (randomblob (16)))) UNIQUE,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  date date DEFAULT CURRENT_DATE,
  meal_id int NOT NULL,
  food_id int NOT NULL, -- TODO: enforce FK constraint across two DBs?
  grams real NOT NULL,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE,
  FOREIGN KEY (meal_id) REFERENCES meals (id) ON UPDATE CASCADE
);

CREATE TABLE recipe_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  guid text NOT NULL DEFAULT (lower(hex (randomblob (16)))) UNIQUE,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  date date DEFAULT CURRENT_DATE,
  meal_id int NOT NULL,
  recipe_id int NOT NULL,
  grams real NOT NULL,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE,
  FOREIGN KEY (meal_id) REFERENCES meals (id) ON UPDATE CASCADE,
  FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Custom RDAs
--------------------------------

CREATE TABLE rda (
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  last_sync int DEFAULT - 1,
  -- TODO: enforce FK constraint across two DBs?
  nutr_id int NOT NULL,
  rda real NOT NULL,
  PRIMARY KEY (profile_id, nutr_id),
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE
);

