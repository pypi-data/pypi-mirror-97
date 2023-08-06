from setuptools import find_packages, setup

######

CLASSIFIERS = [
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
]
DESCRIPTION = ""
KEYWORDS = ["python"]
URL = ""
AUTHOR = "Salah Ahmed"
AUTHOR_EMAIL = "salahs.email@pm.me"

REQUIREMENTS = ["attrs", "geopy", "requests", "automock"]
CRON_REQUIREMENTS = ["python-crontab", "pydub"]
TEST_REQUIREMENTS = [
    "pytest-cov",
    "pytest-freezegun",
    "coverage[toml]",
    "responses",
]
DEV_REQUIREMENTS = [
    "ipython",
    "jedi==0.17.2",
    "pdbpp",
    "black==19.10b0",
    "isort==5.6.4",
    "flake8",
    "pre-commit",
    "tox",
]

#####

with open("README.rst", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="adhan_pi",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    python_requires=">=3.7",
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=KEYWORDS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"adhan_pi": ["py.typed", "stubs/**/*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "schedule_prayer_cron=adhan_pi.cli:schedule_prayer_cron_runner",
            "alert_adhan=adhan_pi.cli:alert_adhan",
        ],
    },
    extras_require={
        "test": TEST_REQUIREMENTS + CRON_REQUIREMENTS,
        "dev": TEST_REQUIREMENTS + DEV_REQUIREMENTS + CRON_REQUIREMENTS,
        "cron": CRON_REQUIREMENTS,
    },
)
