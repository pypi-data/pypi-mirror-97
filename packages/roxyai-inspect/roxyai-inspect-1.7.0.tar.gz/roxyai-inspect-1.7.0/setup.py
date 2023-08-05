# (c) Roxy Corp. 2021-
# Roxy AI Release
import setuptools
from pathlib import Path

PACKAGE_NAME = 'roxyai-inspect'


def _get_version_from_file():
    """ バージョンファイルの読み込み
    """
    VERSION = f'{PACKAGE_NAME.replace("-", "_")}/version'
    ver = Path(VERSION).read_text().strip()
    return ver


def _get_description_from_file():
    DESCRIPTION = './README.md'
    return Path(DESCRIPTION).read_text()


setuptools.setup(
    name=PACKAGE_NAME,
    version=_get_version_from_file(),
    author="Roxy Corp.",
    author_email="support@roxy-ai.jp",
    description="Roxy AI Inspect-Server package",
    long_description=Path('README.md').read_text(encoding='utf_8'),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/roxy-ai/roxy-ai",
    packages=setuptools.find_packages('.'),
    include_package_data=True,
    package_data={
        '': [
            '_pytransform.dll',
            'pytransform.key',
            'config/default_log.conf',
            'config/system_config.json',
            'config/sample/analyze_server_log.conf',
            'config/sample/inspect_server_log.conf',
            'config/sample/system_config.json',
            'roxy_lic_checker.exe',
            'version',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license='Proprietary',
    entry_points=f'''
        [console_scripts]
        {PACKAGE_NAME} = {PACKAGE_NAME.replace('-', '_')}.launch: main
    ''',
    install_requires=[
        'numpy==1.19.3',
        'tensorflow-gpu==2.1.0',
        'tensorflow-addons==0.8.3',
        'imageio==2.8.0',
        'pandas==1.0.3',
        'scipy==1.4.1',
        'scikit_learn==0.22.2.post1',
        'matplotlib==3.2.1',
        'xgboost==1.0.2',
        'optuna==1.2.0',
        'opencv-python==4.2.0.34',
        'pyarmor==6.1.0',
        'objgraph==3.4.1',
        'psutil==5.7.0',
        'json5==0.9.5',
        'h5py==2.10.0',
        'send2trash==1.5.0',
        'pyperclip==1.8.0',
        'colorama==0.4.4',
        'termcolor==1.1.0',
        'roxyai-api>=1.7.0',
    ]
)
