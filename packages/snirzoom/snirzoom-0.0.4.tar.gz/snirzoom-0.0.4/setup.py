from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    include_package_data=True,
    name='snirzoom',
    version='0.0.4',
    description='automate zoom meeting',
    long_description="""enter the link and the time, the link will be opened according to the referenced time""",
    url='',
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='zoom',
    packages=find_packages(),
    install_requires=['ttkthemes', 'pyperclip']
)