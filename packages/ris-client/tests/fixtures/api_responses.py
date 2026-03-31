FEDERAL_LAW_RAW_DOC = {
    "Data": {
        "Metadaten": {
            "Technisch": {
                "ID": "NOR40238671",
                "Applikation": "BrKons",
            },
            "Allgemein": {
                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=BrKons&Dokumentnummer=NOR40238671",
            },
            "Bundesrecht": {
                "Kurztitel": "Mietrechtsgesetz",
                "Titel": "Bundesgesetz vom 12. November 1981 \u00fcber das Mietrecht (Mietrechtsgesetz \u2013 MRG)",
                "Abkuerzung": "MRG",
                "BrKons": {
                    "ArtikelParagraphAnlage": "\u00a7 30",
                    "Paragraphnummer": "30",
                    "Dokumenttyp": "NOR",
                    "Gesetzesnummer": "10002531",
                    "Typ": "BG",
                    "Abkuerzung": "MRG",
                    "Inkrafttretensdatum": "1982-01-01",
                    "Ausserkrafttretensdatum": None,
                    "Aenderung": "BGBl. I Nr. 58/2018",
                    "Indizes": {
                        "item": ["16/01 Allgemeines b\u00fcrgerliches Gesetzbuch", "23/01 Mietrecht"]
                    },
                    "Schlagworte": "K\u00fcndigung, wichtige Gr\u00fcnde",
                    "GesamteRechtsvorschriftUrl": "https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10002531",
                },
            },
        },
        "Dokumentliste": {
            "ContentReference": {
                "ContentType": "MainDocument",
                "Name": "\u00a7 30 MRG",
                "Urls": {
                    "ContentUrl": {
                        "DataType": "Html",
                        "Url": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=BrKons&Dokumentnummer=NOR40238671&ResultFunctionToken=abc",
                    }
                },
            }
        },
    }
}

# A second federal law doc (different law) for deduplication testing
FEDERAL_LAW_RAW_DOC_2 = {
    "Data": {
        "Metadaten": {
            "Technisch": {
                "ID": "NOR40100001",
                "Applikation": "BrKons",
            },
            "Allgemein": {
                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=BrKons&Dokumentnummer=NOR40100001",
            },
            "Bundesrecht": {
                "Kurztitel": "ABGB",
                "Titel": "Allgemeines b\u00fcrgerliches Gesetzbuch",
                "Abkuerzung": "ABGB",
                "BrKons": {
                    "ArtikelParagraphAnlage": "\u00a7 1090",
                    "Paragraphnummer": "1090",
                    "Dokumenttyp": "NOR",
                    "Gesetzesnummer": "10001622",
                    "Typ": "BG",
                    "Abkuerzung": "ABGB",
                    "Inkrafttretensdatum": "1812-01-01",
                    "Ausserkrafttretensdatum": None,
                    "Aenderung": "",
                    "Indizes": {
                        "item": "16/01 Allgemeines b\u00fcrgerliches Gesetzbuch"
                    },
                    "Schlagworte": "Bestandvertrag",
                    "GesamteRechtsvorschriftUrl": "https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001622",
                },
            },
        },
        "Dokumentliste": None,
    }
}

# A duplicate: same law_number as FEDERAL_LAW_RAW_DOC but different section
FEDERAL_LAW_RAW_DOC_DUPLICATE = {
    "Data": {
        "Metadaten": {
            "Technisch": {
                "ID": "NOR40238672",
                "Applikation": "BrKons",
            },
            "Allgemein": {
                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=BrKons&Dokumentnummer=NOR40238672",
            },
            "Bundesrecht": {
                "Kurztitel": "Mietrechtsgesetz",
                "Titel": "Bundesgesetz vom 12. November 1981 \u00fcber das Mietrecht (Mietrechtsgesetz \u2013 MRG)",
                "Abkuerzung": "MRG",
                "BrKons": {
                    "ArtikelParagraphAnlage": "\u00a7 31",
                    "Paragraphnummer": "31",
                    "Dokumenttyp": "NOR",
                    "Gesetzesnummer": "10002531",
                    "Typ": "BG",
                    "Abkuerzung": "MRG",
                    "Inkrafttretensdatum": "1982-01-01",
                    "Aenderung": "BGBl. I Nr. 58/2018",
                    "Indizes": {"item": ["23/01 Mietrecht"]},
                    "Schlagworte": "",
                    "GesamteRechtsvorschriftUrl": "https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10002531",
                },
            },
        },
        "Dokumentliste": None,
    }
}


