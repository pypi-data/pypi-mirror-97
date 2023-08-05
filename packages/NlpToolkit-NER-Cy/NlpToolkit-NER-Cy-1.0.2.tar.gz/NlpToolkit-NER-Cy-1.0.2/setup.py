from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["NER/AutoProcessor/ParseTree/*.pyx",
                           "NER/AutoProcessor/Sentence/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-NER-Cy',
    version='1.0.2',
    packages=['NER', 'NER.AutoProcessor', 'NER.AutoProcessor.Sentence', 'NER.AutoProcessor.ParseTree'],
    package_data={'NER.AutoProcessor.ParseTree': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'NER.AutoProcessor.Sentence': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/NER-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='NER library',
    install_requires = ['NlpToolkit-AnnotatedSentence-Cy', 'NlpToolkit-AnnotatedTree-Cy']
)
