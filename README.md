# Instructions

Download all of these files from
https://drive.google.com/drive/folders/1hfoggzv6fiiOcrr0wmb0d620AY1ILI5L

- `00_traits.txt`

- `01_traits.txt`

- `02_traits.txt`

- `03_traits.txt`

- `00_dynasties.txt`

- `00_religions.txt`

- `00_cultures.txt`

- `province_id to county_id.txt`

- `Leon1067_02_12.ck2` - This is the standard dataset. Does not contain any bloodlines.

- `bloodlines.ck2` - Alternative dataset that contains bloodlines. This would need to be passed to the `load_data.py` as a parameter (i.e. `python load_data.py bloodlines.ck2`)

As superuser `postgres` in psql, run `ck2_setup.py` to create the ck2 database.
This will also create the user `charles` with password `frank`.

Now, run `load_data.py` to load the data from the `Leon1067_02_12.ck2` file by default. You can optionally add the name of a different `.ck2` file to load into the database, as opposed to the default. This file should take around 60 seconds to run.



# Relation Meanings

barony
bloodlineowners
bloodlines
culture
claim
dynasty 
marriage
person
province
religion
title
trait
traitlookup

# Basic Queries

```pgsql
-- Query for getting all of the traits of noble people
SELECT birthname, dynastyname, traitname 
FROM person NATURAL JOIN dynasty NATURAL JOIN trait NATURAL JOIN traitlookup;
```

```pgsql
-- Query for getting noble people and their titles.
SELECT birthname, dynastyname, name as title, level
FROM (
  	SELECT personid AS holderid, birthname, dynastyname 
 		FROM person NATURAL JOIN dynasty) ppl 
NATURAL JOIN title;
```
