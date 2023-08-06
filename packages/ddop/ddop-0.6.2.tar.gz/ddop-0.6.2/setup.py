from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

setup(
    name='ddop',
    version='v0.6.2',
    url='https://andreasphilippi.github.io/ddop/',
    license='MIT',
    author='Andreas Philippi',
    author_email='',
    description='Package for data-driven operations management',
    #long_description=README,
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['numpy==1.18.2', 'scikit-learn==0.23.0', 'pandas', 'PuLP==2.0',
                      'tensorflow==2.1.0', 'Keras==2.3.1', 'statsmodels==0.11.1',
                      'scipy==1.4.1'],
)
