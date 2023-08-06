from dataclasses import dataclass
from typing import Optional, Union
from collections.abc import Iterable

from pyparsing import (And, Char, Combine, Empty, Forward, Group, MatchFirst,
                       Or, Suppress, Word, WordEnd, WordStart,
                       ZeroOrMore, alphas, matchPreviousLiteral, nums, FollowedBy)

from .dtmf import NumWord, BOOLEAN, DTMF_CHARS, EnumValue

from .tables import CWCharacter

PORT = Char('123')
CW_CHARACTER = EnumValue(CWCharacter, 2)
MESSAGE = Forward()


class MessageControlCharacter:
    @classmethod
    def from_dtmf(cls, tokens):
        return cls(**tokens[0].asDict())

    def to_dtmf(self) -> str:
        raise NotImplementedError()

    @classmethod
    def get_parser(cls):
        return cls.parser.copy() \
                         .setParseAction(cls.from_dtmf) \
                         .setName(cls.__name__)


# @dataclass
# class RouteMessage(MessageControlCharacter):
#     code = 97
#     parser = Group(Suppress(code) +
#                    PORT('ports*') +
#                    ((PORT('ports*') + (PORT('ports*') + '0')[0, 1]) ^ '0'))

#     ports: Iterable[str]

#     def to_dtmf(self):
#         port_str = ''.join(self.ports)
#         # if length is odd, make even
#         if len(port_str) % 2 != 0:
#             port_str += '0'
#         return self.code + port_str


class CharacterMode(MessageControlCharacter):
    pass


@dataclass
class CW(CharacterMode):
    @dataclass
    class SpeedChange(MessageControlCharacter):
        code = "9903"
        parser = Group(Suppress(code))

    @dataclass
    class FrequencyChange(MessageControlCharacter):
        code = "9904"
        parser = Group(Suppress(code))

    @dataclass
    class MessageLevel(MessageControlCharacter):
        code = "9905"
        parser = Group(Suppress(code))

    CONTROL = Or([c.get_parser() for c in [SpeedChange, FrequencyChange, MessageLevel]])

    code = "990"
    parser = Group(Suppress(code) + Char("012")("interrupt") +
                   (CW_CHARACTER ^ CONTROL)[1, ...]('message*'))

    interrupt: str
    message: Iterable[Union[CWCharacter, MessageControlCharacter]]

    def to_dtmf(self):
        return f'{self.code}{self.interrupt} {self.message}'


@dataclass
class SingleToneBeep(CharacterMode):
    @dataclass
    class MessageLevel(MessageControlCharacter):
        code = "9913"
        parser = Group(Suppress(code))

    code = "991"
    parser = Group(Suppress(code) + Char("012")("interrupt"))


class DualToneBeep(CharacterMode):
    code = "991"
    parser = Group(Suppress(code) + Char("567")("interrupt"))

    interupt: str

    class MessageLevel(MessageControlCharacter):
        code = "9918"
        parser = Group(Suppress(code))


@dataclass
class Speech(CharacterMode):
    # TODO: vocab/custom audio lookup

    @dataclass
    class MessageLevel(MessageControlCharacter):
        code = "9963"
        parser = Group(Suppress(code) + NumWord(2)('level'))

        level: str

        def to_dtmf(self):
            return f'{self.code} {self.level}'

    code = "996"
    parser = Group(Suppress(code) +
                   Char("012")("interrupt") +
                   # TODO: this should also allow for some other control characters probably
                   Or(Word('01234', nums, exact=4),
                      ('70' + NumWord(2))  # TODO: Intra-message Delay
                      # TODO: SpeechMessageLevel
                      )('words*'))

    words: Iterable[str]
    interrupt: str = "0"

    def to_dtmf(self):
        return f'{self.code}{self.interrupt} {" ".join(self.words)}'


# Paging

@dataclass
class SingleTonePage(MessageControlCharacter):
    code = "9920"
    parser = Group(Suppress(code) + NumWord(4)('tone_code') + NumWord(2)('duration'))

    tone_code: str
    duration: str

    def to_dtmf(self):
        return f'{self.code} {self.tone_code} {self.duration}'


@dataclass
class TwoToneSequentialPage(MessageControlCharacter):
    code = "9930"
    parser = Group(Suppress(code) +
                   NumWord(4)('first_tone_code') +
                   NumWord(2)('first_tone_duration') +
                   NumWord(4)('second_tone_code') +
                   NumWord(2)('second_tone_duration'))

    first_tone_code: str
    first_tone_duration: str
    second_tone_code: str
    second_tone_duration: str

    def to_dtmf(self):
        return f'{self.code} {self.first_tone_code} {self.first_tone_duration} {self.second_tone_code} {self.second_tone_duration}'


@dataclass
class FiveSixTonePage(MessageControlCharacter):
    code = "9940"
    parser = Group(Suppress(code) +
                   Char(nums)('preamble') +
                   NumWord(5)('digits') +
                   BOOLEAN('dual_address') +
                   # Bogus padding character if not at end of message
                   # TODO: this could probably be more robust
                   (FollowedBy('*') ^ Char(DTMF_CHARS)('bogus')))

    preamble: str
    digits: str
    dual_address: str
    bogus: Optional[str] = None

    def to_dtmf(self):
        return f'{self.code} {self.preamble} {self.digits} {self.dual_address} {self.bogus or ""}'


@dataclass
class DTMFPage(MessageControlCharacter):
    # TODO: the dtmf characters are a lot more complicated
    code = "9950"
    parser = Group(Suppress(code) + NumWord(2)('characters*')[1, ...])

    characters: Iterable[str]

    def to_dtmf(self):
        return f'{self.code} {" ".join(self.characters)}'


@dataclass
class SELCALPage(MessageControlCharacter):
    # TODO: SELCAL character table
    code = "9955"
    parser = Group(Suppress(code) + NumWord(2)('tones*'))

    tones: Iterable[str]

    def to_dtmf(self):
        return f'{self.code} {" ".join(self.tones)}'




# "Mixed Audio Allowed": Group(Suppress("9991"))
# "Non-Mixed Audio Only": Group(Suppress("9992"))


@dataclass
class Pause(MessageControlCharacter):
    code = '9993'
    parser = Group(Suppress(code) + NumWord(2)('delay'))

    delay: str

    def to_dtmf(self):
        return f'{self.code} {self.delay}'

# "Queue for executing the macro that follows": Group(Suppress("9999"))


MESSAGE = Or([char.get_parser() for char in CharacterMode.__subclasses__()])
