import random

from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.Sentence.SentenceAutoSemantic cimport SentenceAutoSemantic

cdef class RandomSentenceAutoSemantic(SentenceAutoSemantic):

    cpdef WordNet __turkishWordNet
    cpdef FsmMorphologicalAnalyzer __fsm

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    cpdef bint autoLabelSingleSemantics(self, AnnotatedSentence sentence):
        cdef int i
        cdef list synSets
        random.seed(1)
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            if len(synSets) > 0:
                sentence.getWord(i).setSemantic(synSets[random.randrange(len(synSets))].getId())
        return True
