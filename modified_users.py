#!/usr/bin/env python3
import filecmp
import os

def users():
    return sorted(os.listdir("/home"), key=lambda x: x.lower())

LINK = "1~{0}	/~{0}	tilde.club	70"

for user in users():
    if os.path.exists(f"/home/{user}/public_gopher/gophermap"):
        if not filecmp.cmp(
                "/etc/skel/public_gopher/gophermap", 
                f"/home/{user}/public_gopher/gophermap", shallow=False):
            print(LINK.format(user))

