# NuPIC Geospatial [![Build Status](https://travis-ci.org/numenta/nupic.geospatial.svg?branch=master)](https://travis-ci.org/numenta/nupic.geospatial) [![Coverage Status](https://coveralls.io/repos/numenta/nupic.geospatial/badge.png?branch=master)](https://coveralls.io/r/numenta/nupic.geospatial?branch=master)

Geospatial anomaly detection app using NuPIC.

## Usage

First, install requirements:

    pip install -r requirements.txt

Then, run:

    python server.py

Finally, open `http://localhost:5000` in your browser.

### Using the route simulator

You can use the route simulator to generate geospatial data and run it through the model. Simply open `http://localhost:5000/simulate` in your browser. Once you've created a route (or routes), you can either run them immediately through NuPIC with the "Build" button (at the top right of the screen), or you can save the tracks to a local file for running later (use the step below).

### Loading your own data

Use `./run.py <path/to/input>` to run data you've downloaded from the simulator (described above) through the system. This script will automatically create sequences base on the timing of the input rows. If you don't want this behavior, you can negate it with the `--manual-sequence` option.

### Using [GPX](http://www.topografix.com/gpx.asp) files as input

A conversion tool exists for this. GPX v1.0 works, and all the GPX v1.1 files I've used have worked without a problem (so far). 

    ./tools/convert_gpx.py path/to/gpx/file

This will write out a file you can use as input for `./run.py`.