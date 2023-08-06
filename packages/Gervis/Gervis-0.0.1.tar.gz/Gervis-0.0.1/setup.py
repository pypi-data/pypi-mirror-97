from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Gervis',
  version='0.0.1',
  description="This is a python based voice virtual assistant that performs multiple tasks based on voice commands.",
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='SATISH KUMAR TIGGA',
  author_email='satish.tigga05@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='virtual assistant', 
  packages=find_packages(),
  install_requires=["JarvisAI","speech_recognition","pyttsx3","pywhatkit","datetime","wikipedia","pyjokes","re","pprint","random"] 
)