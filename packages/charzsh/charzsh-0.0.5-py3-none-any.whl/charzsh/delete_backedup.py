import os
import sys
from subprocess import call

from charzsh.backup import get_src_dst_dir
from charzsh.utils import get_dir_tree, dir_tree_to_map, get_dirs_files_cnt, get_size, human_readable_size

dirs_deleted, files_deleted = 0, 0
bytes_deletes = 0


def delete_empty_dirs(cur, base):
    global dirs_deleted, files_deleted
    if os.path.abspath(cur) == os.path.abspath(base):
        return
    if not os.path.isdir(cur):
        return delete_empty_dirs(os.path.dirname(cur), base)
    if not os.listdir(cur):
        cur_dirs, cur_files = get_dirs_files_cnt(cur)
        cmd = ["rm", "-rf", cur]
        print("DELETING DIR", ' '.join(cmd))
        call(cmd)
        dirs_deleted += cur_dirs
        files_deleted += cur_files
        return delete_empty_dirs(os.path.dirname(cur), base)


def main():
    global dirs_deleted, files_deleted, bytes_deletes
    if len(sys.argv) < 3:
        print("Usage: chzsh-rmbu SOURCE_DIR DEST_DIR")
        exit(1)

    source_dir, dest_dir = get_src_dst_dir()

    source_dir_tree = get_dir_tree(source_dir)
    dest_dir_tree_map = dir_tree_to_map(get_dir_tree(dest_dir))

    print("Source total size:", human_readable_size(get_size(source_dir)))

    for ent in source_dir_tree:
        rel = ent["rel"]
        source_path = ent["path"]
        if not rel or rel not in dest_dir_tree_map:
            continue
        if ent["type"] == "dir":
            delete_empty_dirs(source_path, source_dir)
            continue
        if ent["hash"] != dest_dir_tree_map[rel]["hash"]:
            continue

        if not os.path.exists(source_path):
            continue
        success = False
        cur_dirs, cur_files = get_dirs_files_cnt(source_path)
        cur_bytes = get_size(source_path)

        while not success:
            cmd = ["rm", "-rf", source_path]
            print("Calling", ' '.join(cmd))
            call(cmd)
            if not os.path.exists(source_path):
                success = True
                delete_empty_dirs(source_path, source_dir)
            else:
                print("Error: calling {}".format(' '.join(cmd)))
        dirs_deleted += cur_dirs
        files_deleted += cur_files
        bytes_deletes += cur_bytes

    print("Done! Deleted {} folders and {} files. Removed {} in total".format(dirs_deleted, files_deleted,
                                                                              human_readable_size(bytes_deletes)))


if __name__ == "__main__":
    main()
    exit(0)
