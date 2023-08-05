from random import randrange
import random

from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode cimport IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.ParseTree.TreeAutoSemantic cimport TreeAutoSemantic

cdef class RandomTreeAutoSemantic(TreeAutoSemantic):

    cpdef WordNet __turkishWordNet
    cpdef FsmMorphologicalAnalyzer __fsm

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    cpdef bint autoLabelSingleSemantics(self, ParseTreeDrawable parseTree):
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef int i
        cdef list synSets
        random.seed(1)
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            if len(synSets) > 0:
                leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, synSets[randrange(len(synSets))].getId())
        return True
