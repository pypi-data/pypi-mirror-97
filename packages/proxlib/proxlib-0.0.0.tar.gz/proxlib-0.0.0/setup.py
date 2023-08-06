import sys
import subprocess
from pkg_resources import working_set
from pathlib import Path
from setuptools import setup, find_packages


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    src_dir = base_dir/"src"/"proxlib"

    sys.path.insert(0, src_dir.as_posix())
    import __about__ as about

    with (base_dir/"README.rst").open() as f:
        long_description = f.read()

    install_requirements = [
        "numpy",
        "scipy",
        "cython",
    ]

    installed_pkgs = [p.key for p in working_set]
    for pkg in install_requirements:
        if pkg not in installed_pkgs:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    import numpy
    from Cython.Build import cythonize

    test_requirements = [
        "pytest",
    ]

    doc_requirements = []

    setup(name=about.__title__,
          version=about.__version__,

          description=about.__summary__,
          long_description=long_description,
          license=about.__license__,
          url=about.__uri__,

          author=about.__author__,
          author_email=about.__email__,

          package_dir={"": "src"},
          packages=find_packages(where="src"),
          include_package_data=True,

          install_requires=install_requirements,
          tests_require=test_requirements,
          extras_require={
              "docs": doc_requirements,
              "test": test_requirements,
              "dev": doc_requirements + test_requirements
          },
          ext_modules=cythonize('src/proxlib/operators.pyx'),
          include_dirs=[numpy.get_include()],
          zip_safe=False,)
