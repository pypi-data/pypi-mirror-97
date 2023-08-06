import pathlib
import subprocess


def __init__(hub):
    templates = pathlib.Path(__file__).parent / "_templates"
    # Add all the template files to the hub under their base file_name all uppercase under hub.pop_create.docs
    for template in templates.iterdir():
        if template.is_dir():
            continue
        attr = (
            template.stem.upper().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        contents = template.read_text()
        setattr(hub.pop_create.docs, attr, contents)


def new(hub, name: str, directory: pathlib.Path, **kwargs):
    docs_dir = directory / "docs"
    author = subprocess.getoutput("git config --global user.name")
    clean_name = kwargs.get("clean_name", name)

    hub.pop_create.init.write(
        docs_dir / "make.bat",
        contents=hub.pop_create.docs.MAKE,
        replace={"R__NAME__": name},
    )
    hub.pop_create.init.write(
        docs_dir / "Makefile",
        contents=hub.pop_create.docs.MAKEFILE,
        replace={"R__NAME__": name},
    )
    outline_header = f"{name.title()} Docs Outline"
    eqchars = "=" * len(outline_header)
    hub.pop_create.init.write(
        docs_dir / "outline.rst",
        contents=f"{eqchars}\n{outline_header}\n{eqchars}\n\nA description of my project",
    )
    hub.pop_create.init.write(
        docs_dir / "source" / "conf.py",
        contents=hub.pop_create.docs.CONF,
        replace={
            "R__AUTHOR__": author,
            "R__NAME__": name,
            "R__CLEAN_NAME__": clean_name,
        },
    )
    welcome_header = f"Welcome to {name}'s Documentation!"
    eqchars = "=" * len(welcome_header)
    hub.pop_create.init.write(
        docs_dir / "source" / "index.rst",
        contents=hub.pop_create.docs.INDEX,
        replace={
            "R__CLEAN_NAME__": clean_name,
            "R__WELCOME__": f"{welcome_header}\n{eqchars}\n",
        },
    )
    release_header = f"{name} Release 1.0.0"
    eqchars = "=" * len(release_header)
    hub.pop_create.init.write(
        docs_dir / "source" / "releases" / "1.0.0.rst",
        contents=hub.pop_create.docs.FIRST_RELEASE,
        replace={"R__HEADER__": f"{eqchars}\n{release_header}\n{eqchars}"},
    )
    title = clean_name.replace("_", " ").title()
    eqchars = "=" * len(title)
    hub.pop_create.init.write(
        docs_dir / "source" / "topics" / f"{clean_name}.rst",
        contents=f"{title}\n{eqchars}\n\nA description of my project",
    )
    hub.pop_create.init.write(
        docs_dir / "source" / "tutorial" / "quickstart.rst",
        contents=hub.pop_create.docs.QUICKSTART,
        replace={"R__NAME__": name},
    )
