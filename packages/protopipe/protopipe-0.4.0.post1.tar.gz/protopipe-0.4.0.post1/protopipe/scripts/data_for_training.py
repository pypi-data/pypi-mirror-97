#!/usr/bin/env python
"""Process simtel data for the training of an estimator model.

This pipeline tool can produce data files in HDF5 file format with the
following information:

- simulated information (if available)
- DL1a (optional), reconstructed calibrated images and peak times
- DL1b (optional), image parameters and cleaning masks
- DL2a (requires DL1b), shower geometry reconstruction

For documentation and examples, please visit the webpage
https://cta-observatory.github.io/protopipe/scripts/data_training.html
"""

import argparse
import json

from ctapipe.tools import Stage1Tool

def main():

# READ GENERAL CONFIG

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--general_config_file", type=str, required=True)
    parser.add_argument("--DL1_config_file", type=str, required=True)


# READ CLI args

# READ DL1 CONFIG

    with open(parser.DL1_config_file, 'r') as cfg:
        stage1_config = cfg.read()

    # parse file
    stage1_config = json.loads(stage1_config)

# LAUNCH STAGE1

    tool = Stage1Tool()
    tool.run()

# OPEN DL1

# LOOP OVER EVENTS

# RECONSTRUCT SHOWER

# WRITE DL2a


if __name__ == "__main__":
    main()
