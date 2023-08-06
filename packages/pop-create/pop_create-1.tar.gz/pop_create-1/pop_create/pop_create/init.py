import aiofiles
import pathlib
from typing import Dict


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.pop_create, recurse=True)
    # Hold onto all the writes that should be done until exist checks have been done
    hub.pop_create.WRITES = {}


def cli(hub):
    hub.pop.config.load(["pop_create"], cli="pop_create")
    directory = pathlib.Path(hub.OPT.pop_create.directory)
    name = hub.OPT.pop_create.project_name or directory.name
    if not hub.SUBPARSER:
        # No subparser specified, do everything!
        for subparser in ("seed", "cicd", "docs", "tests"):
            hub.pop_create[subparser].init.new(
                name=name,
                directory=directory,
                vertical=hub.OPT.pop_create.vertical,
                dynes=hub.OPT.pop_create.dyne,
            )
    else:
        subparser = hub.SUBPARSER.replace("-", "_")
        hub.pop_create[subparser].init.new(
            name=name,
            directory=directory,
            vertical=hub.OPT.pop_create.vertical,
            dynes=hub.OPT.pop_create.dyne,
        )
    hub.pop_create.init.flush()


def write(
    hub,
    path: pathlib.Path,
    contents: str,
    replace: Dict[str, str] = None,
):
    # Perform substitutions
    if replace:
        for key, value in replace.items():
            contents = contents.replace(key, value)

    if not hub.OPT.pop_create.ignore_empty_warning and path.exists():
        raise FileExistsError(f"Target is not empty: {path}")

    hub.pop_create.WRITES[path] = contents


def flush(hub):
    for path, content in hub.pop_create.WRITES.items():
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)
    hub.pop_create.WRITES.clear()
