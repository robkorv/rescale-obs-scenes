# rescale-obs-scenes

WARNING: Make sure you always create a backup of your exported scenes before tempering with them!

## download

-   Windows: Download the [release](https://github.com/robkorv/rescale-obs-scenes/releases) and run `rescale-obs-scenes.exe`.
-   Linux: clone or download this repo and run `./src/cli.py`.

## usage

-   In OBS use "Scene Collection" -> "Export" to write your scenes to a JSON file.
-   In OBS Take note of the "Base (Canvas) Resolution" at "File" -> "Settings" -> "Video"
-   Run `rescale-obs-scenes.exe input.json output.json src_res dest_res`
-   Import "output.json"

Example

-   I exported scenes with a "Base (Canvas) Resolution" of "1920x1080" to "my-scenes-1080p.json"
-   I want rescale this to "3840x2160" resolution
-   I run `rescale-obs-scenes.exe my-scenes-1080p.json my-scenes-2160p.json 1080 2160`
-   "my-scenes-2160p.json" contains the rescaled scenes
-   I OBS I change the "Base (Canvas) Resolution" to "3840x2160"
-   In OBS I remove my current scenes. "Scene Collection" -> "Remove"
-   Then I import "my-scenes-2160p.json" in OBS. "Scene Collection" -> "Import"
-   Then I switch to the newly imported scenes by selecting them in "Scene Collection"

## Limits

-   only 16/9 ratio supported
-   only tested with rescaling to larger resolutions
-   only tested with one particular scene export that I needed to rescale to a larger resolution

## Development

-   uses [Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all)
-   dependencies
    -   https://pre-commit.com/
    -   https://www.python.org/
    -   https://docs.docker.com/engine/
