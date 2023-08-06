import argparse
import logging
import sys

from gitlab_versioned_pages import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    parser.add_argument("--url")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--job-name", default=None)
    parser.add_argument("--private-token", default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    sys.exit(main(args))
