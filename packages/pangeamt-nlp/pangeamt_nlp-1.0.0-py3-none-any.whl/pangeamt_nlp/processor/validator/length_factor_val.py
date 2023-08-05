from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg


class LengthFactorVal(ValidatorBase):
    NAME = "length_factor_val"

    DESCRIPTION_TRAINING = """
            Remove pair if length factor is high between src and tgt
            Parameters: length_factor(int) by default 3
        """

    DESCRIPTION_DECODING = """
            Validators do not apply to decoding.
        """

    def __init__(self, src_lang: str, tgt_lang: str, length_factor=3) -> None:
        super().__init__(src_lang, tgt_lang)
        self._length_factor = float(length_factor)

    def validate(self, seg: Seg) -> bool:
        if len(seg.src) > len(seg.tgt) * self._length_factor or len(seg.tgt) > len(seg.src) * self._length_factor:
            return False
        return True
