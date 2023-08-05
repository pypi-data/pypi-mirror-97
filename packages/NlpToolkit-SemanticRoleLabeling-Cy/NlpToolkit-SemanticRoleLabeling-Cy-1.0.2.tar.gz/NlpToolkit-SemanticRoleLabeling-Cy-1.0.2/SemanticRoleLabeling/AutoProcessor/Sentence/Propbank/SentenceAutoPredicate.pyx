cdef class SentenceAutoPredicate:

    cpdef bint autoPredicate(self, AnnotatedSentence sentence):
        """
        The method should set determine all predicates in the sentence.

        PARAMETERS
        ----------
        sentence : AnnotatedSentence
            The sentence for which predicates will be determined automatically.
        """
        pass
