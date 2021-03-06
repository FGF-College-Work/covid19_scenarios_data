import sys
import argparse
import os
import json
import importlib
from paths import BASE_PATH, SOURCES_FILE, JSON_DIR, TMP_CASES, TMP_POPULATION

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "",
                                     usage="Parse data and copy output to app")

    parser.add_argument('--fetch', action='store_true', help='update sources from remote')
    parser.add_argument('--parsers', nargs='+', help='parsers to run')
    parser.add_argument('--output-cases', type=str, default=None, help='path to case-counts file')
    parser.add_argument('--output-population', type=str, default=None, help='path to population file')
    parser.add_argument('--output-scenarios', type=str, default=None, help='path to scenarios file')
    parser.add_argument('--num-threads', type=int, default=1, help='number of threads to open for fitting')
    args = parser.parse_args()

    if not os.path.isdir(BASE_PATH):
        print(f"This repo expects to sit inside a directory names '{BASE_PATH}'. "
               "Please check and either rename the directory or change BASE_PATH in "
               "the file 'paths.py'.")
        sys.exit()

    if args.fetch:
        srcs = list(json.load(open(os.path.join(BASE_PATH, SOURCES_FILE))).keys())
        for src in srcs:
            # Allow running this as `python3 covid19_scenarios_data/generate_data.py --fetch --parsers netherlands` to filter sources (debug mode)
            if (args.parsers is None) or src in args.parsers:
                print(f"Running {src} to generate .tsv", file=sys.stderr)
                country = importlib.import_module(f"parsers.{src}")
                country.parse()
                
    # generate and copy jsons to app if requested
    if args.output_cases:
        print(f"Generating cases json")
        pop = importlib.import_module(f"scripts.tsv")
        pop.parse(args.output_cases)


    if args.output_population:
        print(f"Generating population json")
        pop = importlib.import_module(f"scripts.populations")
        pop.generate(args.output_population)

    if args.output_scenarios:
        print(f"Generating scenario json")
        scenarios = importlib.import_module(f"scripts.scenarios")
        scenarios.generate(args.output_scenarios, num_procs=args.num_threads)
