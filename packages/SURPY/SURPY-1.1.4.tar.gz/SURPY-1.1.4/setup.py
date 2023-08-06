from setuptools import setup

with open ("README.md") as f:
	long_description = f.read()
setup(name='SURPY',
version='1.1.4',
description='SURPY python for surgical data analysis',
url='https://github.com/sasurasa/Surgical-Outcome-Analysis-on-Python/tree/SURG-package',
author='Surasak Sangkhathat',
author_email='s.sangkhathat@gmail.com',
license='Prince of Songkla University',
packages=['SURPY'],
zip_safe=False,
long_description=long_description,
    long_description_content_type='text/markdown'
)