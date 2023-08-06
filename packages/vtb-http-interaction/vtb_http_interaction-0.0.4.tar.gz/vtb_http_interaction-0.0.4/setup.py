import setuptools
"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
"""
setuptools.setup(
    name="vtb_http_interaction",
    version="0.0.4",
    author="VTB python team",
    author_email="python.team@vtb.ru",
    description="Межсервисное взаимодействие на основе протокола HTTP",
    long_description="Утилитарный пакет, содержащий в себе интеграционный модуль с Keycloak и инструменты для организации межсервисного взаимодействия на основе протокола HTTP. Детали смотри в README.md",
    keywords='python, microservices, utils, http',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp==3.7.3",
        "python-keycloak==0.24.0",
        "aioredis==1.3.1"
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-aiohttp',
            'pytest-mock',
            'pylint',
            'pytest-dotenv',
            'envparse'
        ]
    },
    python_requires='>=3.8',
)
