from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord

cdef class SentenceAutoSemantic:

    cpdef bint autoLabelSingleSemantics(self, AnnotatedSentence sentence):
        """
        The method should set the senses of all words, for which there is only one possible sense.

        PARAMETERS
        ----------
        sentence: AnnotatedSentence
            The sentence for which word sense disambiguation will be determined automatically.
        """
        pass

    cpdef list getCandidateSynSets(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, AnnotatedSentence sentence, int index):
        cdef AnnotatedWord twoPrevious, previous, twoNext, next, current
        cdef list synSets
        twoPrevious = None
        previous = None
        twoNext = None
        next = None
        current = sentence.getWord(index)
        if index > 1:
            twoPrevious = sentence.getWord(index - 2)
        if index > 0:
            previous = sentence.getWord(index - 1)
        if index != sentence.wordCount() - 1:
            next = sentence.getWord(index + 1)
        if index < sentence.wordCount() - 2:
            twoNext = sentence.getWord(index + 2)
        synSets = wordNet.constructSynSets(current.getParse().getWord().getName(),
                current.getParse(), current.getMetamorphicParse(), fsm)
        if twoPrevious is not None and twoPrevious.getParse() is not None and previous.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, twoPrevious.getParse(), twoPrevious.getMetamorphicParse(),
                                                         previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse()))
        if previous is not None and previous.getParse() is not None and next is not None and next.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse()))
        if next is not None and next.getParse() is not None and twoNext is not None and twoNext.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse(),
                                                         twoNext.getParse(), twoNext.getMetamorphicParse()))
        if previous is not None and previous.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse()))
        if next is not None and next.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(fsm, current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse()))
        return synSets

    cpdef autoSemantic(self, AnnotatedSentence sentence):
        if self.autoLabelSingleSemantics(sentence):
            sentence.save()
