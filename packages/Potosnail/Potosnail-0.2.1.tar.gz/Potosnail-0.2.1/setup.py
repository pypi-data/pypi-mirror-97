from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ]

long_description = 'Potosnail helps improve the Machine Learning workflow with its data preprocessing, model building, and model evaluating helper classes.'

setup(
      name='Potosnail',
      version='0.2.1',
      description='improves ML workflow',
      long_description=long_description,
      url='https://github.com/spe301/Potosnail',
      author='Spencer Holley',
      author_email ='aacjpw@gmail.com',
      liscence='MIT',
      classifiers=classifiers,
      keywords='',
      packages=find_packages(),
      py_modules=['potosnail'],
      install_requires=['pandas>=1.1.3', 'numpy>=1.18.0', 'scikit-learn==0.22.2.post1',
                        'xgboost<=1.3.1', 'matplotlib>=3.3.2',
                        'tensorflow>=2.4.0', 'seaborn>=0.11.0', 'statsmodels>=0.12.0', 
                        'beautifulsoup4==4.9.3', 'urllib3==1.25.11', 'regex==2020.10.15',
                        'lxml==4.6.1'])