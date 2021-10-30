#!/bin/python
from __future__ import annotations



from pathlib import Path
import datetime
from typing import Optional
import dateutil
import sys
import subprocess
import subprocess
import json
import argparse


try: import local_patch_hack
except ImportError: continue


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--timezone", help="Display timezone", type=float, default=8.)
parser.add_argument("--xlabel", default= "Time (SGP timezone)")
parser.add_argument("--algorithms",
		help="Comma-separated (without surrounding spaces) list of algorithm names to plot",
		default="algorithm6,a6-2")
parser.add_argument("--save-file-path", default="/tmp/a.png", help="Pass None to not save")

class SetPlotByMatchCount(argparse.Action):
	def __init__(self, *args, **kwargs):
		super().__init__(
				help="Make the X axis by match count instead of time. Changes the value of several default attributes.",
				default=False,
				nargs=0,
				*args, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		namespace.plot_by_match_count=True
		namespace.xlabel="Total number of matches"

parser.add_argument("--plot-by-match-count", action=SetPlotByMatchCount)

parser.add_argument("--least-time-for-dotted-line", help="(in minutes, or in number of matches if --plot-by-match-count is given.)", type=float, default=10)
args=parser.parse_args()

display_timezone = datetime.timezone(datetime.timedelta(hours=args.timezone))
xlabel: str=args.xlabel
use_clipboard=True
#input_text_file=Path("/tmp/message.txt")
input_text_file=None
desired_algorithm_names: list[str] = args.algorithms.split(",")
plot_by_match_count=args.plot_by_match_count
if plot_by_match_count:
	least_time_for_dotted_line=args.least_time_for_dotted_line
else:
	least_time_for_dotted_line=datetime.timedelta(minutes=args.least_time_for_dotted_line)

save_file_path: Optional[str]=args.save_file_path
if not save_file_path: save_file_path=None










utc = datetime.timezone.utc

def get_data(data: list, desired_algorithm_name: str,
		delta
		)-> list[tuple[datetime.datetime, int]] :
	return [
			(
				(
					int(num_win) + int(num_lose)
					if plot_by_match_count
					else datetime.datetime.fromtimestamp( timestamp_javascript/1000 , utc)
					),
				int(rating)
				)
			for (
				algorithm_name,
				timestamp_javascript,
				[rating],
				[num_win],
				[num_lose],
				) in data
			if algorithm_name == [desired_algorithm_name]
			]





data: list=[]
if use_clipboard:
	data_bin: bytes=subprocess.run(
			"xclip -sel c -o".split(),
			stdout=subprocess.PIPE
			).stdout
	data+=json.loads( data_bin)

if input_text_file:
	data += json.loads( input_text_file .read_text())



import matplotlib                   # type: ignore
import matplotlib.pyplot as plt     # type: ignore

plt.rcParams["figure.figsize"]=(10, 7)
plt.rcParams["figure.dpi"]=144
plt.rcParams["figure.facecolor"]="white"

#plt.ion()



fig, ax = plt.subplots(1)
fig.autofmt_xdate()
plotted_lines: list=[]  # representative line to get legend (weird?)
plotted_legend: list[str]=[]

for desired_algorithm_name in desired_algorithm_names:
	data1 = get_data(data, desired_algorithm_name, datetime.timedelta(hours=1))
	if not data1: continue

	data1.sort(key=lambda x: x[0])
	line=plt.plot(*zip(*data1[:1]))[0]
	plotted_lines.append(line)
	plotted_legend.append(desired_algorithm_name)

	last: int=0
	for i in range(1, len(data1)+1):
		if i==len(data1) or data1[i][0]-data1[i-1][0]>=least_time_for_dotted_line:
			plt.plot(*zip(*data1[last:i]), color=line.get_color(), linestyle="-")
			if i!=len(data1):
				plt.plot(*zip(*data1[i-1:i+1]), color=line.get_color(), linestyle=":")
				last=i

if not plot_by_match_count:
	xfmt = matplotlib.dates.DateFormatter('%d-%m-%y %H:%M',
			tz=display_timezone
			)
	ax.xaxis.set_major_formatter(xfmt)

plt.xlabel(xlabel)
plt.ylabel("Rating")
plt.title(f"Rating of {plotted_legend} over time")
plt.legend(plotted_lines, plotted_legend)
if save_file_path:
	plt.savefig(save_file_path)

plt.show()
