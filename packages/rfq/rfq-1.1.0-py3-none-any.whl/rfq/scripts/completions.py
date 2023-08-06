# Writing completions by hand seems to be the quick
# way here, but it's not nice to do this at all :'(

def bash():
    cmds = " ".join([
        "version",
        "info",
        "list-topics",
        "list-queue",
        "purge-queue",
        "publish",
        "consume",
        "harvest",
        "completions",
    ])

    return f"complete -W '{cmds}' rfq"

def main(args):
    shells = { "bash": bash }

    shell = shells[args.shell]
    compl = shell()

    print(compl)
