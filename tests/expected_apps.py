"""The 23 apps measured as published on Google Play on 4 October 2026 (23 of 23 answered HTTP 200).

Kept apart from src/apps.json on purpose: the tests compare the site with this independent list,
so a package dropped from or added to the generator is noticed. Not a test module.
"""
APPS = {
    "com.hezarfen.adhdflow": ("adhdflow", "ADHDFlow"),
    "com.hezarfen.aqualog": ("aqualog", "AquaLog"),
    "com.hezarfen.backlogbloom": ("backlogbloom", "Backlog Bloom"),
    "com.hezarfen.blockzen": ("blockzen", "Block Zen"),
    "com.hezarfen.bloombyte": ("bloombyte", "BloomByte"),
    "com.hezarfen.carnivorouslog": ("carnivorouslog", "CarnivorousLog"),
    "com.hezarfen.catpulse": ("catpulse", "CatPulse"),
    "com.brilliant.wellbeing": ("clocktopus", "Clocktopus"),
    "com.hezarfen.dogpulse": ("dogpulse", "DogPulse"),
    "com.hezarfen.doomscroll": ("doomscroll", "Doom Scroll"),
    "com.hezarfen.echoharbor": ("echoharbor", "EchoHarbor"),
    "com.hezarfen.glowfox": ("glowfox", "GlowFox"),
    "com.hezarfen.gracerhythm": ("gracerhythm", "GraceRhythm"),
    "com.hezarfen.kinlore.app": ("kinlore", "Kinlore"),
    "com.hezarfen.managergym": ("leadrehearse", "LeadRehearse"),
    "com.hezarfen.nestnote": ("nestnote", "NestNote"),
    "com.hezarfen.pathwayslab": ("pathwayslab", "Pathways Lab"),
    "com.hezarfen.platekind": ("platekind", "PlateKind"),
    "com.hezarfen.pulsepatch": ("pulsepatch", "PulsePatch"),
    "com.hezarfen.recalldock": ("recalldock", "RecallDock"),
    "com.hezarfen.stroopsprint": ("stroopsprint", "Stroop Sprint"),
    "com.hezarfen.tidemind": ("tidemind", "TideMind"),
    "com.hezarfen.tinybroadcast": ("tinybroadcast", "Tiny Broadcast"),
}
PACKAGES = set(APPS)
