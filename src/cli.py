#!/usr/bin/env python3
import argparse
import json


def cli(args):
    dest_width = int((16 / 9) * args.dest_res)
    scale_ratio = args.dest_res / args.src_res

    with open(args.input) as f:
        input_data = json.load(f)

    for source in input_data["sources"]:
        if source["versioned_id"] == "scene":
            for item in source["settings"]["items"]:

                # item is full-size on input scene
                if (
                    item["bounds"]["x"] == 0.0
                    and item["bounds"]["y"] == 0.0
                    and item["pos"]["x"] == 0.0
                    and item["pos"]["y"] == 0.0
                ):
                    item["bounds"]["x"] = dest_width
                    item["bounds"]["y"] = args.dest_res
                    item["bounds_type"] = 2
                    item["scale_filter"] = "bicubic"
                else:
                    # shift positions
                    if item["pos"]["x"]:
                        item["pos"]["x"] *= scale_ratio
                    if item["pos"]["y"]:
                        item["pos"]["y"] *= scale_ratio

                    # scale
                    if item["scale"]["x"]:
                        item["scale"]["x"] *= scale_ratio
                    if item["scale"]["y"]:
                        item["scale"]["y"] *= scale_ratio

    with open(args.output, "w") as f:
        json.dump(input_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("src_res", type=int)
    parser.add_argument("dest_res", type=int)
    args = parser.parse_args()
    cli(args)
