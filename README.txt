
Download all of these files
https://drive.google.com/drive/folders/1hfoggzv6fiiOcrr0wmb0d620AY1ILI5L

As superuser 'postgres' in psql, run ck2_setup.py to create the ck2 database.
This will also create the user 'charles' with password 'frank'.

Now, run load_data.py to load the data from the Leon1067_02_12.ck2 file.
This is the default when no parameters are given, but you can optionally
add the name of a different ck2 file to load into the database.