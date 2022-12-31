#!/usr/bin/env python

import hashlib
import json
import os

LINK = "1~{0}	/~{0}	tilde.club	70"

def compare_gophermaps(user, cache):
    user_path = f"/home/{user}/public_gopher/gophermap"

    if not os.path.exists(user_path):
        # Ignore user if public_gopher folder is not found
        return

    if user in cache:
        print(LINK.format(user))
        return

    skel_path = "/etc/skel/public_gopher/gophermap"
    skel_hash = hashlib.sha256()
    with open(skel_path, "rb") as f:
        skel_hash.update(f.read())

    try:
        user_hash = hashlib.sha256()
        with open(user_path, "rb") as f:
            user_hash.update(f.read())

        if user_hash.hexdigest() != skel_hash.hexdigest():
            cache[user]=True
            print(LINK.format(user))
    except PermissionError:
        # Ignore PermissionError exceptions and treat the gophermap file as one to not list
        pass

def main():
    cache_path = "cache.json"

    # Load the cache from disk if it exists, otherwise create a new cache
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    for user in sorted(os.listdir("/home"), key=lambda x: x.lower()):
        compare_gophermaps(user, cache)

    # Save the cache to disk
    with open(cache_path, "w") as f:
        json.dump(cache, f)

if __name__ == "__main__":
    main()
