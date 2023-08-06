from setuptools import setup 
  
# reading long description from file 
with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here 
REQUIREMENTS = ['requests'] 
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Internet', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 2', 
    'Programming Language :: Python :: 2.6', 
    'Programming Language :: Python :: 2.7', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    ] 
  
# calling the setup function  
setup(name='uncertaint_sdp_python', 
      version='2.0.0', 
      description='Probabilistic programming language', 
      long_description=long_description, 
      url='https://github.com/dadi-vardhan/SDP/tree/master/SDP_Assignments/Uncertain_T/Uncertain_python', 
      author='Vishnu Vardhan Dadi, Krishna Nallanukala, Manoj Kumar Murugan', 
      author_email='vishnu.dadi@smail.inf.h-brs.de, krishna.nallanukala@smail.inf.h-brs.de, manoj.murugan@smail.inf.hochschule-bonn-rhein-sieg.de', 
      license='MIT', 
      packages=['uncertaint_sdp_python'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='Probabilistic programming language'
      ) 