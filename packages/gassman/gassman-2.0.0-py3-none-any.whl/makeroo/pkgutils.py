import pkg_resources


def package_version(name: str) -> str:
    for egg_info in pkg_resources.working_set:
        if egg_info.project_name != name:
            continue

        return egg_info.version

    raise KeyError
