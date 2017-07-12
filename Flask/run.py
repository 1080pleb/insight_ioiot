#!/usr/bin/env python

from app import app
app.run(host='0.0.0.0', debug = True)
#script imports app variable from pkg, invokes run method to start server
#NB the app variable holds Flask instance created before


