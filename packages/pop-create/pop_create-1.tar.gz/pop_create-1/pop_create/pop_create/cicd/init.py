import pathlib


def __init__(hub):
    templates = pathlib.Path(__file__).parent / "_templates"
    # Add all the template files to the hub under their base file_name all uppercase under hub.pop_create.cicd
    for template in templates.iterdir():
        if template.is_dir():
            continue
        attr = (
            template.stem.upper().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        contents = template.read_text()
        setattr(hub.pop_create.cicd, attr, contents)


def new(hub, name: str, directory: pathlib.Path, **kwargs):
    clean_name = name.replace("-", "_").replace(" ", "_")
    hub.pop_create.init.write(
        directory / "build.conf", contents=hub.pop_create.cicd.BUILD,
    )
    hub.pop_create.init.write(
        directory / ".coveragerc",
        contents=hub.pop_create.cicd.COVERAGERC,
        replace={"R__CLEAN_NAME__": clean_name},
    )
    hub.pop_create.init.write(
        directory / ".gitlab-ci.yml", contents=hub.pop_create.cicd.GITLAB_CI,
    )
    hub.pop_create.init.write(
        directory / ".pre-commit-config.yaml",
        contents=hub.pop_create.cicd.PRE_COMMIT_CONFIG,
    )
    hub.pop_create.init.write(
        directory / "noxfile.py",
        contents=hub.pop_create.cicd.NOXFILE,
        replace={"R__CLEAN_NAME__": clean_name},
    )
    hub.pop_create.init.write(
        directory / "cicd" / "upload-code-coverage.sh",
        contents=hub.pop_create.cicd.UPLOAD_CODE_COVERAGE,
    )
