import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-integrations",  # Replace with your own username
    version="0.0.24",
    author="DOT",
    author_email="dot@adara.com",
    description="Simplified advertising integrations",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/framework-auth",
    setup_requires=['pytest-runner'],
    packages=['stratus_api.integrations'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "stratus-api-core>=0.0.14",
        "stratus-api-auth>=0.0.2",
        "stratus-api-tasks>=0.0.2",
        "stratus-api-storage>=0.0.1",
        "google-cloud-bigquery>=1.27.0",
        "stratus-api-bigquery>=0.0.8"
    ]
)
