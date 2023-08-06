import multiprocessing
import argparse
import configparser

from gunicorn.app.base import BaseApplication

from taky import __version__
from taky.config import load_config
from taky.dps import app as taky_dps


class StandaloneApplication(BaseApplication):
    # 'init' and 'load' methods are implemented by WSGIApplication.
    # pylint: disable=abstract-method

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def arg_parse():
    argp = argparse.ArgumentParser(description="Taky command line utility")
    argp.add_argument(
        "-c",
        action="store",
        dest="cfg_file",
        default=None,
        help="Path to configuration file",
    )
    argp.add_argument(
        "-l",
        action="store",
        dest="log_level",
        default="INFO",
        help="Path to configuration file",
    )
    argp.add_argument(
        "--version", action="version", version="%%(prog)s version %s" % __version__
    )

    args = argp.parse_args()

    return (argp, args)


def main():
    """
    Runs the DPS, handy for avoiding a specific gunicorn setup
    """
    (argp, args) = arg_parse()

    try:
        config = load_config(args.cfg_file)
    except (OSError, configparser.ParsingError) as exc:
        argp.error(exc)

    bind_ip = config.get("taky", "bind_ip")
    port = 8443 if config.getboolean("ssl", "enabled") else 8080

    if bind_ip is None:
        argp.error("Server not configured...")

    options = {
        "bind": f"{bind_ip}:{port}",
        "workers": number_of_workers(),
        "loglevel": args.log_level,
    }
    if config.getboolean("ssl", "enabled"):
        options["ca-certs"] = config.get("ssl", "ca")
        options["certfile"] = config.get("ssl", "cert")
        options["keyfile"] = config.get("ssl", "key")
        # options['cert_reqs'] = ssl.VerifyMode.CERT_REQUIRED

    StandaloneApplication(taky_dps, options).run()
    print("DONE")


if __name__ == "__main__":
    main()
