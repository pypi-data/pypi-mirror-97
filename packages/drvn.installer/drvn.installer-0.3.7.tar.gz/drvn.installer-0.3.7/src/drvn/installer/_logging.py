import logging


def configure(log_level):
    logging.basicConfig(
        format="[%(asctime)s.%(msecs)03d %(levelname)s %(module)s]: %(message)s",
        datefmt="%H:%M:%S",
        level=log_level,
    )
