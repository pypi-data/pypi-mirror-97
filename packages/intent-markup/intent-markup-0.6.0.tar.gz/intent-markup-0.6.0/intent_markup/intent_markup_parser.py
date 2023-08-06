import xml.etree.ElementTree as xml
from typing import Union

from intent_markup.intent_markup import IntentMarkup, MustWord


class IntentMarkupParser:

    @staticmethod
    def parse(raw_xml: Union[str, bytes]):
        def parse_must_words(element: xml.Element):
            text = element.text
            fuzzy = element.attrib["fuzzy"] == "true" if "fuzzy" in element.attrib else False
            return MustWord(text, fuzzy)

        def element_to_string(element):
            s = str(element.text) or ""
            for sub_element in element:
                s += element_to_string(sub_element)
            if element.tail is not None:
                s += element.tail
            return s

        try:
            parsed_xml = xml.fromstring("<markup>"+raw_xml+"</markup>")
            if parsed_xml.find(".//intent") is None:
                return IntentMarkup(True, raw_xml, [])
            else:
                intent = parsed_xml.find(".//intent")
                autocomplete = intent.attrib["autocomplete"] == "true" if "autocomplete" in intent.attrib else True
                value = element_to_string(intent)
                must_words = list(map(parse_must_words,intent.findall("must")))
                return IntentMarkup(autocomplete, value, must_words)
        except xml.ParseError:
            raise ValueError("A parse error was thrown when parsing " + raw_xml)

