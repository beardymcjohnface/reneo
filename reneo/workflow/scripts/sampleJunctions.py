import logging
import sys
from reneo_utils.coverage_utils import read_pair_generator
from collections import defaultdict
import pysam
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


def find_links_in_bam(**kwargs):
    """Return a dictionary of contig pairs and their PE junction counts"""
    link_counts = defaultdict(int)

    bam_file = pysam.AlignmentFile(kwargs["bam"], "rb")
    read_pairs = read_pair_generator(bam_file)

    for read1, read2 in read_pairs:
        if read1.reference_name != read2.reference_name:
            link_counts[(read1.reference_name, read2.reference_name)] += 1

    return link_counts


def pickle_and_dump(**kwargs):
    """Write a pickle file of the dictionary of contig pairs and their PE junction counts"""
    with open(kwargs["out"], "wb") as handle:
        pickle.dump(kwargs["links"], handle, protocol=pickle.HIGHEST_PROTOCOL)


def main(**kwargs):
    logger = setup_logging(**kwargs)

    logger.info(f"Finding junctions for {kwargs['smpl']}")
    kwargs["links"] = find_links_in_bam(**kwargs)

    logger.info("Writing junctions to pickle file")
    pickle_and_dump(**kwargs)

    logger.info("Done!")
    sys.exit(0)


if __name__ == "__main__":
    main(
        bam=snakemake.input.bam,
        out=snakemake.output.pkl,
        smpl=snakemake.wildcards.sample,
        log=snakemake.log.err
    )