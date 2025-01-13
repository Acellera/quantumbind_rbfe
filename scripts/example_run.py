# This is an example script specifically for results reproduction.
# Takes as input any of the provided systems and runs the simulation and analysis.

# Usage:
# python scripts/example_run.py inputs/BACE/A34_A31_r0/

from atm.rbfe_production import rbfe_production
from atm.uwham import calculate_uwham
from glob import glob
import subprocess
import shutil
import yaml
import sys
import os


def main(sim_dir):
    with open(os.path.join(sim_dir, "nodefile"), "w+") as f:
        f.write("localhost,0:0,1,CUDA,,/tmp")

    yaml_file = glob(os.path.join(sim_dir, "*.yaml"))[0]

    with open(yaml_file, "r") as of:
        config_cntl = yaml.safe_load(of)

    rbfe_production(yaml_file)

    # These parameters allow you to select which samples you want to use for the analysis.
    # It's recomneded to discard the first 30% samples.
    rmin = int(0.3 * int(config_cntl["MAX_SAMPLES"]))
    rmax = int(config_cntl["MAX_SAMPLES"])

    # Now, we execute the analysis
    ddG, ddG_std, _, _, samples = calculate_uwham(
        sim_dir, config_cntl["BASENAME"], rmin, rmax
    )

    print("ddG:", ddG)
    print("Error", ddG_std)
    print("Replicas", samples)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Specify ONE input directory"

    main(sys.argv[1])
