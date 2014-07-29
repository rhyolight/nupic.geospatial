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

<<<<<<< HEAD
Use `./tools/run_complete.sh <path/to/input>` to run your own data through the system.

### NuPIC Input File Format

#### Fields

1. name
2. timestamp
3. lon
4. lat
5. ?
6. speed
7. ?
8. accuracy

=======
Use `./run.py <path/to/input>` to run data you've downloaded from the simulator (described above) through the system. This script will automatically create sequences base on the timing of the input rows. If you don't want this behavior, you can negate it with the `--manual-sequence` option.
>>>>>>> 4be1c72e7c6182c620b763750e4dbfd6e27b42ae
