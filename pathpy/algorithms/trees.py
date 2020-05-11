"""Pathpy tree algorithms."""
# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : tree.py -- Module containing tree algorithms
# Author    : Ingo Scholtes <scholtes@uni-wuppertal.de>
# Time-stamp: <Mon 2020-05-11 19:33 ingo>
#
# Copyright (c) 2016-2020 Pathpy Developers
# =============================================================================
from __future__ import annotations
from typing import Any, List, Union, Optional
from functools import singledispatch
from collections import defaultdict

import numpy as np
from scipy import sparse  # pylint: disable=import-error

from pathpy import logger
from pathpy.core.base import BaseNetwork

# create logger
LOG = logger(__name__)




def check_tree(network: BaseNetwork):

    
    if network.directed: 
        
        # identify node with zero indegree
        root = None
        for v in network.nodes.uids:
            if network.indegrees()[v]==0:
                if root == None:
                    root = v
                else:   # two nodes with in-degree zero -> no tree
                    return False
        if root == None:  # no node with indegree zero -> no tree
            return False

        visited = defaultdict(bool)

        def dfs(network: BaseNetwork, node: str):
            
            nonlocal visited

            visited[node] = True
            tree = True
            for v in network.successors[node]:
                if visited[v.uid]:
                    tree &= False
                else:
                    tree &= dfs(network, v.uid)
            return tree
        return dfs(network, root)
    
    else: 
        LOG.error('Tree checking not supported for undirected networks')
    
    return False


def tree_size(network: BaseNetwork, node: str):

    size = 1
    for v in network.successors[node]:
        size += tree_size(network, v.uid)
    return size