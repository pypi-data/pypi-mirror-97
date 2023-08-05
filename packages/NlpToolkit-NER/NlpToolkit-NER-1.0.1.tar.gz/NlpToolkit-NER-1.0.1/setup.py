from setuptools import setup

setup(
    name='NlpToolkit-NER',
    version='1.0.1',
    packages=['NER', 'NER.AutoProcessor', 'NER.AutoProcessor.Sentence', 'NER.AutoProcessor.ParseTree'],
    url='https://github.com/StarlangSoftware/NER-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='NER library',
    install_requires=['NlpToolkit-AnnotatedSentence', 'NlpToolkit-AnnotatedTree']
)
