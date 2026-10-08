"""New narrow identity bridge for the recovered P10 import, not recovered P03 source.

Accepted P03 numeric locations return original units48-50 after the one grant;
current inventory publishes their group35. The host projection remains pending.
Names and numbers are checked against dependencies/p04-abi.json and accepted current p09-schema.json in tests.
"""
TILE_IDS = ("rita_sample_tile_1", "rita_sample_tile_2", "rita_sample_tile_3")
TILE_NATIVE_IDS = (48, 49, 50)
TILE_GROUP_NATIVE_ID = 35
