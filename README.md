## Synopsis

The Hero 5 data parser started as a holiday hacking project. The initial focus for h5parser was to reverse engineer the GoPro Hero 5 auxiliary binary data stream to extract the GPS, Accelerometer and Gyroscope data. As such, any actual functionality from the parser is focused on exploring the structure of the stream.

## Notes and Credit
My ego compels me to state that I mapped the file structure myself.

But to be fair, David Stillman (https:github.com/stilldavid/gopro-utils) finished reverse engineering the file before I ever even started. Credit to him for great work. His code is clean, nice and used in production. Mine is a hot mess with a mid-life crisis due to a lack of purpose.

## Code and Branches
The code on master will parse files, but needs to be modified to output any useful data. Feel free to write your own code to export the data as needed

The code on `orphaned_dev_changes` does not run.

## Dependencies
> python 2.7
> ffmpeg (to extract the data from the mp4 container)
> bash
> code skillz?

## Install (optional)

If you plan to use the parser with  `./parser.py`:
```bash
chmod ug+x parser.py
```

## Usage

### Command Line
Extract the data stream into a suitable file:
```bash
ffmpeg -i video_file.mp4 -codec copy -map 0:3 -f rawvideo data.bin
```

Process the file ("installed"):
```bash
./parser.py data.bin
```

Process the file ("installed"):
```bash
python2.7 parser.py data.bin
```

### Programmatic
(TBD)
