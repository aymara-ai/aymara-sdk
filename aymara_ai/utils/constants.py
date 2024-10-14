from enum import Enum
from typing import List

POLLING_INTERVAL = 1  # seconds

# Test Creation Defaults
DEFAULT_MAX_WAIT_TIME_SECS: int = 120
DEFAULT_NUM_QUESTIONS: int = 20
DEFAULT_TEST_LANGUAGE: str = "en"

# Input Limit Defaults
DEFAULT_TEST_NAME_LEN_MIN: int = 1
DEFAULT_TEST_NAME_LEN_MAX: int = 100
DEFAULT_NUM_QUESTIONS_MIN: int = 1
DEFAULT_NUM_QUESTIONS_MAX: int = 150
DEFAULT_CHAR_TO_TOKEN_MULTIPLIER: float = 0.15
DEFAULT_MAX_TOKENS: int = 100000

# SUPPORTED LANGUAGES
SUPPORTED_LANGUAGES: List[str] = ["en"]


AYMARA_TEST_POLICY_PREFIX = "aymara_test_policy:"


class AymaraTestPolicy(Enum):
    """
    Aymara Test Policy
    """

    ANIMAL_ABUSE = "animal_abuse"
    CHILD_ABUSE = "child_abuse"
    CONTROVERSIES_POLITICS = "controversies_politics"
    BIAS_DISCRIMINATION = "bias_discrimination"
    DRUGS_WEAPONS = "drugs_weapons"
    THEFT_FINANCIAL_CRIME = "theft_financial_crime"
    HATE_OFFENSIVE_SPEECH = "hate_offensive_speech"
    MISINFORMATION = "misinformation"
    UNETHICAL_BEHAVIOR = "unethical_behavior"
    PRIVACY_VIOLATION = "privacy_violation"
    SELF_HARM = "self_harm"
    SEXUALLY_EXPLICIT = "sexually_explicit"
    TERRORISM_ORGANIZED_CRIME = "terrorism_organized_crime"
    VIOLENCE = "violence"
