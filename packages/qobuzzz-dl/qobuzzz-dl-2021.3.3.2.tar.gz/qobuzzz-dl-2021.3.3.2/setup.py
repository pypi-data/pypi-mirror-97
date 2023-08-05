from setuptools import setup, find_packages
from qobuzzz_dl.printf import VERSION
setup(
    name = 'qobuzzz-dl',
    version = VERSION,
    license = "Apache2",
    description = "Qobuz Music Downloader.",

    author = 'YaronH',
    author_email = "yaronhuang@foxmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2021.3.1.0", "requests>=2.22.0", "pycryptodome", "pydub", "prettytable"],
    entry_points={'console_scripts': ['qobuzzz-dl = qobuzzz_dl:main', ]}
)
