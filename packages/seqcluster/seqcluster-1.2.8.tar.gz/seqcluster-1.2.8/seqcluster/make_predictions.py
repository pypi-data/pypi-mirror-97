import os
import logging

from seqcluster.libs.read import load_data, write_data
from seqcluster.function.predictions import is_tRNA, run_coral
from seqcluster.libs.utils import safe_dirs

logger = logging.getLogger('predictions')


def predictions(args):
    """
    Create predictions of clusters
    """

    logger.info(args)
    logger.info("Reading sequences")
    out_file = os.path.abspath(os.path.splitext(args.json)[0] + "_prediction.json")
    data = load_data(args.json)
    out_dir = os.path.abspath(safe_dirs(os.path.join(args.out, "predictions")))

    logger.info("Make predictions")
    data = is_tRNA(data, out_dir, args)

    if args.coral:
        logger.info("Make CoRaL predictions")
        run_coral(data, out_dir, args)
    write_data(data[0], out_file)
    logger.info("Done")
