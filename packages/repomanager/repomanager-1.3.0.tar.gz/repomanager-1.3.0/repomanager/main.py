# See LICENSE.incore for license details
import logging
import os
import sys
import shutil


from repomanager import __version__ as version
import repomanager.utils as utils
import repomanager.rpm as repoman

def main():
    '''
        Entry point for riscv_config.
    '''

    # Set up the parser
    parser = utils.repomanager_cmdline_args()
    args = parser.parse_args()

    # Set up the logger
    utils.setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(utils.ColoredFormatter())
    logger.addHandler(ch)

    logger.info('################### Repository Manager ##################')
    logger.info('--- Copyright (c) 2020 InCore Semiconductors Pvt. Ld. ---')
    logger.info('------------------- Version : {0} ---------------------'.format(version))
    logger.info('#########################################################')
    logger.info('\n')

    yml_str = open(args.yaml,'r').read()
    repoman.repoman(yml_str, args.clean, args.update, args.patch,
            args.unpatch, args.dir)
    
if __name__ == "__main__":
    exit(main())
