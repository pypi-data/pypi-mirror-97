from setuptools import setup, find_packages

from take_ai_evaluation import __name__ as name
from take_ai_evaluation import __author__ as author
from take_ai_evaluation import __doc__ as doc
from take_ai_evaluation import __email__ as author_email
from take_ai_evaluation import __version__ as version
from take_ai_evaluation import __license__ as license
from take_ai_evaluation import __credits__ as credits

maintainer = "daresearch"
maintainer_email = "anaytics.dar@take.net"
keywords = ['ai-knowledge', 'chatbot', 'classification', 'evaluation']
description = doc.splitlines()[0].strip()
long_description = open('README.md').read()
long_description_content_type = 'text/markdown'
install_requires = [
    element
    for element in [
        line.split('#', 1)[0].strip()
        for line in open('requirements.txt', 'r', encoding='utf-8')
    ]
    if element and not element.startswith('--')
]
classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
]

setup(
    name=name,
    author=author,
    author_email=author_email,
    version=version,
    license=license,
    credits=credits,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    keywords=keywords,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    install_requires=install_requires,
    classifiers=classifiers,
    packages=find_packages(exclude=['tests'])
)
