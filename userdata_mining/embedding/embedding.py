from flair.data import Sentence
from flair.embeddings import TransformerDocumentEmbeddings


class Embedding:
    """
    Performs embedding on sentences.
    """

    def __init__(self, model='gpt2-large'):
        """
        Initializes the embedding model.

        :param {str} model - The model architecture. Must be one of
        https://huggingface.co/transformers/pretrained_models.html
        """
        self.model = TransformerDocumentEmbeddings(model)

    def embed(self, sentence: str) -> list:
        """
        Embeds a given sentence.

        :param {str} sentence - A cased or uncased sentence.
        """
        sent = Sentence(sentence)
        return self.model.embed(sent)
