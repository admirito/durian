#!/usr/bin/env python
#
# Durian Debian Deployer
# Originally Developed by Mohammad Razavi <mrazavi64 at gmail dot com>
#

"""\
Durian Debian Deployer is a program to preconfigure and deploy a
customized debian/ubuntu installation.
"""

import os, sys, re, subprocess
from optparse import OptionParser

__version__ = "1.0.0"

def get_path(*paths):
    return ":".join([os.path.abspath(i) for i in paths])

os.environ.setdefault("PLUGINS_PATH", get_path( \
    os.path.expanduser("~/.durian/plugins"), "/var/lib/durian/plugins", \
    "/usr/share/durian/plugins", "./plugins"))

os.environ.setdefault("SEEDS_PATH", get_path( \
    os.path.expanduser("~/.durian/seeds"), "/var/lib/durian/seeds", \
    "/usr/share/durian/seeds", "./seeds"))

os.environ.setdefault("MIRRORS_PATH", get_path( \
    os.path.expanduser("~/.durian/mirrors"), "/var/lib/durian/mirrors", \
    "/usr/share/durian/mirrors", "./mirrors"))

os.environ.setdefault("DEFINITIONS_PATH", get_path( \
    os.path.expanduser("~/.durian/definitions"), \
    "/var/lib/durian/definitions", "/usr/share/durian/definitions", \
    "./definitions"))

os.environ.setdefault("THEME_PATH", "/usr/share/durian/themes/durian")

os.environ.setdefault("DURIAN_EXE", os.path.abspath(sys.argv[0]))

def parse_version(text):
    atoi = lambda text: int(text) if text.isdigit() else text
    digit_rx = re.compile(r"(\d+)")
    return [atoi(c) for c in digit_rx.split(text)]

def find_plugins():
    """\
    Returns a dictionary with commands as the key and another dictionary
    as the value. The value dictionary containts "path", "description" and
    "version" and "minimum durian version".
    """
    plugins = {}

    for plugin_path in os.environ.get("PLUGINS_PATH", "").split(":"):
        try:
            for filename in os.listdir(plugin_path):
                fullpath = os.path.join(plugin_path, filename)
                if not os.access(fullpath, os.X_OK): continue

                try:
                    # call the executable with --version
                    # if its output is a couple of "key: value" lines,
                    # one of them "minimum durian version: x.y.z"
                    # we accept it as a plugin
                    p = subprocess.Popen([fullpath, "--version"], \
                                         stdout = subprocess.PIPE, \
                                         stderr = subprocess.PIPE)
                    stdout, stderr = p.communicate()

                    info = {"name": filename, "path": fullpath}
                    info.update(re.findall(r"^\s*([^:\n]+?)\s*:\s*(.*?)\s*$", \
                                           stdout, flags = re.MULTILINE))
                    if parse_version(info["minimum durian version"]) > \
                       parse_version(__version__):
                        continue

                except Exception:
                    continue

                else:
                    plugins[info["name"]] = info

        except Exception:
            continue

    return plugins

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--plugins-path", dest = "plugins_path", \
                      type = "string", default = "", \
                      help = "add PATH to plugins path", metavar="PATH")
    parser.add_option("--seeds-path", dest = "seeds_path", \
                      type = "string", default = "", \
                      help = "add PATH to seeds path", metavar="PATH")
    parser.add_option("--mirrors-path", dest = "mirrors_path", \
                      type = "string", default = "", \
                      help = "add PATH to mirror profiles path", \
                      metavar="PATH")
    parser.add_option("--definitions-path", dest = "definitions_path", \
                      type = "string", default = "", \
                      help = "add PATH to definitions path", \
                      metavar="PATH")
    parser.add_option("-l", "--list-commands", dest = "list_commands", \
                      action = "store_true", default = False, \
                      help = "Print list of supported durian commands " \
                      "and exit")
    parser.add_option("-v", "--version", dest = "version", \
                      action = "store_true", default = False, \
                      help = "Print durian version and exit")

    parser.set_description(__doc__)
    parser.set_usage("durian [-v|--version] [-h|--help] [-l|--list-commands] " \
                     "[--plugins-path=<path>] [--seeds-path=<path>] " \
                     "<command> <args>")

    args = [i for i in sys.argv[1:] if not i.startswith("-")]
    command_position = sys.argv.index(args[0]) if args else len(sys.argv)

    OPTIONS, ARGS = parser.parse_args(sys.argv[1:command_position])

    command = sys.argv[command_position] \
              if len(sys.argv) > command_position else None
    command_args = sys.argv[command_position + 1:]

    for path, variable_name in [(OPTIONS.plugins_path, "PLUGINS_PATH"), \
                                (OPTIONS.seeds_path, "SEEDS_PATH"), \
                                (OPTIONS.definitions_path, \
                                 "DEFINITIONS_PATH"), \
                                (OPTIONS.mirrors_path, "MIRRORS_PATH")]:
        if not path: continue

        try:
            os.listdir(path)
        except Exception as e:
            sys.stderr.write("{0}\n".format(e))
            exit(1)
        else:
            os.environ[variable_name] = ":".join([path, \
                                         os.environ.get(variable_name, "")])

    if OPTIONS.version:
        sys.stdout.write("{0}\n".format(__version__))
        exit(0)

    plugins = {"help": {"desctiption": "print information about the "\
                        "given command"}}
    plugins.update(find_plugins())

    if OPTIONS.list_commands:
        sys.stdout.write("{0}\n".format("\n".join(plugins.keys())))
        exit(0)

    if not command:
        parser.print_help()
        sys.stdout.write("\nAvailable commands:\n")
        sys.stdout.write("\n".join("{0:<15} {1}".format(name, \
                                                     info.get("desctiption")) \
                                   for name, info in sorted(plugins.items())))
        sys.stdout.write("\n")
        exit(0)

    if command == "help":
        if len(command_args) == 1:
            if command_args[0] == "help" and "path" not in plugins["help"]:
                sys.stdout.write("{0}\n" \
                                 .format(plugins["help"]["desctiption"]))
                exit(0)

            command = command_args[0]
            command_args = ["--help"]

        else:
            sys.stderr.write("You should specify a command.\n")
            exit(1)

    if command in plugins:
        plugin_info = plugins[command]
        plugin_path = plugin_info["path"]
        retcode = subprocess.call([plugin_path] + command_args)
        exit(retcode)

    else:
        sys.stderr.write("Invalid command: `{0}'\n".format(command))
        exit(1)
