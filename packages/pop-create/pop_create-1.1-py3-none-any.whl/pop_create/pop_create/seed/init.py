"""
Seed a new project with a directory tree and first files
"""
import pathlib
import subprocess

COMPLETION_TEXT = """
Congratulations! You now have a project set up called {name}!
This project can be executed by calling the run.py script:
    python3 run.py
This project has been set up with pre-commit hooks for code checks and black.
First set up your source control environment with "git init" or "hg init".
Then enable these checks in your git checkout:
    pip install pre-commit
    pre-commit install
To run pre-commit manually, execute:
    pre-commit run --all-files
Please fork the pop-awesome and open a PR listing your new project \u263A
    https://gitlab.com/saltstack/pop/pop-awesome
"""


def __init__(hub):
    templates = pathlib.Path(__file__).parent / "_templates"
    # Add all the template files to the hub under their base file_name all uppercase under hub.pop_create.seed
    for template in templates.iterdir():
        if template.is_dir():
            continue
        attr = (
            template.stem.upper().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        contents = template.read_text()
        setattr(hub.pop_create.seed, attr, contents)


def new(hub, name: str, directory: pathlib.Path, **kwargs):
    """
    Given the option in hub.opts "project_name" create a directory tree for a
    new pop project
    """
    author = subprocess.getoutput("git config --global user.name")
    author_email = subprocess.getoutput("git config --global user.email")
    clean_name = kwargs.get("clean_name", name)
    vertical = kwargs.get("vertical")

    dynes = list(kwargs.get("dynes", ()))
    if not vertical:
        dynes.append(clean_name)

    dynes = sorted(dynes)

    for dyne in dynes:
        (directory / clean_name / dyne / "contracts").mkdir(parents=True, exist_ok=True)

    dyne_str = ",\n".join(" " * 4 + f'"{dyne}": ["{dyne}"]' for dyne in dynes)
    hub.pop_create.init.write(
        directory / clean_name / "conf.py",
        contents=hub.pop_create.seed.CONF,
        replace={'"R__DYNE__"': f"\n{dyne_str}\n"},
    )
    hub.pop_create.init.write(
        directory / clean_name / "version.py", contents=hub.pop_create.seed.VERSION,
    )
    eqchars = "=" * len(name)
    readme_str = f"{eqchars}\n{name.upper()}\n{eqchars}\n"
    hub.pop_create.init.write(
        directory / "README.rst",
        contents=readme_str,
        replace={"R__NAME__": clean_name},
    )
    hub.pop_create.init.write(
        directory / "requirements" / "base.txt", contents=hub.pop_create.seed.BASE
    )
    hub.pop_create.init.write(
        directory / "LICENSE",
        contents=hub.pop_create.seed.LICENSE,
        replace={"R__AUTHOR__": author},
    )
    hub.pop_create.init.write(
        directory / ".pyproject.toml", contents=hub.pop_create.seed.PYPROJECT
    )
    hub.pop_create.init.write(
        directory / ".pre-commit-config.yaml",
        contents=hub.pop_create.seed.PRE_COMMIT_CONFIG,
    )
    hub.pop_create.init.write(
        directory / ".gitignore", contents=hub.pop_create.seed.GITIGNORE
    )

    if kwargs.get("vertical"):
        hub.pop_create.init.write(
            directory / "setup.py",
            contents=hub.pop_create.seed.SETUP,
            replace={
                "R__NAME__": name,
                "R__CLEAN_NAME__": clean_name,
                "R__ENTRY__": "",
                "R__AUTHOR__": author,
                "R__AUTHOR_EMAIL__": author_email,
            },
        )
    else:
        (directory / clean_name / clean_name / "contracts").mkdir(
            parents=True, exist_ok=True
        )
        hub.pop_create.init.write(
            directory / "setup.py",
            contents=hub.pop_create.seed.SETUP,
            replace={
                "R__NAME__": name,
                "R__CLEAN_NAME__": clean_name,
                "R__AUTHOR__": author,
                "R__AUTHOR_EMAIL__": author_email,
                "R__ENTRY__": f"{name} = {clean_name}.scripts:start",
            },
        )
        hub.pop_create.init.write(
            directory / clean_name / "scripts.py",
            contents=hub.pop_create.seed.SCRIPT,
            replace={"R__NAME__": clean_name},
        )
        hub.pop_create.init.write(
            directory / "run.py",
            contents=hub.pop_create.seed.RUN,
            replace={"R__NAME__": clean_name},
        )
        hub.pop_create.init.write(
            directory / clean_name / clean_name / "init.py",
            contents=hub.pop_create.seed.INIT,
            replace={"R__NAME__": name, "R__CLEAN_NAME__": clean_name},
        )

    print(COMPLETION_TEXT)
