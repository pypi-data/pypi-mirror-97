def get_local_package_version(package_name):
    import pip_api

    installed_distributions = pip_api.installed_distributions()
    if package_name not in installed_distributions:
        return None
    return str(installed_distributions[package_name].version)


def latest_package_version(package_name):
    pass
