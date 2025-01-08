# This is an example script specifically for results reproduction.
# Takes as input any of the provided systems and runs the simulation and analysis.

# Usage:
# python scripts/example_run.py inputs/BACE/A34_A31_r0/

from atm.rbfe_production import rbfe_production
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

    # We copy the uwham_analysis.R script into the simulation directory
    shutil.copy(
        "uwham_analysis.R",
        sim_dir,
    )

    # These parameters allow you to select which samples you want to use for the analysis.
    # It's recomneded to discard the first 30% samples.
    rmin = int(0.3 * int(config_cntl["MAX_SAMPLES"]))
    rmax = int(config_cntl["MAX_SAMPLES"])

    # Now, we execute the analysis using R
    r_exec = shutil.which("R", mode=os.X_OK)
    basename = config_cntl["BASENAME"]
    subprocess.run(
        [
            r_exec,
            "CMD",
            "BATCH",
            f"-{basename}",
            f"-{rmin}",
            f"-{rmax}",
            "uwham_analysis.R",
        ],
        cwd=sim_dir,
    )

    with open(os.path.join(sim_dir, "uwham_analysis.Rout"), "r") as f:
        for line in f.readlines():
            if "DDGb =" in line and "sprintf" not in line:
                res = line.split(" ")
                print("ddG:", float(res[2]))
                print("Error", float(res[4]))
                print("Replicas", int(res[-1]))


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Specify ONE input directory"

    main(sys.argv[1])
