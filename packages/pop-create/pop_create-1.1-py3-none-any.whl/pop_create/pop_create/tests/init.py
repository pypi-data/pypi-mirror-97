import pathlib

TESTS = "tests"
UNIT = "unit"
INTEGRATION = "integration"


def __init__(hub):
    templates = pathlib.Path(__file__).parent / "_templates"
    # Add all the template files to the hub under their base file_name all uppercase under hub.pop_create.tests
    for template in templates.iterdir():
        if template.is_dir():
            continue
        attr = (
            template.stem.upper().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        contents = template.read_text()
        setattr(hub.pop_create.tests, attr, contents)


def new(hub, name: str, directory: pathlib.Path, **kwargs):
    test_dir = directory / TESTS

    clean_name = kwargs.get("clean_name", name)
    dynes = kwargs.get("dynes", ())

    hub.pop_create.init.write(
        directory / "requirements" / "tests.in", contents=hub.pop_create.tests.TESTS,
    )
    hub.pop_create.init.write(
        directory / ".pre-commit-config.yaml",
        contents=hub.pop_create.tests.PRE_COMMIT_CONFIG,
    )
    hub.pop_create.init.write(
        test_dir / UNIT / "conftest.py",
        contents=hub.pop_create.tests.UNIT_CONFTEST,
        replace={"R__CLEAN_NAME__": clean_name},
    )
    hub.pop_create.init.write(
        test_dir / INTEGRATION / "conftest.py",
        contents=hub.pop_create.tests.INTEGRATION_CONFTEST,
        replace={"R__NAME__": name, "R__CLEAN_NAME__": clean_name},
    )

    # Vertically app-merged projects won't have an entrypoint for this test
    if not kwargs.get("vertical"):
        hub.pop_create.init.write(
            test_dir / UNIT / clean_name / "test_seed.py",
            contents=hub.pop_create.tests.UNIT,
            replace={"R__CLEAN_NAME__": clean_name},
        )
        hub.pop_create.init.write(
            test_dir / INTEGRATION / clean_name / "test_seed.py",
            contents=hub.pop_create.tests.INTEGRATION,
            replace={"R__CLEAN_NAME__": clean_name},
        )

    for dyne in dynes:
        (test_dir / UNIT / dyne).mkdir(parents=True, exist_ok=True)
        (test_dir / INTEGRATION / dyne).mkdir(parents=True, exist_ok=True)

    # Make sure that all the directories under "test" are considered modules
    test_paths = {x for x in hub.pop_create.WRITES.keys()}
    for d in test_paths:
        if any(p.name == TESTS for p in d.parents):
            hub.pop_create.init.write(d.parent / "__init__.py", contents="")
    hub.pop_create.init.write(test_dir / "__init__.py", contents="")
