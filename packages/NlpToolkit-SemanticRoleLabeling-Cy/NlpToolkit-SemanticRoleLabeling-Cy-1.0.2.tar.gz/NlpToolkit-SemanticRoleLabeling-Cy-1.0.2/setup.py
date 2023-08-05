from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["SemanticRoleLabeling/AutoProcessor/ParseTree/Propbank/*.pyx",
                           "SemanticRoleLabeling/AutoProcessor/Sentence/Propbank/*.pyx",
                           "SemanticRoleLabeling/AutoProcessor/Sentence/FrameNet/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-SemanticRoleLabeling-Cy',
    version='1.0.2',
    packages=['SemanticRoleLabeling', 'SemanticRoleLabeling.AutoProcessor',
              'SemanticRoleLabeling.AutoProcessor.Sentence', 'SemanticRoleLabeling.AutoProcessor.Sentence.FrameNet',
              'SemanticRoleLabeling.AutoProcessor.Sentence.Propbank', 'SemanticRoleLabeling.AutoProcessor.ParseTree',
              'SemanticRoleLabeling.AutoProcessor.ParseTree.Propbank'],
    package_data={'SemanticRoleLabeling.AutoProcessor.ParseTree.Propbank': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'SemanticRoleLabeling.AutoProcessor.Sentence.FrameNet': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'SemanticRoleLabeling.AutoProcessor.Sentence.Propbank': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/SemanticRoleLabeling-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Semantic Role Labeling Library',
    install_requires = ['NlpToolkit-AnnotatedSentence-Cy', 'NlpToolkit-AnnotatedTree-Cy']
)
