import hashlib
import os
from subprocess import call
from uuid import uuid4


def join_path(*args):
    if not args:
        return ""
    for i in range(len(args)):
        if not args[i]:
            return join_path(*(args[:i] + args[i + 1:]))
    if len(args) == 1:
        return args[0]
    return os.path.join(*args)


BUF_SIZE = 65536


def get_file_hash(path):
    # sha1 = hashlib.sha1()
    # with open(path, 'rb') as f:
    #     while True:
    #         data = f.read(BUF_SIZE)
    #         if not data:
    #             break
    #         sha1.update(data)
    # return sha1.digest()
    return str(get_file_size(path)).encode()


def get_dir_tree(path, rel=""):
    for suffix in [".st", ".part"]:
        if path.endswith(suffix) or os.path.exists(path + suffix):
            return []
    if not os.path.isdir(path):
        return [
            {"path": path, "rel": rel, "type": "file", "hash": get_file_hash(path)}
        ]
    else:
        fix_io_errors(path)

    res = []
    sha1 = hashlib.sha1()
    for name in sorted(list(os.listdir(path)), key=lambda k: (-1 if os.path.isdir(os.path.join(path, k)) else 1, k)):
        new_path = join_path(path, name)
        new_rel = join_path(rel, name)
        cur = get_dir_tree(new_path, new_rel)
        if not cur:
            continue
        res += cur
        sha1.update(b"^^" + new_rel.encode() + b"$" + cur[0]["hash"] + b"$")
    return [
               {"path": path, "rel": rel, "type": "dir", "hash": sha1.digest()}
           ] + res


def dir_tree_to_map(tree):
    res = {}
    for d in tree:
        res[d["rel"]] = d
    return res


def get_file_size(path):
    return os.path.getsize(path)


def get_size(path):
    if os.path.isdir(path):
        res = 0
        for name in os.listdir(path):
            res += get_size(join_path(path, name))
        return res
    return get_file_size(path)


def get_dirs_files_cnt(path):
    if os.path.isdir(path):
        dirs, files = 1, 0
        for name in os.listdir(path):
            cur_dirs, cur_files = get_dirs_files_cnt(join_path(path, name))
            dirs += cur_dirs
            files += cur_files
        return dirs, files
    return 0, 1


def human_readable_size(sz):
    """
    :param sz: int, in bytes
    :return:
    """
    sz = int(sz)
    if sz < 0:
        return "-" + human_readable_size(-sz)
    unit = ["B", "KB", "MB", "GB", "TB"]
    for u in unit:
        if sz < 1000:
            return "{:.2f}".format(sz) + u
        sz /= 1000
    return "INF"


def fix_io_errors(par):
    # os.stat(filename)
    bad_files = set()
    for f in os.listdir(par):
        path = os.path.join(par, f)
        try:
            os.stat(path)
        except OSError:
            bad_files.add(path)
    if not bad_files:
        return

    tmp_dir = os.path.join(os.path.dirname(par), str(uuid4()))
    print(f"Temporarily {par} moving to {tmp_dir}")
    call(["mkdir", "-p", tmp_dir])
    moved = []

    for f in os.listdir(par):
        path = os.path.join(par, f)
        if path in bad_files:
            continue
        moved.append((path, os.path.join(tmp_dir, f)))
        call(["mv", moved[-1][0], moved[-1][1]])

    call(["gio", "trash", par])
    call(["gio", "trash", "--empty"])
    call(["mkdir", "-p", par])

    for old_path, tmp_path in moved:
        call(["mv", tmp_path, old_path])

    call(["rm", "-rf", tmp_dir])
    print(f"Fixed {len(bad_files)} io errors!")
