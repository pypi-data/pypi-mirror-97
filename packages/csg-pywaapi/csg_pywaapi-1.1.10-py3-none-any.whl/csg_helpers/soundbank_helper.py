bankTransforms = [

    [
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    #### For a project, I'm not sure it is useful to know if decendants are in a soundbank, as that does not mean the selected object is
    # [
    #     {"select": ['descendants']},
    #     {"select": ['referencesTo']},
    #     {"where": ['type:isIn', ['SoundBank']]},
    #     "distinct",
    # ],

    [
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['Action']]},
        "distinct",
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],
    ####### For a project, I'm not sure it is useful to know if decendants are in a soundbank, as that does not mean the selected object is
    # [
    #     {"select": ['descendants']},
    #     {"select": ['referencesTo']},
    #     {"where": ['type:isIn', ['Action']]},
    #     "distinct",
    #     {"select": ['ancestors']},
    #     {"select": ['referencesTo']},
    #     {"where": ['type:isIn', ['SoundBank']]},
    #     "distinct",
    # ],

    [
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['Action']]},
        "distinct",
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],
]