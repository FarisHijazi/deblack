"""
https://github.com/FarisHijazi/deblack
Use ffprobe to extract black frames and ffmpeg to trim them and output a new video
"""

# help from:
# https://video.stackexchange.com/questions/16564/how-to-trim-out-black-frames-with-ffmpeg-on-windows#new-answer?newreg=d534934be5774bd1938b535cd76608cd
# https://github.com/kkroening/ffmpeg-python/issues/184#issuecomment-493847192


import argparse
import os
import shlex
import subprocess


def delete_back2back(l):
    from itertools import groupby

    return [x[0] for x in groupby(l)]


def construct_ffmpeg_trim_cmd(timepairs, inpath, outpath, has_audio=True):
    cmd = f'ffmpeg -i "{inpath}" -y -filter_complex '
    cmd += '"'
    for i, (start, end) in enumerate(timepairs):
        cmd += (
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,format=yuv420p[{i}v]; "
            + (f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[{i}a]; " if has_audio else "")
        )
    for i, (start, end) in enumerate(timepairs):
        cmd += f"[{i}v]"
        if has_audio:
            cmd += f"[{i}a]"

    audio_cmd = " [outa]" if has_audio else ""
    audio_cmd1 = ":a=1" if has_audio else ""
    cmd += f"concat=n={len(timepairs)}:v=1{audio_cmd1}[outv]{audio_cmd}"
    cmd += '"'
    audio_cmd = " -map [outa]" if has_audio else ""
    cmd += f' -map [outv]{audio_cmd} "{outpath}"'
    return cmd


def get_blackdetect(inpath, invert=False):
    ffprobe_cmd = f'ffprobe -f lavfi -i "movie={inpath},blackdetect[out0]" -show_entries tags=lavfi.black_start,lavfi.black_end -of default=nw=1 -v quiet'
    print("ffprobe_cmd:", ffprobe_cmd)
    lines = (
        subprocess.check_output(shlex.split(ffprobe_cmd)).decode("utf-8").split("\n")
    )
    times = [float(x.split("=")[1].strip()) for x in delete_back2back(lines) if x]
    assert len(times), "no black detected"

    if not invert:
        times = [0] + times[:-1]
    timepairs = [(times[i], times[i + 1]) for i in range(0, len(times) // 2, 2)]
    return timepairs


def main():
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        elif v.lower() == 'auto':
            return 'auto'
        else:
            raise argparse.ArgumentTypeError("Boolean value expected.")

    parser = argparse.ArgumentParser(
        __doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", type=str, help="input video file")
    parser.add_argument(
        "--invert", action="store_true", help="remove nonblack instead of removing black"
    )
    parser.add_argument("--audio", type=str2bool, default="auto", help="input video contains audio? (auto, yes, no)")
    args = parser.parse_args()

    ##FIXME: sadly you must chdir so that the ffprobe command will work
    video_dir, video_name = os.path.split(os.path.join('.', args.input))
    os.chdir(video_dir)
    args.input = video_name

    spl = args.input.split(".")
    outpath = (
        ".".join(spl[:-1]) + "." + ("invert" if args.invert else "") + "out." + spl[-1]
    )

    if args.audio == "auto":
        try:
            args.audio = subprocess.check_output(shlex.split(f'ffprobe -i "{args.input}" -show_streams -select_streams a -loglevel error')).decode("utf-8").strip() != ""
        except Exception as e:
            print(e, "Failed to detect audio, assuming no audio. Use --audio to override.")
    else:
        args.audio = args.audio

    timepairs = get_blackdetect(args.input, invert=args.invert)
    cmd = construct_ffmpeg_trim_cmd(timepairs, args.input, outpath, has_audio=args.audio)

    print(cmd)
    # run the command cmd
    subprocess.call(shlex.split(cmd))

if __name__ == "__main__":
    main()
