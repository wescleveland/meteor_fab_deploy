# Fabric script for deploying meteor apps

This is a quick and dirty script to satisfy the requirements I had for quickly deploying a meteor app.
Note: I quickly generalized the script I am currently using to create this, there may be typos, errors, etc but this is
the general idea of what has worked for me.

There is also a fabric command to dump and fetch the remote mongo database which has proved useful to recreate production
data when debugging issues.

## Installation

Install python, install fabric via pip, copy fabfile.py to the root of your meteor app.  Edit the settings at the top of fabfile.py.

## Examples

List commands
``` sh
$ fab help
```

Deploy app
``` sh
$ fab deploy
```

Restart forever process
``` sh
$ fab restart_app
```

Fetch a dump of the app's mongo db
``` sh
$ fab get_mongo_dump
$ tar -xvf dump.tar.gz
$ mongorestore
```

Pull requests welcomed, there are most likely better ways of doing these actions but this worked for my simple needs.