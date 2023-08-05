import os
import sys
import time
from datetime import datetime

from charzsh.backup import get_src_dst_dir
from dateutil.tz import tzlocal

from charzsh.utils import join_path, get_file_hash, get_dir_tree, dir_tree_to_map, get_size, human_readable_size


def main():
    if len(sys.argv) < 3:
        print("Usage: chzsh-eta SOURCE_DIR DEST_DIR")
        exit(1)
    source_dir, dest_dir = get_src_dst_dir()
    start_time = time.time()
    last_check = None
    last_rem = None
    first_rem = None
    first_check = None

    while True:
        source_dir_tree = get_dir_tree(source_dir)
        dest_dir_tree_map = dir_tree_to_map(get_dir_tree(dest_dir))

        diff = 0

        for ent in source_dir_tree:
            rel = ent["rel"]
            if rel not in dest_dir_tree_map and ent["type"] == "dir":
                os.mkdir(join_path(dest_dir, rel))
                continue
            elif dest_dir_tree_map and ent["type"] == "dir":
                continue
            elif rel in dest_dir_tree_map and ent["hash"] == dest_dir_tree_map[rel]["hash"]:
                continue
            source_file_path = ent["path"]
            diff += get_size(source_file_path)
        if diff == 0:
            print("finished in {:.2f}s".format(time.time() - start_time))
            return
        now = time.time()
        print(datetime.now(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"))
        print(f"Remaining: {human_readable_size(diff)}")
        if first_check and first_rem:
            print(f"Avg speed: {human_readable_size((first_rem - diff) / (now - first_check))}/s, having passed " +
                  "{:.2f}s".format(time.time() - start_time))

        if last_check and last_rem:
            print(f"Cur speed: {human_readable_size((last_rem - diff) / (now - last_check))}/s")
            last_check, last_rem = now, diff

        if first_check and first_rem:
            print("ETA: {:.2f}s".format(diff / ((first_rem - diff) / (now - first_check))))
        else:
            first_check, first_rem = now, diff
        print("\n\n")
        time.sleep(120)


if __name__ == "__main__":
    main()
    exit(0)
