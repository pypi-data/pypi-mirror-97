import pathlib

# python 3.9 is required.
try:
    # Use setup() from setuptools(/distribute) if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

from Particle_Board_REPL import __version__

setup(
    name="Particle_Board_REPL",
    version=__version__,
    # Your name & email here
    long_description=README,
    long_description_content_type="text/markdown",
    description="An application with REPL for programming and testing Particle.io boards.",
    url="https://github.com/EricGebhart/Particle_Board_REPL",
    author="Eric Gebhart",
    author_email="e.a.gebhart@gmail.com",
    packages=["Particle_Board_REPL"],
    package_data={"": ["*.yaml"]},
    include_package_data=True,
    scripts=[],
    license="MIT",
    entry_points={"console_scripts": ["PBR=Particle_Board_REPL.__main__:main"]},
    install_requires=["Simple_Process_REPL"],
)
