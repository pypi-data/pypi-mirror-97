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
    name='snirwhatsapp',
    version='0.0.6',
    description='automate whatsapp messages',
    long_description="""this script sends automatic messages with input from the user (contact and message). this script include friendly interface using tkinter""",
    url='',
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='whatsapp',
    packages=find_packages(),
    install_requires=['selenium', 'ttkthemes']
)