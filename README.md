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

| Relation Name 			| Meaning |
| ------------------------- | ------- |
| barony					| A table of tuples that describes a single city, castle, church, or other singular holding |
| bloodlineowners			| A table that maps characters to bloodlines |
| bloodlines				| A table of tuples that describes a bloodline by giving it a name and founder |
| culture					| A table of tuples that describes a culture |
| claim					    | A table that maps characters to titles they have claims on |
| dynasty 				    | A table of tuples that describes a dynasty |
| marriage				    | A table of tuples that describes a marriage between two characters   |
| person					| A table of tuples that describes a character |
| province				    | A table of tuples that describes a singular province (a section of land) |
| religion				    | A table of tuples that describes a religion |
| title					    | A table of tuples that describes a title (e.g. county of dorset, duchy of essex, kingdom of england, or empire of britannia) |
| trait					    | A table that maps characters to traits |
| traitlookup				| A table of tuples that describes a trait |
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

```pgsql
-- Query for the culture and religion for all living, noble people
SELECT birthname, dynastyname, culturename, religionname
FROM person NATURAL JOIN dynasty NATURAL JOIN culture NATURAL JOIN religion
WHERE deathday is NULL;
```
