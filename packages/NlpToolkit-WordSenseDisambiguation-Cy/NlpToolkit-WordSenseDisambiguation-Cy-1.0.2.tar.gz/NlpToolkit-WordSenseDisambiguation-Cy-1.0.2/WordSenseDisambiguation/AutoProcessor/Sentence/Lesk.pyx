from random import randrange
import random

from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.Sentence.SentenceAutoSemantic cimport SentenceAutoSemantic

cdef class Lesk(SentenceAutoSemantic):

    cpdef WordNet __turkishWordNet
    cpdef FsmMorphologicalAnalyzer __fsm

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    cpdef int intersection(self, SynSet synSet, AnnotatedSentence sentence):
        cdef list words1, words2
        cdef int count
        cdef str word1, word2
        if synSet.getExample() is not None:
            words1 = (synSet.getLongDefinition() + " " + synSet.getExample()).split(" ")
        else:
            words1 = synSet.getLongDefinition().split(" ")
        words2 = sentence.toString().split(" ")
        count = 0
        for word1 in words1:
            for word2 in words2:
                if word1.lower() == word2.lower():
                    count = count + 1
        return count

    cpdef bint autoLabelSingleSemantics(self, sentence: AnnotatedSentence):
        cdef bint done
        cdef int i, j, maxIntersection, intersectionCount
        cdef list synSets, maxSynSets
        cdef SynSet synSet
        random.seed(1)
        done = False
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            maxIntersection = -1
            for j in range(len(synSets)):
                synSet = synSets[j]
                intersectionCount = self.intersection(synSet, sentence)
                if intersectionCount > maxIntersection:
                    maxIntersection = intersectionCount
            maxSynSets = []
            for j in range(len(synSets)):
                synSet = synSets[j]
                if self.intersection(synSet, sentence) == maxIntersection:
                    maxSynSets.append(synSet)
            if len(maxSynSets) > 0:
                done = True
                sentence.getWord(i).setSemantic(maxSynSets[randrange(len(maxSynSets))].getId())
        return done
