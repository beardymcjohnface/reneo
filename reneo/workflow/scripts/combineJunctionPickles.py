import logging
import sys
from collections import defaultdict
import pickle


__author__ = "Michael Roach"
__copyright__ = "Copyright 2022, Reneo Project"
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Vijini Mallawaarachchi"
__email__ = "viji.mallawaarachchi@gmail.com"
__status__ = "Development"


def setup_logging(**kwargs):
    """Setup logging"""
    logger = logging.getLogger(__version__)
    logger.setLevel(logging.DEBUG)
    logging.captureWarnings(True)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    consoleHeader = logging.StreamHandler()
    consoleHeader.setFormatter(formatter)
    consoleHeader.setLevel(logging.INFO)
    logger.addHandler(consoleHeader)
    fileHandler = logging.FileHandler(kwargs["log"])
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger


def combine_junction_pickles(**kwargs):
    """Read in all the sample junction pickle files and combine the counts"""
    all_counts = defaultdict(int)

    for pickle_file in kwargs["pkls"]:
        with open(pickle_file, "rb") as handle:
            sample_counts = pickle.load(handle)
            for ctgs, count in sample_counts.items():
                all_counts[ctgs] += count

    return all_counts


def pickle_and_dump(**kwargs):
    """Write a pickle file of the dictionary of contig pairs and their PE junction counts"""
    with open(kwargs["out"], "wb") as handle:
        pickle.dump(kwargs["links"], handle, protocol=pickle.HIGHEST_PROTOCOL)


def main(**kwargs):
    logger = setup_logging(**kwargs)

    logger.info(f"Combining junctions")
    kwargs["links"] = combine_junction_pickles(**kwargs)

    logger.info("Writing combined pickle file")
    pickle_and_dump(**kwargs)

    logger.info("Done!")
    sys.exit(0)


if __name__ == "__main__":
    main(
        pkls=snakemake.input.pkls,
        out=snakemake.output.pkl,
        log=snakemake.log.err
    )