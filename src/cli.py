#!/usr/bin/env python3
import argparse
import json
import pathlib

FILE_SETTING_KEYS = ["local_file", "file"]


def fix_file_path(pathsegment, absolute_input_path, absolute_output_path):
    if pathsegment is None or not pathsegment.strip():
        return None

    input_parent = absolute_input_path.parent
    output_parent = absolute_output_path.parent

    other_path = pathlib.Path(pathsegment)
    if other_path.is_file():
        pathsegment = other_path
    else:
        joined_path = output_parent.joinpath(other_path)
        if joined_path.is_file():
            pathsegment = joined_path
        else:
            found_files = list(output_parent.rglob(other_path.name)) or list(
                input_parent.rglob(other_path.name)
            )
            if found_files:
                other_path_parts = set(other_path.parts)
                found_files_parts_matches = [
                    (found_file, len(list(other_path_parts & set(found_file.parts))))
                    for found_file in found_files
                ]
                pathsegment = max(found_files_parts_matches, key=lambda x: x[1])[0]

    if isinstance(pathsegment, pathlib.Path):
        pathsegment = str(pathsegment.resolve())

    return pathsegment


def cli(args):
    # calculations
    dest_width = int((16 / 9) * args.dest_res)
    scale_ratio = args.dest_res / args.src_res

    # paths
    absolute_input_path = pathlib.Path(args.input_path).resolve(strict=True)
    absolute_output_path = pathlib.Path(args.output_path).resolve()

    # reading
    with open(absolute_input_path) as f:
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

    # files
    if args.fix_file_paths:
        if "modules" in input_data and "scripts-tool" in input_data["modules"]:
            for script_tool in input_data["modules"]["scripts-tool"]:
                script_tool_path = fix_file_path(
                    script_tool.get("path"), absolute_input_path, absolute_output_path
                )
                if script_tool_path:
                    script_tool["path"] = script_tool_path

    for source in input_data["sources"]:
        if "settings" in source:
            settings = source["settings"]
            for file_key in FILE_SETTING_KEYS:
                file = fix_file_path(
                    settings.get(file_key), absolute_input_path, absolute_output_path
                )
                if file:
                    settings[file_key] = file

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
    with open(absolute_output_path, "w") as f:
        json.dump(input_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    parser.add_argument("src_res", type=int)
    parser.add_argument("dest_res", type=int)
    parser.add_argument("-r", "--remove-audio-devices", action="store_true")
    parser.add_argument("-n", "--scene-collection-name", default="")
    parser.add_argument("-f", "--fix-file-paths", action="store_true")
    args = parser.parse_args()
    cli(args)
