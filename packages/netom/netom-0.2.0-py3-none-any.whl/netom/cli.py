import argparse
import io
import sys

import munge

import netom


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="netom")
    parser.add_argument(
        "--version",
        action="version",
        version="{}s version {}".format("%(prog)", netom.__version__),
    )
    # parser.add_argument("--output-format", help="output format (yaml, json, text)")

    parser.add_argument("command")
    parser.add_argument("render_call")
    parser.add_argument("model_version")
    parser.add_argument("model_type")
    parser.add_argument("data_file")
    args = parser.parse_args(argv)

    # get dict of options and update config
    argd = vars(args)

    command = argd["command"]
    render_call = argd["render_call"]
    model_version = argd["model_version"]
    model_type = argd["model_type"]

    if command != "render":
        raise Exception("only render is supported")

    render = netom.Render(model_version, model_type)
    data = munge.load_datafile(argd["data_file"])

    with io.StringIO() as fobj:
        getattr(render, render_call)(data, fobj)
        print("---")
        print(fobj.getvalue())

    return 0
