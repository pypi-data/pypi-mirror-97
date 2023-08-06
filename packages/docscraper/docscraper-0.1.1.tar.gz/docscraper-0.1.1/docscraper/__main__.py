import argparse
from .spider import crawl


def parse_arguments():
    """ Parse and return command-line arguments.
    :return: An argparse namespace object containing the command-line
    argument values.
    :rtype: argparse.Namespace

    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--allowed_domains", nargs="+",
                        help="one or more allowed domains", required=True)

    parser.add_argument("-s", "--start_urls", nargs="+",
                        help="one or more start urls", required=True)

    parser.add_argument("-d", "--directory", help="directory path for output.",
                        default="./output")

    parser.add_argument("-e", "--extensions", nargs="*",
                        help="one or more document extensions (e.g., '.pdf')")

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_arguments()

    if args.extensions is None:
        args.extensions = ['.pdf', '.doc', '.docx']

    crawl(args.allowed_domains, args.start_urls,
          args.directory, args.extensions)

