"""Fixes common make rule typos by regular expression
matching over the result of `make -qp` like
bash-completion tab.

Example:
> make clen
make: *** No rule to make target `clen'.  Stop.

"""
from thefuck.utils import for_app, get_closest

@for_app('make')
def match(command):
    return command.stderr.__contains__("No rule to make target")


def get_new_command(command):
    if len(command.script_parts) <= 1:
        return []

    badrule = command.script_parts[1]

    from subprocess import call, Popen, PIPE

    proc = Popen(["make", "-qp"], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = proc.communicate()

    import re
    matcher = re.compile(r'^[a-zA-Z0-9][^$#/\t=]*:([^=$])*$', re.MULTILINE)
    possibilities = []

    for s in stdout.split("\n"):
        res = matcher.match(s)
        if res:
            possibilities.append(res.group(0).split(":")[0])

    return ['make ' + get_closest(badrule, possibilities, 5)]
