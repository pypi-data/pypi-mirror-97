import os
import sys
from subprocess import call

from charzsh.utils import join_path, get_file_hash, get_dir_tree, dir_tree_to_map, get_size, human_readable_size


def main():
    if len(sys.argv) < 3:
        print("Usage: chzsh-bu SOURCE_DIR DEST_DIR")
        exit(1)
    source_dir, dest_dir = get_src_dst_dir()
    source_dir_tree = get_dir_tree(source_dir)
    dest_dir_tree_map = dir_tree_to_map(get_dir_tree(dest_dir))

    dirs_made = 0
    files_copied = 0
    bytes_copied = 0
    start_size = get_size(dest_dir)

    for ent in source_dir_tree:
        rel = ent["rel"]
        if rel not in dest_dir_tree_map and ent["type"] == "dir":
            os.mkdir(join_path(dest_dir, rel))
            dirs_made += 1
            continue
        elif dest_dir_tree_map and ent["type"] == "dir":
            continue
        elif rel in dest_dir_tree_map and ent["hash"] == dest_dir_tree_map[rel]["hash"]:
            continue
        print("Preparing to copy file {}".format(rel))

        source_file_path = ent["path"]
        dest_file_path = join_path(dest_dir, rel)
        success = False
        while not success:
            cmd = ["cp", source_file_path, dest_file_path]
            print(" ".join(cmd))
            ret_code = call(cmd)
            if ret_code == 0 and os.path.exists(dest_file_path) and ent["hash"] == get_file_hash(dest_file_path):
                success = True
            else:
                print("Error: calling {}".format(' '.join(cmd)))
                exit(1)
        files_copied += 1
        bytes_copied += get_size(dest_file_path)

    print("Done! Made {} folders and copied {} files. "
          "Copied {} in total.\nDELTA SIZE OF {} = {}"
          .format(dirs_made, files_copied, human_readable_size(bytes_copied), dest_dir,
                  human_readable_size(get_size(dest_dir) - start_size)))


def get_src_dst_dir():
    source_dir, dest_dir = sys.argv[1:3]
    if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
        print("Invalid directory {}".format(source_dir))
        exit(1)
    if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
        print("Invalid directory {}".format(dest_dir))
        exit(1)
    source_dir, dest_dir = os.path.abspath(source_dir), os.path.abspath(dest_dir)
    return  source_dir, dest_dir


if __name__ == "__main__":
    main()
    exit(0)
