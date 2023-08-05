"""
This module contains all functions related to pulling the features/feature scripts.
A successful query results in data being stored where the user indicates (AWS/local).
"""
from pyrasgo.pull import pull_code


def get_feature(feature_ids: list) -> list:
	return pull_code(feature_ids)


# build out helper functions to allow for simple unit testing


