from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode cimport IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector cimport NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet
from WordSenseDisambiguation.AutoProcessor.ParseTree.TreeAutoSemantic cimport TreeAutoSemantic

cdef class MostFrequentTreeAutoSemantic(TreeAutoSemantic):

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

    cpdef bint autoLabelSingleSemantics(self, ParseTreeDrawable parseTree):
        cdef NodeDrawableCollector nodeDrawableCollector
        cdef int i
        cdef list leafList
        cdef list synSets
        cdef SynSet best
        nodeDrawableCollector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leafList = nodeDrawableCollector.collect()
        for i in range(len(leafList)):
            synSets = self.getCandidateSynSets(self.__turkishWordNet, self.__fsm, leafList, i)
            if len(synSets) > 0:
                best = self.mostFrequent(synSets, leafList[i].getLayerInfo().getMorphologicalParseAt(0).getWord().getName())
                if best is not None:
                    leafList[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, best.getId())
        return True
