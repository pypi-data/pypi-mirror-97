from setuptools import setup

setup(
    name="eternalswarm.mind",
    version='0.2.8',
    packages=['eternalswarm.mind'],
    namespace_packages=['eternalswarm'],
    install_requires=['grpcio'],
    extras_require={
        'dev': [
            'grpcio-tools',
            'mypy',
            'mypy-protobuf',
            'grpc-stubs',
        ]
    },
    author='Matthijs Gielen',
    author_email='eternalswarm@mwgielen.com',
    url='https://gitlab.com/eternal-swarm/mind',
    description='The protobuf files to talk to the eternalswarm drone.',
    package_data={"eternalswarm.mind": ["py.typed", "*.pyi"]},
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Information Technology',
        'Typing :: Typed',
    ]
)
