import functools
import logging
import signal


def handle_signal(server, ioloop, signum, frame):
    logging.info("Received signal {}; shutting down...".format(signum))

    def stop_ioloop():
        logging.info("Stopping IOLoop")
        ioloop.stop()

    def stop_server():
        logging.info("Stopping HTTPServer")
        server.stop()
        ioloop.call_later(2, stop_ioloop)

    if server is None:
        ioloop.add_callback_from_signal(stop_ioloop)
    else:
        ioloop.add_callback_from_signal(stop_server)


def on_sigterm(server, ioloop):
    """Shut down server and ioloop when SIGTERM signal is received.

    The server may be None, in which case only the ioloop is stopped on SIGTERM.

    If the server is not None, it will be stopped, first, and then the ioloop will be stopped two
    seconds later.
    """

    signal.signal(signal.SIGTERM, functools.partial(handle_signal, server, ioloop))
