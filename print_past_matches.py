#!/bin/python
"""
Print past matches given algorithm_id.

Works for anyone's algorithm.
"""

import requests
import argparse
import tabulate
import datetime
from typing import Sequence
from colorama import Fore  # type: ignore

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("algorithm_id", type=int)
parser.add_argument("--limit", type=int, default=50, help="Maximum number of newest entries")
args=parser.parse_args()

limit: int=args.limit
algorithm_id: int=args.algorithm_id

#data_str=Path("/tmp/d").read_text()
#data=json.loads(data_str)

# warning: ignore SSL certificate error!!!
data=requests.get(f"https://terminal.c1games.com/api/game/algo/{algorithm_id}/matches", verify=False).json()


def get_data_API(
		data: dict,
		algorithm_id: int
		)-> Sequence[Sequence]:
	result=[]
	for match in data["data"]["matches"]:
		if algorithm_id==match["winning_algo"]["id"]:
			me="winning"
			opponent="losing"
		else:
			me="losing"
			opponent="winning"


		result.append((
			#dateutil.parser.parse( match["date"]),

			#rating
			#match[me+"_algo"]["rating"]

			#opponent_rating
			match[opponent+"_algo"]["rating"],

			match[opponent+"_algo"]["name"],

			match[opponent+"_algo"]["id"],

			match["id"],

			#status
			{"winning": Fore.GREEN+"won"+Fore.RESET, "losing": Fore.RED+"lost"+Fore.RESET}[me],
			))
	return result




print(tabulate.tabulate(
	get_data_API(data, algorithm_id)[:limit],
	headers=("rating", "name", "opponent id", "match id", "status",)
	))

#sorted(
#		get_data_API(data, algorithm_id),
#		key=lambda x: x[0]
#		)
##

# unfortunately rating always refer to the current rating
