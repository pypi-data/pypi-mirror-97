from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class FrenchApostrophationPosprocess(NormalizerBase):
    NAME = "french_apostrophation_posprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Remove spaces around french apostrophe
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        if self.tgt_lang == 'fr':
            seg.tgt = seg.tgt.replace(" jusqu ’ ", " jusqu’").replace(" qu ’ ", " qu’").replace(" l ’ ", " l’").replace(" t ’ ", " t’").replace(" m ’ ", " m’").replace(" c ’ ", " c’").replace(" d ’ ", " d’").replace(" n ’ ", " n’").replace(" s ’ ", " s’").replace("L ’ ", "L’").replace("C ’ ", "C’").replace("D ’ ", "D’")