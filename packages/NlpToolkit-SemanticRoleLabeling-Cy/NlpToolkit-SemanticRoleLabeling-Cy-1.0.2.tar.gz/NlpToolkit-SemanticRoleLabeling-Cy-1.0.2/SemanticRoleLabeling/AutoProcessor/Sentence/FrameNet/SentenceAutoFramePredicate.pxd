from FrameNet.FrameNet cimport FrameNet
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence


cdef class SentenceAutoFramePredicate:

    cdef FrameNet frameNet

    cpdef bint autoPredicate(self, AnnotatedSentence sentence)
