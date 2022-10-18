"""
@author: https://github.com/FarisHijazi
Use ffprobe to extract black frames and ffmpeg to trim them and output a new video
"""

# help from:
# https://video.stackexchange.com/questions/16564/how-to-trim-out-black-frames-with-ffmpeg-on-windows#new-answer?newreg=d534934be5774bd1938b535cd76608cd
# https://github.com/kkroening/ffmpeg-python/issues/184#issuecomment-493847192


import argparse
import os
import shlex
import subprocess

parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input', type=str, help='input video file')
parser.add_argument('--invert', action='store_true', help='remove nonblack instead of removing black')
args = parser.parse_args()

##FIXME: sadly you must chdir so that the ffprobe command will work
os.chdir(os.path.split(args.input)[0])
args.input = os.path.split(args.input)[1]

spl = args.input.split('.')
outpath = '.'.join(spl[:-1]) + '.' + ('invert' if args.invert else '') + 'out.' + spl[-1]


def delete_back2back(l):
  from itertools import groupby
  return [x[0] for x in groupby(l)]


def construct_ffmpeg_trim_cmd(timepairs, inpath, outpath):
  cmd = f'ffmpeg -i "{inpath}" -y -filter_complex '
  cmd += '"'
  for i, (start, end) in enumerate(timepairs):
    cmd += (f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,format=yuv420p[{i}v]; " +
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[{i}a]; ")
  for i, (start, end) in enumerate(timepairs):
    cmd += f"[{i}v][{i}a]"
  cmd += f'concat=n={len(timepairs)}:v=1:a=1[outv][outa]'
  cmd += '"'
  cmd += f' -map [outv] -map [outa] "{outpath}"'
  return cmd


def get_blackdetect(inpath, invert=False):
  ffprobe_cmd = f"ffprobe -f lavfi -i \"movie={inpath},blackdetect[out0]\" -show_entries tags=lavfi.black_start,lavfi.black_end -of default=nw=1 -v quiet"
  print('ffprobe_cmd:', ffprobe_cmd)
  lines = subprocess.check_output(shlex.split(ffprobe_cmd)).decode('utf-8').split('\n')
  times = [float(x.split('=')[1].strip()) for x in delete_back2back(lines) if x]
  assert len(times), 'no black detected'

  if not invert:
    times = [0] + times[:-1]
  timepairs = [(times[i], times[i + 1]) for i in range(0, len(times) // 2, 2)]
  return timepairs

if __name__ == "__main__":
  timepairs = get_blackdetect(args.input, invert=args.invert)
  cmd = construct_ffmpeg_trim_cmd(timepairs, args.input, outpath)

  print(cmd)
  os.system(cmd)
