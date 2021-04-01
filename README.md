# Usage

The goal of this project is to provide a means by which players of the game Crusader Kings II can
access and explore the interesting data in their save files. We do this by loading the data into a SQL database.

Run `python application.py SAVE_FILE_NAME_HERE` to load the data from the specified save file
and enter the command line interface for exploring the game's data.
Loading may take up to a minute for sufficiently large files.
Once in the command line interface, type `help` to see a list of available commands,
and `help command` to get more information on a specific command.

The data is placed into SQLite3 database file named `ck2-db.db`.
You can use `sqlite3 ck2-db.db` to open it and run SQL queries by hand.

`python application.py` will open the command line interface using whatever data is in the `ck2-db.db` file.


# Test Data

You can download test data (example save files) from:
- https://homepages.rpi.edu/~xieo/ck2_data.tar.gz
- https://homepages.rpi.edu/~xieo/ck2_data.zip

Both archives contain the following files (you can ignore the rest as it's outdated compared to what's integrated into the repo):

- `Leon1067_02_12.ck2` - This is the standard dataset. Does not contain any bloodlines. .

- `Bloodlines.ck2` - Alternative dataset that contains bloodlines. 

For using your own save data, be sure to save your file in-game in a non-compressed format (there should be a box to tick).
This tool will not work for ironman-mode saves, since they are encoded to prevent save-game editing.

# Relation Meanings

The following table lists and describes each table in the database schema.
See `ck2_make_table.sql` for the exact schema.

| Relation Name             | Meaning |
| ------------------------- | ------- |
| barony                    | A table of tuples that describes a single city, castle, church, or other singular holding |
| bloodlineowners           | A table that maps characters to bloodlines |
| bloodlines                | A table of tuples that describes a bloodline by giving it a name and founder |
| culture                   | A table of tuples that describes a culture |
| claim                     | A table that maps characters to titles they have claims on |
| dynasty                   | A table of tuples that describes a dynasty |
| marriage                  | A table of tuples that describes a marriage between two characters   |
| person                    | A table of tuples that describes a character |
| province                  | A table of tuples that describes a singular province (a section of land) |
| religion                  | A table of tuples that describes a religion |
| title                     | A table of tuples that describes a title (e.g. county of dorset, duchy of essex, kingdom of england, or empire of britannia) |
| trait                     | A table that maps characters to traits |
| traitlookup               | A table of tuples that describes a trait |


# Example Queries

```sql
-- Query for getting all of the traits of noble people
SELECT birthname, dynastyname, traitname 
FROM person NATURAL JOIN dynasty NATURAL JOIN trait NATURAL JOIN traitlookup;
```

```sql
-- Query for getting noble people and their titles.
SELECT birthname, dynastyname, name as title, level
FROM (
      SELECT personid AS holderid, birthname, dynastyname 
         FROM person NATURAL JOIN dynasty) ppl 
NATURAL JOIN title;
```
Bear in mind that natural join of `person` and `dynasty` tables will try to match not only dynastyID, but also cultureID and religionID, often resulting in less results than you'd expect.

```sql
-- Query for the culture and religion for all living, noble people
SELECT birthname, dynastyname, culturename, religionname
FROM person NATURAL JOIN dynasty NATURAL JOIN culture NATURAL JOIN religion
WHERE deathday is NULL;
```

# Reference

Information on how ck2 save files are formatted can be found here:
 - https://ck2.paradoxwikis.com/Save-game_editing#Save_File_Contents
