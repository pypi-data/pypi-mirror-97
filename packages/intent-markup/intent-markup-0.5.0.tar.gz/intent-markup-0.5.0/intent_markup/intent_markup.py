from dataclasses import dataclass


@dataclass
class IntentMarkup:
    autocomplete: bool
    text: str
    musts: ['MustWord']


@dataclass
class MustWord:
    text: str
    fuzzy: bool
