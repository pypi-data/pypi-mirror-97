from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.WordNet cimport WordNet


cdef class TreeAutoSemantic:

    cpdef bint autoLabelSingleSemantics(self, ParseTreeDrawable parseTree)
    cpdef list getCandidateSynSets(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, list leafList, int index)
    cpdef autoSemantic(self, ParseTreeDrawable parseTree)
