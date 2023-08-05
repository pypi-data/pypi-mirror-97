from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence


cdef class SentenceAutoArgument:

    cpdef bint autoArgument(self, AnnotatedSentence sentence)
