from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class ApostrophePosprocess(NormalizerBase):
    NAME = "apostrophe_posprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Remove spaces around apostrophe
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        if self.tgt_lang not in ['fr', 'es']:
            words = []
            if self.tgt_lang == 'en':
                seg.tgt = seg.tgt.replace(' ’ m ', '’m ').replace('’ m ', '’m ').replace(' ’ re ', '’re ').replace('’ re ', '’re ').replace(' ’ s ', '’s ').replace('’ s ', '’s ')\
                    .replace(' ’ ve ', '’ve ').replace('’ ve ', '’ve ').replace(' ’ d ', '’d ').replace('’ d ', '’d ').replace(' ’ ll ', '’ll ').replace('’ ll ', '’ll ')
            else:
                seg.tgt = seg.tgt.replace(' ’ ', '’')
