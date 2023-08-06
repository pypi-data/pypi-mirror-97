import os

import click
from controller.compose import Compose
from langauge.utils import cli_args
import dotenv

_ROOT = os.path.abspath(os.path.dirname(__file__))


@click.group(chain=True)
def cli():
    pass


# @cli.command()
# def ui():
#     subprocess.call("npm start", shell=True, cwd='ui/')
#     print("In UI")


@cli.command()
@cli_args.HOST
@cli_args.PORT
@cli_args.BACKEND
def ui(host, port, backend):
    dotenv_file = dotenv.find_dotenv(filename=os.path.join(_ROOT, 'ui', '.env'))
    dotenv.load_dotenv(dotenv_file)
    dotenv.set_key(dotenv_file, "HOST", host)
    dotenv.set_key(dotenv_file, "PORT", port)
    dotenv.set_key(dotenv_file, "REACT_APP_BASE_URL", 'http://'+backend)
    dc = Compose(files=[os.path.join(_ROOT, 'docker-compose.yml')])
    options = {
        "-d": True,
        "--no-color": True,
        "--quiet-pull": True,
        "--no-deps": True,
        "--force-recreate": True,
        "--always-recreate-deps": True,
        "--no-recreate": False,
        "--no-build": False,
        "--no-start": False,
        "--build": True,
        "--abort-on-container-exit": False,
        "--attach-dependencies": False,
        "--renew-anon-volumes": True,
        "--remove-orphans": True,
        "SERVICE": ["ui"],
        "--scale": ["service=1"]
    }
    dc.command('up', options)


@cli.command()
@cli_args.BACKENDPORT
def backend(backendport):
    dotenv_file = dotenv.find_dotenv(filename=os.path.join(_ROOT, '.env'))
    dotenv.load_dotenv(dotenv_file)
    dotenv.set_key(dotenv_file, "PORT", backendport)
    dc = Compose(files=[os.path.join(_ROOT, 'docker-compose.yml')])
    options = {
        "-d": True,
        "--no-color": True,
        "--quiet-pull": True,
        "--no-deps": True,
        "--force-recreate": True,
        "--always-recreate-deps": True,
        "--no-recreate": False,
        "--no-build": False,
        "--no-start": False,
        "--build": True,
        "--abort-on-container-exit": False,
        "--attach-dependencies": False,
        "--renew-anon-volumes": True,
        "--remove-orphans": True,
        "SERVICE": ["service", "worker", "redis", "monitor", "runner", "database"],
        "--scale": ["service=1"]
    }
    dc.command('up', options)


@cli.command()
def down():
    dc = Compose(files=[os.path.join(_ROOT, 'docker-compose.yml')])
    options = {
        "--rmi": "all",
        "--volumes": [],
        "--remove-orphans": True
    }
    dc.command('down', options)

