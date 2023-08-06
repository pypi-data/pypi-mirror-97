import sys
import argparse
from mapula.count import CountMappingStats
from mapula.merge import MergeMappingStats

USAGE = (
    """mapping-stats <command> [<args>]"

Available subcommands are:
    count        Count mapping stats from a SAM/BAM file
    merge        Combine mapula count's aggregated json outputs
""")


class MappingStats(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Collects stats from SAM/BAM files",
            usage=USAGE
        )

        parser.add_argument("command", help="Subcommand to run")

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)

        getattr(self, args.command)(sys.argv[2:])

    def count(self, argv):
        CountMappingStats.execute(argv)

    def merge(self, argv):
        MergeMappingStats.execute(argv)


def run_main():
    MappingStats()


if __name__ == "__main__":
    run_main()
