import os
import shutil
import logging

#try:
#    from bcbio.install import _set_matplotlib_default_backend
#    _set_matplotlib_default_backend()
#except (ImportError, OSError, IOError):
#    pass
#import matplotlib
#matplotlib.use('Agg', force=True)

from seqcluster.libs.read import load_data
from seqcluster.libs.report import make_profile
from seqcluster.libs.utils import safe_dirs
from seqcluster.db import make_database
from seqcluster import templates

logger = logging.getLogger('report')


def report(args):
    """
    Create report in html format
    """
    logger.info("Reading sequences")
    data = load_data(args.json)

    profilesDir=os.path.join(args.out, "profiles")
    logger.info("Creating profile (%s)" % profilesDir)
    data = make_profile(data, profilesDir, args)
    logger.info("Creating database")
    make_database(data, "seqcluster.db", args.out)

    logger.info("Done. Download https://github.com/lpantano/seqclusterViz/archive/master.zip to browse the output.")
