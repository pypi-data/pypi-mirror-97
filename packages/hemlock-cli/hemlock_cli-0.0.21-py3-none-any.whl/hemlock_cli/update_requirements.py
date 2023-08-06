"""Update requirements files"""

from pkg_resources import get_distribution
import sys

def parse_package(package):
    comparisons = [
        '>=',
        '==',
        '<=',
        '>',
        '<'
    ]
    for comparison in comparisons:
        if comparison in package:
            name, version = package.split(comparison)
            return [name, comparison, version]
    version = get_distribution(package).version
    return [package, '==', version]

def update_file(path, new_package):
    """Update a single requirements file with package"""
    def update_packages():
        new_line = ''.join(new_package)
        for i, package in enumerate(packages):
            package = parse_package(package)
            if package[0] == new_package[0]:
                # replace old version of the package
                packages[i] = new_line
                return
            if package[0] > new_package[0]:
                # insert new package
                packages.insert(i, new_line)
                return
        packages.append(new_line)

    with open(path, 'r') as requirements_f:
        packages = requirements_f.readlines()
    packages = [p.strip() for p in packages]
    packages.sort()
    update_packages()
    with open(path, 'w') as requirements_f:
        requirements_f.write('\n'.join(packages))

if __name__ == '__main__':
    new_packages = sys.argv[1:]
    for new_package in new_packages:
        new_package = parse_package(new_package)
        update_file('requirements.txt', new_package)
        update_file('local-requirements.txt', new_package)