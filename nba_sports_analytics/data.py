import nba_py
from nba_py import *
from nba_py.player import get_player
from nba_py.constants import *
from nba_py.shotchart import TeamID
from nba_py.draftcombine import *
from nba_py.game import *
from nba_py.shotchart import *
import pandas as pd
import numpy as np

from urllib.request import *
import urllib.request, json, sys, requests




def parse_endpoint(block):
    name = block[0][3:-1]
    param_names = [line[4:] for line in block[2:]
                   if line[4:] is not '']
    params = [
        {"name": p, "required": False}
        for p in param_names
    ]
    return {"endpoint": name, "params": params, "description": None}


def get_endpoints(path):
    with open(path, 'r') as f:
        md = ''.join(f.read())

    endpoints = [parse_endpoint(block)
                 for block in map(lambda s: s.split("\n"), md.split("\n\n"))
                 if block[0].startswith("##")]

    return endpoints

def get_team_ids():
    team_ids = {}
    team_info = constants.TEAMS
    for i, info in team_info.items():
        team_id = {i:info["id"]}
        team_ids.update(team_id)

    return team_ids


