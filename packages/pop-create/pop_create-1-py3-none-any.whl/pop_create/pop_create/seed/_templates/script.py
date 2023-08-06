#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pop.hub


def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="R__NAME__")
    hub.R__NAME__.init.cli()
