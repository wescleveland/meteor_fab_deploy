# Fabric script for deploying meteor apps

This is a quick and dirty script to satisfy the requirements I had for quickly deploying a meteor app.



This package was created because the existing nvd3 package's github repo seems to have been made private.

## Installation

Install python, install fabric via pip, copy fabfile.py to the root of your meteor app.  Edit the settings at the top of fabfile.py.

## Examples

List commands
'''
$ fab help
'''

Deploy app
'''
$ fab deploy
'''

Restart forever process
'''
$ fab restart_app
'''

Fetch a dump of the app's mongo db
'''
$ fab get_mongo_dump
$ tar -xvf dump.tar.gz
$ mongorestore
'''

Pull requests welcomed, there are most likely better ways of doing these actions but this worked for my simple needs.