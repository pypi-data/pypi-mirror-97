from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
from pangeamt_nlp.utils.strip_and_catch_white import strip_and_catch_white


class DetokBlanksSlashQuotes(NormalizerBase):
    NAME = "detok_blanks_norm"
    DESCRIPTION_TRAINING = """
    """
    DESCRIPTION_DECODING = """
          Remove spaces next to slashes and quotes
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        seg.tgt = seg.tgt.replace(" / ", "/").replace(" ”", "”").\
            replace("http:// ", "http://").replace("https:// ", "https://").\
            replace("# ", "#").replace(" @ ", "@").replace("o ’ clock", "o’clock").replace("o’ clock", "o’clock").replace("m ²", "m²")


