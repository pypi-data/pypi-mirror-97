from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["WordSenseDisambiguation/AutoProcessor/ParseTree/*.pyx",
                           "WordSenseDisambiguation/AutoProcessor/Sentence/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-WordSenseDisambiguation-Cy',
    version='1.0.2',
    packages=['WordSenseDisambiguation', 'WordSenseDisambiguation.AutoProcessor',
              'WordSenseDisambiguation.AutoProcessor.Sentence', 'WordSenseDisambiguation.AutoProcessor.ParseTree'],
    package_data={'WordSenseDisambiguation.AutoProcessor.ParseTree': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'WordSenseDisambiguation.AutoProcessor.Sentence': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/WordSenseDisambiguation-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Word Sense Disambiguation Library',
    install_requires = ['NlpToolkit-AnnotatedSentence-Cy', 'NlpToolkit-AnnotatedTree-Cy']
)
