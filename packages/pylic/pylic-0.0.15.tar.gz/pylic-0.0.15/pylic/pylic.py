import sys
from typing import List, Tuple

import toml

if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
    from importlib.metadata import Distribution, distributions
else:
    from importlib_metadata import Distribution, distributions  # type: ignore


def read_pyproject_file() -> Tuple[List[str], List[str]]:
    with open("pyproject.toml", "r") as pyproject_file:
        try:
            project_config = toml.load(pyproject_file)
        except Exception as exception:
            print("Could not load pyproject.toml file.")
            raise exception

    tool_config = project_config.get("tool", None)
    if tool_config is None:
        raise Exception("No 'tool' section found in the pyproject.toml file. Excpecting a [tool.pylic] section.")

    pylic_config = tool_config.get("pylic", None)
    if pylic_config is None:
        raise Exception("No 'tool.pylic' section found in the pyproject.toml file. Excpecting a [tool.pylic] section.")

    allowed_licenses: List[str] = [license.lower() for license in pylic_config.get("allowed_licenses", [])]

    if "unknown" in allowed_licenses:
        raise Exception("'unknown' can't be an allowed license. Whitelist the corresponding packages instead.")

    whitelisted_packages: List[str] = pylic_config.get("whitelisted_packages", [])

    return (allowed_licenses, whitelisted_packages)


def read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]

    return "unknown"


def read_licenses_from_metadata(distribution: Distribution) -> str:
    return distribution.metadata.get("License", "unknown")


def read_installed_license_metadata() -> List[dict]:
    installed_distributions = distributions()

    installed_licenses: List[dict] = []
    for distribution in installed_distributions:
        package_name = distribution.metadata["Name"]

        license_string = read_license_from_classifier(distribution)
        if license_string == "unknown":
            license_string = read_licenses_from_metadata(distribution)

        new_license = {"license": license_string, "package": package_name}
        installed_licenses.append(new_license)

    return installed_licenses


def check_whitelisted_packages(whitelisted_packages: List[str], licenses: List[dict]):
    bad_whitelisted_packages: List[dict] = []
    for license_info in licenses:
        license = license_info["license"]
        package = license_info["package"]

        if package in whitelisted_packages and license.lower() != "unknown":
            bad_whitelisted_packages.append({"license": license, "package": package})

    if len(bad_whitelisted_packages) > 0:
        print("Found whitelisted packages with a known license. Instead allow these licenses explicitly:")
        for bad_package in bad_whitelisted_packages:
            print(f"\t{bad_package['package']}: {bad_package['license']}")
        sys.exit(1)


def check_licenses(allowed_licenses: List[str], whitelisted_packages: List[str], licenses: List[dict]) -> None:
    bad_licenses: List[dict] = []
    for license_info in licenses:
        license = license_info["license"]
        package = license_info["package"]

        if (license.lower() == "unknown" and package in whitelisted_packages) or license.lower() in allowed_licenses:
            continue

        bad_licenses.append({"license": license, "package": package})

    if len(bad_licenses) > 0:
        print("Found unallowed licenses:")
        for bad_license in bad_licenses:
            print(f"\t{bad_license['package']}: {bad_license['license']}")
        sys.exit(1)

    print("All licenses ok")


def main():
    allowed_licenses, whitelisted_packages = read_pyproject_file()
    installed_licenses = read_installed_license_metadata()
    check_whitelisted_packages(whitelisted_packages, installed_licenses)
    check_licenses(allowed_licenses, whitelisted_packages, installed_licenses)


if __name__ == "__main__":
    main()
