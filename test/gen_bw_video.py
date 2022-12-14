"""
this script generates a video of interleaved black and white frames
"""

import numpy as np
import cv2
import argparse


def generate_frames(seconds=30, fps=30):
    for i in range(seconds * fps):
        frame = np.zeros((1080 // 4, 1920 // 4, 3), dtype=np.uint8)
        if i % 2:
            frame[:, :, :] = 255
        yield frame


def main():
    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--outpath", default="bw.mp4")
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(args.outpath, fourcc, args.fps, (1920 // 4, 1080 // 4))
    for frame in generate_frames(args.seconds, args.fps):
        out.write(frame)
    out.release()


if __name__ == "__main__":
    main()
