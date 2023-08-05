from alphabet_detector import AlphabetDetector

from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg, SegCase

ad = AlphabetDetector()

class OnlyChineseCharsVal(ValidatorBase):
    NAME = "only_chinese_chars_val"

    DESCRIPTION_TRAINING = """
                Filter segments that have characters different than chinese
            """

    DESCRIPTION_DECODING = """
                Validators do not apply to decoding.
            """

    def __init__(self, src_lang: str, tgt_lang: str, length_factor=3) -> None:
        super().__init__(src_lang, tgt_lang)
        self.counter = 0

    def validate(self, seg: Seg) -> bool:
        if self.src_lang != 'zh' and self.tgt_lang != 'zh':
            return True

        chinese_line = ''

        if self.src_lang == 'zh':
            chinese_line = seg.src
        else:
            chinese_line = seg.tgt

        not_zh = 0
        for char in chinese_line:
            if not ad.is_cjk(char):
                not_zh += 1
                if len(chinese_line) * 0.5 < not_zh:
                    self.counter += 1
                    return False

        return True

