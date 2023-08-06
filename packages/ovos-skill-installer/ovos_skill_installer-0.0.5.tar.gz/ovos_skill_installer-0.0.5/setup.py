from setuptools import setup

setup(
    name='ovos_skill_installer',
    version='0.0.5',
    description='Mycroft skill installer from .zip or .tar.gz urls',
    url='https://github.com/OpenVoiceOS/ovos_skill_installer',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Topic :: System :: Filesystems',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=["requests"],
    keywords='tar extraction web download dependencies',
    packages=['ovos_skill_installer']

)
