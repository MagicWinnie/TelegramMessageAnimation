import os
import sys
import time
import codecs
import logging
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)

parser = ArgumentParser()
parser.add_argument(
    "-f", "--frames", help="Path to a directory with frames.", required=True
)
parser.add_argument(
    "-d", "--delay", help="A delay between frames (seconds).", default=0.25, type=float
)
args = parser.parse_args()

assert os.path.exists(args.frames), "The path to frames folder does not exist."

frames_filenames = os.listdir(args.frames)
frames_filenames = list(
    filter(lambda x: x.endswith(".txt") and x.split(".")[0].isdigit(), frames_filenames)
)
frames_filenames = sorted(frames_filenames, key=lambda x: int(x.split(".")[0]))

MAX_LENGTH = 128

if len(frames_filenames) > MAX_LENGTH:
    print(
        f"[INFO] The length of the animation exceeds the max length of {MAX_LENGTH}. It will be cut to first {MAX_LENGTH} frames."
    )

frames = []

for f in frames_filenames:
    with codecs.open(os.path.join(args.frames, f), encoding="utf-8") as fp:
        frames.append(fp.read())

countPrevLines = 0
for frame in frames:
    for i in range(countPrevLines):
        sys.stdout.write("\033[F")
    print(frame)
    countPrevLines = frame.count("\n") + 1
    time.sleep(args.delay + 0.3)

print()
