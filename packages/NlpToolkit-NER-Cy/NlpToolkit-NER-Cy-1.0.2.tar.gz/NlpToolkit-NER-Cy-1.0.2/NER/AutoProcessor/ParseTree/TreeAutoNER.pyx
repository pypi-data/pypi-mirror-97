from AnnotatedSentence.ViewLayerType import ViewLayerType
from NamedEntityRecognition.AutoNER cimport AutoNER
from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTransferable cimport IsTransferable
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector


cdef class TreeAutoNER(AutoNER):

    cdef object secondLanguage

    cpdef autoDetectPerson(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoDetectLocation(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoDetectOrganization(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoDetectMoney(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoDetectTime(self, ParseTreeDrawable parseTree):
        pass

    def __init__(self, secondLanguage: ViewLayerType):
        self.secondLanguage = secondLanguage

    cpdef autoNER(self, ParseTreeDrawable parseTree):
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef list leafList
        cdef ParseNodeDrawable parseNode
        self.autoDetectPerson(parseTree)
        self.autoDetectLocation(parseTree)
        self.autoDetectOrganization(parseTree)
        self.autoDetectMoney(parseTree)
        self.autoDetectTime(parseTree)
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTransferable(self.secondLanguage))
        leafList = nodeDrawableCollector.collect()
        for parseNode in leafList:
            if isinstance(parseNode, ParseNodeDrawable) and not parseNode.layerExists(ViewLayerType.NER):
                parseNode.getLayerInfo().setLayerData(ViewLayerType.NER, "NONE")
        parseTree.saveWithFileName()
