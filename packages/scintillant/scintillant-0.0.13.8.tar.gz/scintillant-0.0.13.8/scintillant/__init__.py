"""
Scintillant -a tool for quickly creating skills adapted to work with the
Dialog service - the central system of the Lilia chat bot.
"""

GITHUB = "https://github.com"
BOTTLE_SKILL_TEMPLATE_URL = (
        GITHUB + "/PaperDevil/bottle-skill-template/archive/develop.zip"
)
AIOHTTP_SKILL_TEMPLATE_URL = ""
FAST_API_SKILL_TEMPLATE_URL = ""

# get key package details from scintillant/__version__.py
about = {
    '__title__': 'scintillant',
    '__description__': 'Fast bot creating framework',
    '__version__': '0.0.13.8',
    '__author__': 'Niel Ketov',
    '__author_email__': 'ketov-x@yandex.ru',
    '__url__': 'https://code.tatar.ru/projects/LILIYA/repos/scintillant',
    '__license__': 'Apache 2.0'
}

addons_versions = {
    '__testsuite__': 'v0.0.1',
    '__bottle_skill_template__': ''
}
