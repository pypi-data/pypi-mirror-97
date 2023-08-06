import pathlib


def __init__(hub):
    templates = pathlib.Path(__file__).parent / "_templates"
    # Add all the template files to the hub under their base file_name all uppercase under hub.pop_create.idem_cloud
    for template in templates.iterdir():
        if template.is_dir():
            continue
        attr = (
            template.stem.upper().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        contents = template.read_text()
        setattr(hub.pop_create.idem_cloud, attr, contents)


def new(hub, name: str, directory: pathlib.Path, **kwargs):
    clean_name = kwargs.get("clean_name", name)
    dynes = set(kwargs.get("dynes", ()))
    idem_dynes = {"acct", "exec", "states", "tool"}
    dynes.update(idem_dynes)
    if hub.OPT.pop_create.simple_cloud_name:
        cloud_name = hub.OPT.pop_create.simple_cloud_name
    else:
        cloud_name = clean_name.replace("idem", "").replace("cloud", "").strip("_")

    # Run a traditional pop seed on the directory with common idem states
    hub.pop_create.init.run(
        ["seed", "tests", "cicd"], name, directory, vertical=True, dynes=dynes
    )

    # Overwrite some of the files made by "seed"
    hub.pop_create.init.write(
        directory / "requirements" / "base.txt", contents=hub.pop_create.idem_cloud.BASE
    )
    eqchars = "=" * len(name)
    header = f"{eqchars}\n{name.upper()}\n{eqchars}\n"
    hub.pop_create.init.write(
        directory / "README.rst",
        contents=hub.pop_create.idem_cloud.README,
        replace={
            "R__HEADER__": header,
            "R__NAME__": name,
            "R__CLEAN_NAME__": clean_name,
            "R__CLOUD__": cloud_name,
        },
    )

    # Overwrite some of the files made by "test"
    test_dir = directory / "tests"
    hub.pop_create.init.write(
        test_dir / "unit" / "conftest.py",
        contents=hub.pop_create.idem_cloud.UNIT_CONFTEST,
    )
    hub.pop_create.init.write(
        test_dir / "integration" / "conftest.py",
        contents=hub.pop_create.idem_cloud.INTEGRATION_CONFTEST,
        replace={"R__CLOUD__": cloud_name},
    )

    # Overwrite some of the files made by "cicd"
    hub.pop_create.init.write(
        directory / "build.conf",
        contents=hub.pop_create.idem_cloud.BUILD,
    )

    # Set up new files for idem_cloud
    SRC = directory / clean_name
    # Set up acct
    hub.pop_create.init.write(
        SRC / "acct" / cloud_name / "basic_auth.py",
        contents=hub.pop_create.idem_cloud.ACCT_GATHER,
        replace={"R__CLOUD__": cloud_name},
    )
    hub.pop_create.init.write(
        SRC / "exec" / cloud_name / "init.py",
        contents=hub.pop_create.idem_cloud.EXEC_INIT,
        replace={"R__CLOUD__": cloud_name},
    )
    hub.pop_create.init.write(
        SRC / "states" / cloud_name / "init.py",
        contents=hub.pop_create.idem_cloud.STATE_INIT,
        replace={"R__CLOUD__": cloud_name},
    )
