from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.Sentence.SentenceAutoSemantic cimport SentenceAutoSemantic

cdef class MostFrequentSentenceAutoSemantic(SentenceAutoSemantic):

    cpdef WordNet __turkishWordNet
    cpdef FsmMorphologicalAnalyzer __fsm

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkishWordNet = turkishWordNet

    cpdef SynSet mostFrequent(self, list synSets, str root):
        cdef SynSet synSet, best
        cdef int minSense, i
        if len(synSets) == 1:
            return synSets[0]
        minSense = 50
        best = None
        for synSet in synSets:
            for i in range(synSet.getSynonym().literalSize()):
                if synSet.getSynonym().getLiteral(i).getName().lower().startswith(root) or synSet.getSynonym().getLiteral(i).getName().lower().endswith(" " + root):
                    if synSet.getSynonym().getLiteral(i).getSense() < minSense:
                        minSense = synSet.getSynonym().getLiteral(i).getSense()
                        best = synSet
        return best

    cpdef bint autoLabelSingleSemantics(self, AnnotatedSentence sentence):
        cdef int i
        cdef list synSets
        cdef SynSet best
        for i in range(sentence.wordCount()):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, sentence, i)
            if len(synSets) > 0:
                best = self.mostFrequent(synSets, sentence.getWord(i).getParse().getWord().getName())
                if best is not None:
                    sentence.getWord(i).setSemantic(best.getId())
        return True
