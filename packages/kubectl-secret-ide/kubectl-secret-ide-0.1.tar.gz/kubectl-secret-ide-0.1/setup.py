from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='kubectl-secret-ide',
      version='0.1',
      description='A tool to edit secrets inside k8s',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.9',
      ],
      keywords='kubectl kubectl-plugin k8s secrets',
      author='Ben Antony',
      author_email='antony@synyx.de',
      license='MIT',
      packages=['kubectl_secret_ide'],
      entry_points={
          'console_scripts': ['kubectl-secret-ide=kubectl_secret_ide:main'],
      },
      zip_safe=False)
