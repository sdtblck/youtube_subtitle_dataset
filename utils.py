import pycountry

all_langs = pycountry.languages


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def lang_code_to_name(lang_code):
    lang = all_langs.get(alpha_2="{}".format(lang_code))
    if lang is None:
        lang = all_langs.get(alpha_3="{}".format(lang_code))
        if lang is None:
            # sometimes lang codes have a dash that then specifies regional dialect - just take the first part
            lang = all_langs.get(alpha_2="{}".format(lang_code.split("-")[0]))
            if lang is None:
                lang = all_langs.get(alpha_2="{}".format(lang_code.split("-")[0]))
                if lang is None:
                    if "zh" in lang_code:
                        # this should cover lots of regional zh langs (sorry to lump them all into one!)
                        lang = all_langs.get(alpha_2="{}".format("zh"))
                        if lang is None:
                            print('No language name found for {}, returning language code'.format(lang_code))
                            return lang_code
                    else:
                        return lang_code
    return lang.name
