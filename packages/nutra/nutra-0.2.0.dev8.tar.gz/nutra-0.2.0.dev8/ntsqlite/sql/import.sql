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

PRAGMA foreign_keys = 1;
-- PRAGMA integrity_check = 1;


.mode csv
-- .nullvalue NULL

.import '| tail -n +2 ./data/bmr_eqs.csv' bmr_eqs
.import '| tail -n +2 ./data/bf_eqs.csv' bf_eqs
.import '| tail -n +2 ./data/meals.csv' meals

.import '| tail -n +2 ./data/biometrics.csv' biometrics
.import '| tail -n +2 ./data/profiles.csv' profiles
.import '| tail -n +2 ./data/rda.csv' rda

.import '| tail -n +2 ./data/recipes.csv' recipes
.import '| tail -n +2 ./data/recipe_dat.csv' recipe_dat

.import '| tail -n +2 ./data/food_log.csv' food_log
.import '| tail -n +2 ./data/recipe_log.csv' recipe_log

.import '| tail -n +2 ./data/biometric_log.csv' biometric_log
.import '| tail -n +2 ./data/bio_log_entry.csv' bio_log_entry

.header on
.mode column
