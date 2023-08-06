import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.warning('This is a dummy placeholder for the SparkBeyond Python SDK.'
                   'The actual SDK can be installed directly from your Discovery Platform server.'
                   'For further information, please contact support@sparkbeyond.com')
