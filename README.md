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

As superuser `postgres` in psql, run `ck2_setup.py` to create the ck2 database.
This will also create the user `charles` with password `frank`.

Now, run `load_data.py` to load the data from the `Leon1067_02_12.ck2` file by default. You can optionally add the name of a different `.ck2` file to load into the database, as opposed to the default.
