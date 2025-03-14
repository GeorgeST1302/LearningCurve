from enum import Enum


class FuzzerAttackMode(str, Enum):
    PERSUASIVE = "per"
    TAXONOMY = "tax"
    GENETIC = "gen"
    HALLUCINATIONS = "hal"
    ARTPROMPT = "art"
    MANYSHOT = "man"
    PIGLATIN = "pig"
    DEFAULT = "def"
    PLEASE = "pls"
    BACKTOPAST = "pst"
    THOUGHTEXPERIMENT = "exp"
    WORDGAME = "wrd"
    GPTFUZZER = "fuz"
    DAN = "dan"
    CRESCENDO = "crs"
    ACTOR = "act"
    BON = "bon"
    ASCIISMUGGLING = "asc"