#!/usr/bin/env python

import hashlib
import json
import os
import time

LINK = "1~{0}	/~{0}	tilde.club	70"

# This function returns boolean on whether `cache` was modified
def compare_gophermaps(user, cache):
    user_path = f"/home/{user}/public_gopher/gophermap"
    current_time = time.time()
    time_threshold = 259200

    if user in cache and current_time-cache[user] < time_threshold:
        print(LINK.format(user))
        return False

    if not os.path.exists(user_path):
        # Ignore user if public_gopher folder is not found
        if user in cache:
            del cache[user]
            return True
        else:
            return False

    skel_path = "/etc/skel/public_gopher/gophermap"
    skel_hash = hashlib.sha256()
    with open(skel_path, "rb") as f:
        skel_hash.update(f.read())

    try:
        user_hash = hashlib.sha256()
        with open(user_path, "rb") as f:
            user_hash.update(f.read())

        if user_hash.hexdigest() != skel_hash.hexdigest():
            cache[user]=current_time
            print(LINK.format(user))
            return True
        else:
            if user in cache:
                del cache[user]
                return True
            else:
                return False
    except FileNotFoundError:
        # Accessible gopher directory without gophermap is a non-stock gopher directory
        cache[user]=current_time
        print(LINK.format(user))
        return True
    except:
        # PermissionError and the rest, treat the gophermap file as one to not list
        if user in cache:
            del cache[user]
            return True
        else:
            return False

def main():
    cache_path = "cache.json"
    modified = False

    # Load the cache from disk if it exists, otherwise create a new cache
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            cache = json.load(f)
    else:
        cache = {}
        modified = True

    for user in sorted(os.listdir("/home"), key=lambda x: x.lower()):
        if compare_gophermaps(user, cache):
            modified = True

    # Save the cache to disk, if modified
    if modified:
        with open(cache_path, "w") as f:
            json.dump(cache, f)

if __name__ == "__main__":
    main()
