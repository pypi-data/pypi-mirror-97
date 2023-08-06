import os
from library_wrector.gector.gec_model import GecBERTModel

here = os.path.abspath(os.path.dirname(__file__))

vocab_path = os.path.join(here, "data/output_vocabulary")

class Wrector:
    def __init__(
            self, 
            nlp, 
            model_paths, 
            vocab_path=vocab_path,
            max_len=50,
            min_len=3,
            iterations=5,
            min_error_probability=0.41,
            min_probability=0.0,
            lowercase_tokens=0,
            model_name="bert",
            special_tokens_fix=1,
            log=False,
            confidence=0.1,
            is_ensemble=0,
            weigths=None,
            device="cpu"
        ):
        self.model = GecBERTModel(vocab_path=vocab_path,
                                model_paths=model_paths,
                                max_len=max_len, 
                                min_len=min_len,
                                iterations=iterations,
                                min_error_probability=min_error_probability,
                                min_probability=min_probability,
                                lowercase_tokens=lowercase_tokens,
                                model_name=model_name,
                                special_tokens_fix=special_tokens_fix,
                                log=log,
                                confidence=confidence,
                                is_ensemble=is_ensemble,
                                weigths=weigths,
                                device=device)
        self.nlp = nlp

    def tokenize(self, doc):
        try:
            doc.text
        except AttributeError:
            doc = self.nlp(doc, disable=['parser', 'tagger', 'ner'])
        return [token.text for token in doc]

    
    def __call__(self, sent):
        sent_tokenized = self.tokenize(sent)
        preds, cnt = self.model.handle_batch([sent_tokenized])
        if len(preds):
            return " ".join(preds[0])
        return sent
