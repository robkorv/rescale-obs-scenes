#!/usr/bin/env python3
import argparse
import json


def cli(args):
    # calculations
    dest_width = int((16 / 9) * args.dest_res)
    scale_ratio = args.dest_res / args.src_res

    # reading
    with open(args.input) as f:
        input_data = json.load(f)

    # name
    if args.scene_collection_name.strip():
        input_data["name"] = args.scene_collection_name.strip()
    else:
        name = input_data.get("name")
        input_data["name"] = f"{name}-{args.dest_res}p"

    # audio devices
    if args.remove_audio_devices:
        input_data_copy = input_data.copy()
        for key in input_data.keys():
            if "AudioDevice" in key:
                del input_data_copy[key]
        input_data = input_data_copy

    # resizing
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

    # writing
    with open(args.output, "w") as f:
        json.dump(input_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("src_res", type=int)
    parser.add_argument("dest_res", type=int)
    parser.add_argument("-r", "--remove-audio-devices", action="store_true")
    parser.add_argument("-n", "--scene-collection-name", default="")
    args = parser.parse_args()
    cli(args)
