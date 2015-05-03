import re

# import yaml


LEXEMS = {
    'name': r'[\w\-_]+',
    'key_separator': ':',
}

PATTERNS = {
    'streams': r'\>(?P<stream>{name})',
    'mentions': r'@(?P<mention>{name})',
    'privates': r'!(?P<private>{name})',
    'tags': r'#(?P<tag>{name}(?:{key_separator}{name})?)',
}

COMPILED_PATTERNS = {
    key: re.compile(value.format(**LEXEMS), flags=re.UNICODE)
    for key, value in PATTERNS.items()
}


class Blip(object):

    @classmethod
    def from_text(cls, text):
        blip = cls()
        blip.text = text
        for attr, pattern in COMPILED_PATTERNS.items():
            setattr(blip, attr, pattern.findall(text))
        return blip.populate_metadata()

    """
    @classmethod
    def from_yaml(cls, yaml_text):
        parsed = yaml.load(yaml_text)
        blip = cls()
        blip.__dict__ = parsed
        return blip.populate_metadata()
    """

    def populate_metadata(self):
        self.metadata = {}
        for tag in self.tags:
            try:
                key, value = tag.split(LEXEMS['key_separator'])
            except:
                pass
            else:
                self.metadata[key] = value
        return self

    def __getitem__(self, key):
        return self.metadata[key]
