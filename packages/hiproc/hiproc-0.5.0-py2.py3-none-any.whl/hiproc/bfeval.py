#!/usr/bin/env python
"""Evaluate how the algorithms work.

"""

# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import math
import subprocess
import sys
import traceback
import json
from pathlib import Path

import numpy as np
from osgeo import gdal_array

import pvl
import kalasiris as isis

import hiproc.util as util
import hiproc.bitflips as bf


# This is only here for temporary testing

dp = Path("/Users/rbeyer/projects/HiRISE/bitflip")


def main():
    try:
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[util.parent_parser()],
            conflict_handler="resolve",
        )
        parser.add_argument(
            "-l",
            "--log",
            required=False,
            default=21,
            help="The log level to show for this program, can "
            "be a named log level or a numerical level.",
        )
        parser.add_argument(
            "-w",
            "--width",
            required=False,
            default=5,
            type=int,
            help="The number of medstd widths for bit-flip "
            "cleaning. "
            "(default: %(default)s)",
        )
        parser.add_argument(
            "--saveplot",
            required=False,
            nargs="?",
            default=False,
            const=True,
            help="Saves plot for each area to a file.  If a directory is "
            "provided it will be used to save the plots to, otherwise "
            "the directory of the input file will be used.",
        )

        with open(dp / "dn_ideal.json", "r") as f:
            goal_dn = json.load(f)

        args = parser.parse_args()

        set_logging(args.log, args.logfile)

        atol = 75
        # atol = 1000
        logging.log(21, f"DN must be within {atol} of the goal DN.")

        for cid, v in goal_dn.items():

            fp = dp / v["path"]
            label = pvl.load(fp)
            specialpix = getattr(
                isis.specialpixels, label["IsisCube"]["Core"]["Pixels"]["Type"]
            )
            result = dict()

            print(fp)

            result["img"] = image_area_dn(
                fp,
                specialpix=specialpix,
                width=args.width,
                saveplot=args.saveplot,
            )

            result.update(
                tables_dn(
                    fp,
                    specialpix,
                    v,
                    width=args.width,
                    saveplot=args.saveplot,
                )
            )

            log_lines = [
                f"DN for {fp.name}",
            ]
            mm = ("min", "max")
            # print(result.keys())
            for k in sorted(result.keys()):
                for i in (0, 1):
                    g = v[k][i]
                    r = result[k][i]
                    # print(g)
                    # print(type(g))
                    # print(f"result {r}")
                    # print(type(r))
                    if math.isclose(g, r, abs_tol=atol):
                        # print(f"{k} min is close!")
                        pass
                    else:
                        diff = abs(g - r)
                        # print(diff)
                        # print(type(diff))
                        fdiff = diff / max(g, r)
                        # print(fdiff)
                        # print(type(fdiff))
                        log_lines.append(
                            f"  {k} {mm[i]} is not close, "
                            f"goal: {g}, actual: {r}, diff: {diff}, "
                            f"fdiff: {fdiff:.3}"
                        )
            if len(log_lines) > 1:
                for line in log_lines:
                    # Logs at a level slightly above INFO (20), so the default
                    # just logs this, but selecting INFO also allows underlying
                    # modules to log their INFO-level messages.
                    logging.log(21, line)

        sys.exit(0)
    except subprocess.CalledProcessError as err:
        print("Had an ISIS error:", file=sys.stderr)
        print(" ".join(err.cmd), file=sys.stderr)
        print(err.stdout, file=sys.stderr)
        print(err.stderr, file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        traceback.print_exc(file=sys.stderr)
        print(err, file=sys.stderr)
        sys.exit(1)


def set_logging(i, filename=None) -> None:
    """Sets the log level and basic configuration."""
    if isinstance(i, int):
        log_level = i
    else:
        log_level = getattr(logging, i.upper(), logging.WARNING)

    if filename is None:
        logging.basicConfig(format="%(message)s", level=log_level)
    else:
        logging.basicConfig(
            filename=filename, format="%(message)s", level=log_level,
        )
    return


def image_area_dn(
    in_p: Path, specialpix, width=5, axis=0, saveplot=False,
):
    """ISIS Cube version of clean().

    Please see clean() for argument details.
    """

    image = np.ma.masked_outside(
        gdal_array.LoadFile(str(in_p)), specialpix.Min, specialpix.Max
    )

    # logging.info(f"Bit-flip cleaning Image area.")
    # # These four lines are just informational.
    # img_mean = np.ma.mean(image)
    # img_mode = mstats.mode(image, axis=None)[0][0]
    # d = img_mean - img_mode
    # logging.info(f"Mean: {img_mean}, Mode: {img_mode}, diff: {d}")

    return bf.find_smart_window_from_ma(
        image,
        width=width,
        axis=axis,
        plottitle=(f"{in_p.name} Image Area" if saveplot else None),
        saveplot=(Path(saveplot) / in_p.with_suffix(".bf-image.pdf").name)
        if saveplot
        else False,
    )


def tables_dn(
    in_path: Path, specialpix, keys, width=5, saveplot=False,
):
    rev_area = True if "rev" in keys else False
    mask_area = False
    ramp_area = False
    buffer_area = False
    dark_area = False

    tables_result = dict()

    # print(keys)

    if any((rev_area, mask_area, ramp_area)):
        t_name = "HiRISE Calibration Image"
        HCI_dict = isis.cube.get_table(in_path, t_name)
        cal_vals = np.array(HCI_dict["Calibration"])

        cal_image = np.ma.masked_outside(
            cal_vals, specialpix.Min, specialpix.Max
        )

        # logging.info(f"Bit-flip cleaning Reverse-Clock area.")
        tables_result["rev"] = bf.find_smart_window_from_ma(
            cal_image[:20, :],
            width=width,
            axis=1,
            medstd_limit=200,
            plottitle=(f"{in_path.name} Reverse-Clock" if saveplot else None),
            saveplot=(
                Path(saveplot) / in_path.with_suffix(".bf-revclk.pdf").name
            )
            if saveplot
            else False,
        )

    if any((buffer_area, dark_area)):
        raise NotImplementedError(
            f"Bit-flip detection for this area is not yet implemented."
        )

    # print(tables_result)
    return tables_result


if __name__ == "__main__":
    main()
