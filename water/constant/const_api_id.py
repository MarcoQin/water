#!/usr/bin/env python
# encoding: utf-8

from utils.common_utils import Dict


API_ID = Dict(
    HELLO_WORLD_API=10001,  # Test api hello world
    CALENDAR=Dict(
        LIST=10002,  # Canlendar event
        INSERT=10003,  # create event
        UPDATE=10004,  # create event
    )
)
