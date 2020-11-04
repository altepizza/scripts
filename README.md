# Bookmark recovery script
This is a very simple 'recovery' script. It will ask the API for all bookmarks
and folders. If it finds bookmarks that don't belong to any folder or are not
saved in root then it will create a new folder called 'TEMP RECOVERY' and move
them there so that you can easily access them via the frontend again.

## Warning
Do only use this script once. The new folder ID will only be added to the
'folders' attribute of the bookmarks entity and therefore will still be
identified as an orphan in any subsequent run. It may not do any harm, but I
would be cautious anyways.

## Disclaimer
I am very aware that this script is no beauty and I only tested it for my
setup.
USE AT YOUR OWN RISK! Enjoy :)


## Run
`pip install -r requirements.txt`

`python recovery_orphaned_bookmarks.py`

