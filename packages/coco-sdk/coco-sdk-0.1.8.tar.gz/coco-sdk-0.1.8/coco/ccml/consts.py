from enum import Enum


class ChannelType(Enum):
    AWS_POLLY = "aws_polly"
    AMAZON = "amazon"
    GOOGLE = "google"
    TWILIO = "twilio"


CHANNEL_STORAGE_FOLDER = {
    ChannelType.AWS_POLLY.value: "alexa",
    ChannelType.AMAZON.value: "alexa",
    ChannelType.GOOGLE.value: "google",
    ChannelType.TWILIO.value: "alexa",
}

CCML_DICTIONARY = {
    ChannelType.AWS_POLLY.value: {
        "speak": None,
        "phoneme": None,
        "domain": "amazon:domain",
        "effect": "amazon:effect",
        "emotion": "amazon:emotion",
        "language": "lang",
        "part-of-speech": "w",
    },
    ChannelType.AMAZON.value: {
        "phoneme": None,
        "voice": None,
        "language": "lang",
        "part-of-speech": "w",
        "domain": "amazon:domain",
        "effect": "amazon:effect",
        "emotion": "amazon:emotion",
        "speak": None,
        "audio": None,
    },
    ChannelType.GOOGLE.value: {
        "mark": None,
        "media": None,
        "parallel": "par",
        "sequential": "seq",
        "speak": None,
        "audio": None,
    },
    ChannelType.TWILIO.value: {
        "part-of-speech": "w",
        "language": "lang",
        "phoneme": None,
    },
    "common": {
        "break": None,
        "say-as": None,
        "p": None,
        "s": None,
        "prosody": None,
        "emphasis": None,
        "sub": None,
    },
}
