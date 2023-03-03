import logging

def configureLogger(args):
    logging.basicConfig(format="(%(msecs)d:%(filename)s:%(funcName)s:%(lineno)d) [%(levelname)s] %(message)s")
    logger = logging.getLogger()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    return logger
