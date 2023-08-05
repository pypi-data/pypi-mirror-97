from AnnotatedSentence.ViewLayerType import ViewLayerType
from Dictionary.Word cimport Word
from PropBank.ArgumentType import ArgumentType
from PropBank.Frameset cimport Frameset
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTransferable cimport IsTransferable
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector


cdef class AutoArgument:

    cdef object secondLanguage

    cpdef bint autoDetectArgument(self, ParseNodeDrawable parseNode, object argumentType):
        pass

    def __init__(self, secondLanguage: ViewLayerType):
        self.secondLanguage = secondLanguage

    cpdef autoArgument(self, ParseTreeDrawable parseTree, Frameset frameset):
        cdef list leafList
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef ParseNodeDrawable parseNode
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTransferable(self.secondLanguage))
        leafList = nodeDrawableCollector.collect()
        for parseNode in leafList:
            if isinstance(parseNode, ParseNodeDrawable) and parseNode.getLayerData(ViewLayerType.PROPBANK) is None:
                for argumentType in ArgumentType:
                    if frameset.containsArgument(argumentType) and self.autoDetectArgument(parseNode, argumentType):
                        parseNode.getLayerInfo().setLayerData(ViewLayerType.PROPBANK,
                                                              ArgumentType.getPropbankType(argumentType))
                if Word.isPunctuationSymbol(parseNode.getLayerData(self.secondLanguage)):
                    parseNode.getLayerInfo().setLayerData(ViewLayerType.PROPBANK, "NONE")
        parseTree.saveWithFileName()
