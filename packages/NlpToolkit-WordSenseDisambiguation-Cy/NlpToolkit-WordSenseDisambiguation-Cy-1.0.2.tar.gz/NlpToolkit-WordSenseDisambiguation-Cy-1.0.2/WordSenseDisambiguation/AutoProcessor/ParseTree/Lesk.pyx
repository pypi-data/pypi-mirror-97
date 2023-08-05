from random import randrange
import random

from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode cimport IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.ParseTree.TreeAutoSemantic cimport TreeAutoSemantic

cdef class Lesk(TreeAutoSemantic):

    cpdef WordNet __turkishWordNet
    cpdef FsmMorphologicalAnalyzer __fsm

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    cpdef int intersection(self, SynSet synSet, list leafList):
        cdef list words1
        cdef list words2
        cdef int i, count
        cdef str word1, word2
        if synSet.getExample() is not None:
            words1 = (synSet.getLongDefinition() + " " + synSet.getExample()).split(" ")
        else:
            words1 = synSet.getLongDefinition().split(" ")
        words2 = []
        for i in range(len(leafList)):
            words2.append(leafList[i].getLayerData(ViewLayerType.TURKISH_WORD))
        count = 0
        for word1 in words1:
            for word2 in words2:
                if word1.lower() == word2.lower():
                    count = count + 1
        return count

    cpdef bint autoLabelSingleSemantics(self, ParseTreeDrawable parseTree):
        cdef int i, maxIntersection, j, intersectionCount
        cdef list leafList
        cdef bint done
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef list synSets, maxSynSets
        cdef SynSet synSet
        random.seed(1)
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        done = False
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            maxIntersection = -1
            for j in range(len(synSets)):
                synSet = synSets[j]
                intersectionCount = self.intersection(synSet, leafList)
                if intersectionCount > maxIntersection:
                    maxIntersection = intersectionCount
            maxSynSets = []
            for j in range(len(synSets)):
                synSet = synSets[j]
                if self.intersection(synSet,leafList) == maxIntersection:
                    maxSynSets.append(synSet)
            if len(maxSynSets) > 0:
                leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, maxSynSets[randrange(len(maxSynSets))].getId())
                done = True
        return done
