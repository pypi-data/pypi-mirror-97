import os
import sys
from subprocess import call


def main():
    if len(sys.argv) < 2:
        print("Usage: k8s-config CONFIG_NAME")
        exit(1)
    config_path = os.path.expanduser("~/.chzsh/{}.k8s.cfg".format(sys.argv[1]))
    if not os.path.exists(config_path):
        print("No such file or directory {}".format(config_path))
    kube_dir = os.path.expanduser("~/.kube")
    call(["mkdir", "-p", kube_dir])
    call(["cp", config_path, os.path.join(kube_dir, "config")])


if __name__ == "__main__":
    main()
    exit(0)
