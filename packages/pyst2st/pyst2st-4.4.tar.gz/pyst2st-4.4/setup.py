from distutils.core import setup
setup(
    name='pyst2st',         # How you named your package folder (MyLib)
    packages=['pyst2st'],   # Chose the same as "name"
    version='4.4',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Dynamic Student Story Generator',
    author='Doulat',                   # Type in your name
    author_email='ahmad.doulat@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/ahmaddoulat/pystorygen',
    # I explain this later on
    download_url='https://github.com/ahmaddoulat/pystorygen/archive/v_0.1.tar.gz',
    # Keywords that define your package best
    keywords=['student', 'nlg', 'story'],
    install_requires=[            # I get to this in a second
        'inflect',
        'pandas',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