CASE_LAW_RAW_DOC = {
    "Data": {
        "Metadaten": {
            "Technisch": {
                "ID": "JJR_20150901_OGH0002_0020OB00156_15B0000_001",
                "Applikation": "Justiz",
                "Organ": "OGH",
            },
            "Allgemein": {
                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJR_20150901",
            },
            "Judikatur": {
                "Dokumenttyp": "Rechtssatz",
                "Geschaeftszahl": {
                    "item": ["2 Ob 156/15b", "5 Ob 100/14s"]
                },
                "Entscheidungsdatum": "2015-09-01",
                "EuropeanCaseLawIdentifier": "ECLI:AT:OGH0002:2015:0020OB00156.15B.0901.000",
                "Normen": {
                    "item": ["MRG \u00a7 30 Abs 2", "MRG \u00a7 30 Abs 2 Z 4"]
                },
                "Schlagworte": "K\u00fcndigung, erheblich nachteiliger Gebrauch",
                "GesamteEntscheidungUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Ges=123",
                "RechtssaetzeUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Rs=123",
                "Justiz": {
                    "Gericht": "OGH",
                    "Rechtsgebiete": {
                        "item": "Zivilrecht"
                    },
                    "Fachgebiete": {
                        "item": ["Bestandrecht", "Mietrecht"]
                    },
                    "Rechtssatznummern": {
                        "item": "RS0067816"
                    },
                    "Entscheidungstexte": {
                        "item": [
                            {
                                "Geschaeftszahl": "2 Ob 156/15b",
                                "Dokumenttyp": "Text",
                                "Gericht": "OGH",
                                "Entscheidungsdatum": "2015-09-01",
                                "Anmerkung": "Verst\u00e4rkter Senat",
                                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20150901",
                            },
                            {
                                "Geschaeftszahl": "5 Ob 100/14s",
                                "Dokumenttyp": "Text",
                                "Gericht": "OGH",
                                "Entscheidungsdatum": "2014-11-15",
                                "Anmerkung": "",
                                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20141115",
                            },
                        ]
                    },
                },
            },
        },
        "Dokumentliste": {
            "ContentReference": [
                {
                    "ContentType": "MainDocument",
                    "Name": "Rechtssatz",
                    "Urls": {
                        "ContentUrl": [
                            {
                                "DataType": "Html",
                                "Url": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJR_20150901&Html=true",
                            },
                            {
                                "DataType": "Xml",
                                "Url": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJR_20150901&Xml=true",
                            },
                        ]
                    },
                },
                {
                    "ContentType": "Attachment",
                    "Name": "Beilage",
                    "Urls": {
                        "ContentUrl": {
                            "DataType": "Pdf",
                            "Url": "https://example.com/attachment.pdf",
                        }
                    },
                },
            ]
        },
    }
}

# Case law doc without linked decisions (Entscheidungstext)
CASE_LAW_RAW_DOC_DECISION = {
    "Data": {
        "Metadaten": {
            "Technisch": {
                "ID": "JJT_20200115_OGH0002_0010OB00200_19X0000_000",
                "Applikation": "Justiz",
                "Organ": "OGH",
            },
            "Allgemein": {
                "DokumentUrl": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20200115",
            },
            "Judikatur": {
                "Dokumenttyp": "Text",
                "Geschaeftszahl": {
                    "item": "1 Ob 200/19x"
                },
                "Entscheidungsdatum": "2020-01-15",
                "EuropeanCaseLawIdentifier": "",
                "Normen": {
                    "item": "ABGB \u00a7 1295"
                },
                "Schlagworte": "Schadenersatz",
                "GesamteEntscheidungUrl": "",
                "RechtssaetzeUrl": "",
                "Justiz": {
                    "Gericht": "OGH",
                    "Rechtsgebiete": {
                        "item": "Zivilrecht"
                    },
                    "Fachgebiete": {},
                    "Rechtssatznummern": {},
                    "Entscheidungstexte": {},
                },
            },
        },
        "Dokumentliste": {
            "ContentReference": {
                "ContentType": "MainDocument",
                "Name": "Volltext",
                "Urls": {
                    "ContentUrl": {
                        "DataType": "Html",
                        "Url": "https://www.ris.bka.gv.at/Dokument.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20200115&Html=true",
                    }
                },
            }
        },
    }
}


def make_search_result(doc_refs, hits=None):
    if hits is None:
        hits = len(doc_refs) if isinstance(doc_refs, list) else (1 if doc_refs else 0)

    if isinstance(doc_refs, list) and len(doc_refs) == 1:
        doc_refs = doc_refs[0]

    result = {
        "OgdSearchResult": {
            "OgdDocumentResults": {
                "Hits": {"#text": str(hits)},
                "OgdDocumentReference": doc_refs,
            }
        }
    }
    return result


def make_empty_search_result():
    return {
        "OgdSearchResult": {
            "OgdDocumentResults": {
                "Hits": {"#text": "0"},
            }
        }
    }


def make_error_result(application="BrKons", message="Ung\u00fcltige Abfrage"):
    return {
        "OgdSearchResult": {
            "Error": {
                "Applikation": application,
                "Message": message,
            }
        }
    }
