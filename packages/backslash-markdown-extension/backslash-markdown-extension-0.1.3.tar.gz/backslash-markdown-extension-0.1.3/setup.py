import setuptools

with open('README.md', 'r') as fh:
	readme = fh.read()

setuptools.setup(
	name='backslash-markdown-extension',
	version='0.1.3',
	author='Georges Duverger',
	author_email='georges.duverger@gmail.com',
	description='Backslash Markdown Extension',
	long_description=readme,
	long_description_content_type='text/markdown',
	url='https://github.com/gduverger/backslash-markdown-extension',
	license='MIT',
	packages=['backslash_markdown_extension'],
	install_requires=['markdown'],
	python_requires='>=3',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'Natural Language :: English'
	],
)
