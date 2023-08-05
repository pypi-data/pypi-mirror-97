from PropBank.FramesetList cimport FramesetList
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from SemanticRoleLabeling.AutoProcessor.Sentence.Propbank.SentenceAutoPredicate cimport SentenceAutoPredicate


cdef class TurkishSentenceAutoPredicate(SentenceAutoPredicate):

    cdef FramesetList __framesetList

    def __init__(self, framesetList: FramesetList):
        """
        Constructor for TurkishSentenceAutoPredicate. Gets the FrameSets as input from the user, and sets
        the corresponding attribute.

        PARAMETERS
        ----------
        framesetList : FramesetList
            FramesetList containing the Turkish propbank frames.
        """
        self.__framesetList = framesetList

    cpdef bint autoPredicate(self, AnnotatedSentence sentence):
        """
        The method uses predicateCandidates method to predict possible predicates. For each candidate, it sets for that
        word PREDICATE tag.

        PARAMETERS
        ----------
        sentence : AnnotatedSentence
            The sentence for which predicates will be determined automatically.

        RETURNS
        -------
        bool
            If at least one word has been tagged, true; false otherwise.
        """
        cdef list candidateList
        cdef AnnotatedWord word
        candidateList = sentence.predicateCandidates(self.__framesetList)
        for word in candidateList:
            if isinstance(word, AnnotatedWord):
                word.setArgument("PREDICATE$" + word.getSemantic())
        if len(candidateList) > 0:
            return True
        return False
