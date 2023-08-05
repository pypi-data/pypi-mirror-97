from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence


cdef class SentenceAutoPredicate:

    cpdef bint autoPredicate(self, AnnotatedSentence sentence)
