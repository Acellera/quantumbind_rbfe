# This is an example script specifically for results reproduction.
# Takes as input any of the provided systems and runs the simulation and analysis.

# Usage:
# python scripts/example_run.py inputs/BACE/A34_A31_r0/

from atm.rbfe_explicit_sync import main as atm_production
from glob import glob
from configobj import ConfigObj
import subprocess
import shutil
import yaml
import sys
import os


def main(sim_dir):
    with open(os.path.join(sim_dir, "nodefile"), "w+") as f:
        f.write("localhost,0:0,1,CUDA,,/tmp")

    config_cntl_file = glob(os.path.join(sim_dir, "*.cntl"))[0]
    config_cntl = ConfigObj(config_cntl_file)

    # Convert cntl file to yaml
    yaml_file = config_cntl_file.replace(".cntl", ".yaml")
    config_dict = config_cntl.dict()
    config_dict["TEMPERATURES"] = [
        float(config_dict["TEMPERATURES"]),
    ]
    config_dict["DIRECTION"] = [int(x) for x in config_dict["DIRECTION"].split(",")]
    config_dict["INTERMEDIATE"] = [
        int(x) for x in config_dict["INTERMEDIATE"].split(",")
    ]
    config_dict["LAMBDAS"] = [float(x) for x in config_dict["LAMBDAS"].split(",")]
    config_dict["LAMBDA1"] = [float(x) for x in config_dict["LAMBDA1"].split(",")]
    config_dict["LAMBDA2"] = [float(x) for x in config_dict["LAMBDA2"].split(",")]
    config_dict["ALPHA"] = [float(x) for x in config_dict["ALPHA"].split(",")]
    config_dict["U0"] = [float(x) for x in config_dict["U0"].split(",")]
    config_dict["W0COEFF"] = [float(x) for x in config_dict["W0COEFF"].split(",")]

    with open(yaml_file, "w") as of:
        yaml.dump(config_dict, of, default_flow_style=None)

    atm_production(yaml_file)

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
