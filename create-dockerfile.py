#!/usr/bin/env python3

import argparse
import os.path
import jinja2
import yaml
import urllib.parse
import os
import subprocess
import shutil


def _main():
    parser = argparse.ArgumentParser(
        description="Create Dockerfile from config yaml")
    parser.add_argument(
        "--output", "-o", help="Output directory", required=True)
    parser.add_argument("config", help="Config file",
                        type=argparse.FileType('r'))
    parser.add_argument("--templates", "-t", help="templates directory (default: %(default)s)",
                        default=os.path.join(os.path.dirname(__file__), "templates"))
    parser.add_argument(
        "--build", "-b", help="Build docker images", action="store_true")
    parser.add_argument(
        "--username", "-u", help="Docker Hub username (default: %(default)s)", default="bioslimcontainers")
    options = parser.parse_args()

    config = yaml.load(options.config)
    print(config)

    templates = {}
    for root, dirs, files in os.walk(options.templates):
        for one_file in files:
            if one_file == "Dockerfile":
                with open(os.path.join(root, one_file)) as f:
                    templates[os.path.basename(root)] = f.read()
    template_loader = jinja2.DictLoader(templates)
    template_env = jinja2.Environment(loader=template_loader, autoescape=False)

    for one in config:
        for one_version in one["versions"]:
            one_version = str(one_version)
            vars = dict(one)
            del vars["versions"]
            vars["version"] = one_version
            if 'url' in vars:
                vars["url"] = vars["url"].format(version=one_version)
            else:
                vars["url"] = "dummy"

            if "filename" in vars:
                vars["filename"] = vars["filename"].format(
                    version=one_version)
            else:
                vars["filename"] = os.path.basename(
                    urllib.parse.urlparse(vars["url"]).path)

            if "archivename" in vars:
                vars["archivename"] = vars["archivename"].format(
                    version=one_version)
            else:
                vars["archivename"] = vars["filename"]
                expected = {".tar.gz", ".tar.bz2", ".tar.xz",
                            ".zip", ".tgz", ".tbz", ".txz"}
                for extension in expected:
                    if vars["archivename"].endswith(extension):
                        vars["archivename"] = vars["archivename"][:-
                                                                  len(extension)]
            x = template_env.get_template(vars["type"])

            os.makedirs(os.path.join(options.output,
                                     one_version), exist_ok=True)
            with open(os.path.join(options.output, one_version, "Dockerfile"), "w") as f:
                print(
                    "# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT BY HAND", file=f)
                print("# template file is {}".format(vars['type']), file=f)
                f.write(x.render(**vars))

            if 'patch' in vars:
                for one_patch in vars["patch"]:
                    shutil.copyfile(os.path.join(
                        os.path.dirname(options.config.name), one_patch), os.path.join(options.output, one_version, one_patch))

            if options.build:
                subprocess.check_call(["docker", "build", "-t",
                                       "{username}/{name}:{version}".format(
                                           username=options.username, name=vars["name"], version=one_version),
                                       os.path.join(options.output, one_version)])


if __name__ == '__main__':
    _main()