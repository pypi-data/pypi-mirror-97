from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.WordNet cimport WordNet


cdef class SentenceAutoSemantic:

    cpdef bint autoLabelSingleSemantics(self, AnnotatedSentence sentence)
    cpdef autoSemantic(self, AnnotatedSentence sentence)
    cpdef list getCandidateSynSets(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, AnnotatedSentence sentence,
                                   int index)
