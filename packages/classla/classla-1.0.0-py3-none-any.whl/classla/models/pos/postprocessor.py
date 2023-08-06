class InflectionalLexiconProcessor(object):
    def __init__(self, lexicon, vocab, pretrain):
        pass

    """Base class for data converters for sequence classification data sets."""
    def process(self, padded_prediction, word_ids):
        raise NotImplementedError()


class SloveneInflectionalLexiconProcessor(InflectionalLexiconProcessor):
    def __init__(self, lexicon, vocab, pretrain):
        closed_classes_rules = ['P', 'S', 'C', 'Q', 'Z']

        # fills hypothesis_dictionary
        self.hypothesis_dictionary = {}
        # fallback for when xpos tag in influectional lexicon is not in vocab
        self.hypothesis_dictionary_fallback = {}
        self.extract_lexicon_data(lexicon, vocab['xpos'], pretrain.vocab)

        # fills closed_classes
        self.closed_classes = set()
        self.xpos_vocab = vocab['xpos']
        self.create_closed_classes(vocab['xpos'], closed_classes_rules)
        self.closed_classes_inverse = [vocab['xpos'][el] for el in vocab['xpos'] if vocab['xpos'][el] not in self.closed_classes]
        super(SloveneInflectionalLexiconProcessor, self).__init__(lexicon, vocab, pretrain)

    def process(self, padded_prediction, word_strings):
        predictions = []

        max_value = padded_prediction.max(2)[1]

        for sent_id, (sent_indices, sent_strings) in enumerate(zip(max_value, word_strings)):
            sent_predictions = []
            for word_id, (word_prediction, word_string) in enumerate(zip(sent_indices, sent_strings)):
                if word_string in self.hypothesis_dictionary:
                    # if only one possible prediction in hypothesis dictionary, take it!
                    if len(self.hypothesis_dictionary[word_string]) == 1:
                        prediction = self.hypothesis_dictionary[word_string][0]
                    elif self.xpos_vocab[word_prediction.item()] in self.hypothesis_dictionary[word_string]:
                        prediction = self.xpos_vocab[word_prediction.item()]
                    else:
                        optional_indices = [self.xpos_vocab[el] for el in self.hypothesis_dictionary[word_string]]
                        prediction = self.xpos_vocab[optional_indices[padded_prediction[sent_id, word_id, optional_indices].argmax().item()]]
                elif word_string in self.hypothesis_dictionary_fallback:
                    prediction = self.hypothesis_dictionary_fallback[word_string][0]
                else:
                    if word_prediction.item() not in self.closed_classes:
                        prediction = self.xpos_vocab[word_prediction.item()]
                    else:
                        prediction = self.xpos_vocab[self.closed_classes_inverse[padded_prediction[sent_id, word_id, self.closed_classes_inverse].argmax().item()]]
                sent_predictions.append(prediction)
            predictions.append(sent_predictions)
        return predictions

    def extract_lexicon_data(self, lexicon, vocab_xpos, vocab_words):
        """ Creates hypothesis dictionary from lexicon. """
        for key in lexicon.keys():
            if key[1] in vocab_xpos:
                self.hypothesis_dictionary.setdefault(key[0].lower(), []).append(key[1])
            else:
                self.hypothesis_dictionary_fallback.setdefault(key[0].lower(), []).append(key[1])

    def create_closed_classes(self, vocab, closed_classes_rules):
        """ Fills a set of closed classes, that contains xpos ids that are not permitted. """
        for key in vocab:
            if key[0] in closed_classes_rules:
                self.closed_classes.add(vocab[key])


processors = {"ssj": SloveneInflectionalLexiconProcessor, "sl_ssj": SloveneInflectionalLexiconProcessor}


class InflectionalLexicon:
    def __init__(self, lexicon, shorthand, vocab, pretrain):
        """Base class for data converters for sequence classification data sets."""
        self.shorthand = shorthand
        assert shorthand in processors, f"Tag {shorthand} is not supported by inflectional lexicon."
        self.processor = processors[shorthand](lexicon, vocab, pretrain)

    def process(self, padded_prediction, word_strings):
        return self.processor.process(padded_prediction, word_strings)
