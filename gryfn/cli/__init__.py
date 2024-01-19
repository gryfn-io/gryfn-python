import argparse
import json

arguments = argparse.ArgumentParser(
    description='Run custom processing module for your GPros.')


def FileString(argstring):
    return repr(argstring).strip("'")


def GPro(argstring):
    from gryfn import GPro
    return GPro(repr(argstring).strip("'"))



arguments.add_argument('--gpro', type=GPro, help="location of gpro to process")

# Inspect call is to be used by front-end UI for determining how to
# display the arguments to the user in a graphical front end
arguments.add_argument("--inspect", action='store_true', help=argparse.SUPPRESS)


def parse_args():
    args = arguments.parse_args()
    if args.inspect:
        script_args = []
        for a in arguments._action_groups:
            for ga in a._group_actions:
                if ga.type:
                    script_args.append({
                        "argument": ga.option_strings[0],
                        "type": ga.type.__name__,
                        "default": ga.default,
                        "help":  ga.help})
        print(json.dumps(script_args))
        exit(0)
    if not args.gpro:
        raise Exception("Could not find gpro '%s' on file system" % args.gpro)
    return args
