import os
import setuptools

setuptools.setup(
     name='udpipe_parser_temp',  
     version='0.9.4',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="UDPipe-based Parser brings Universal Dependencies trees in more practical form.",
     include_package_data=True,
     keywords=['parser', 'Universal Dependencies', 'NLP', 'russian','syntax'],
     url="https://github.com/constantin50/udpipe_parser",
     packages=setuptools.find_packages(),
     install_requires=["pymorphy2","conllu","separatrice_temp","nltk"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
