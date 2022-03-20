from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="DataShip",
        version="0.0.1",
        url="https://github.com/AgustinZavalaA/DataShip",
        author="Agustin Zavala",
        author_email="1930120@upv.edu.mx",
        description="DataShip is an easy to use data analysis app.",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )
