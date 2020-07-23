from setuptools import setup, find_packages

with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='pynet-ssh',
    version='1.0.0',
    description='Fast and simple SSH library for interactive session based on paramiko',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Gustavo Santiago',
    author_email='jcdaniel14@gmail.com',
    keywords=['SSH', 'SSH Client', 'Paramiko', "Devnet"],
    url='https://github.com/jcdaniel14/pynet-ssh.git',
    download_url='https://pypi.org/project/pynet-ssh/'
)

install_requires = [
    "paramiko>=2.4.3"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)