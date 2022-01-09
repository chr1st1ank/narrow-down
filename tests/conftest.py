"""Common fixtures for the test modules."""
import pytest


@pytest.fixture
def sample_byte_strings():
    """Return a list of byte arbitrary byte strings."""
    return [
        b"QHtbc3lzdGVtICJ0b3VjaCAvdG1wL2JsbnMuZmFpbCJdfQ==",
        b"ZXZhbCgicHV0cyAnaGVsbG8gd29ybGQnIik=",
        b"U3lzdGVtKCJscyAtYWwgLyIp",
        b"YGxzIC1hbCAvYA==",
        b"S2VybmVsLmV4ZWMoImxzIC1hbCAvIik=",
        b"S2VybmVsLmV4aXQoMSk=",
        b"JXgoJ2xzIC1hbCAvJyk=",
        b"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/PjwhRE9DVFlQRSBmb28g",
        b"WyA8IUVMRU1FTlQgZm9vIEFOWSA+PCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFz",
        b"c3dkIiA+XT48Zm9vPiZ4eGU7PC9mb28+",
        b"JEhPTUU=",
        b"JEVOVnsnSE9NRSd9",
        b"true",
        b"false",
        b"-1.00",
        b"-$1.00",
        b"-1/2",
        b"-1E2",
        b"0/0",
        b"-2147483648/-1",
        b"-9223372036854775808/-1",
        b"-0",
        b"-0.0",
        b"+0",
        b"+0.0",
    ]


@pytest.fixture
def sample_sentences_french():
    """Return a list of french sentences."""
    return [
        "Cocody, par déformation de Cocoly à l’origine, était une délégation comme les autres "
        "communes d’Abidjan.",
        "Né à partir d’un petit village qui était situé à l’emplacement du stade Géo-André, actuel "
        "Stade Félix Houphouët-Boigny, Cocody était habité par les autochtones Ébriés autrefois "
        "appelés « Tchamans ».",
        "Les Tchamans étaient répartis en onze fratries regroupées en six groupes ou « goto » dont "
        ": les Bidjans, les Djédo, les Gnagon, les Kowês et les Noutoua.",
        "Cocody est l’un des tout premiers villages d’Abidjan. C’est à la suite d'une bagarre "
        "entre les « tchamans » que sept villages se sont constitués.",
        "Blockauss, autrefois appelé Anokouaté, servait d’intermédiaire entre certains villages en "
        "litige.",
        "Cocody s’est vu petit à petit rapproché de Blockauss à la faveur de l’essor économique de "
        "1905, ce qui l’emmène sur les sites actuels de la Polyclinique Sainte-Anne-Marie. En "
        "1929, les sites de la savonnerie Blohorn l’entraînent au pied de l’Hôtel Ivoire non loin "
        "du village de Blochausso, actuel Blockauss.",
        "Cocody doit son essor économique à Abidjan alors érigée en capitale en 1934.",
        "En 1960, Cocody réalise ses premières constructions. Ce sont les 160 logements, dans le "
        "souci de loger tous les agents de l’État.",
        "29 ans plus tard, Cocody voit la naissance du nouveau quartier appelé Angré.",
        "Le 17 octobre 1980, Cocody est érigé en commune avec l’élection d’un maire par les "
        "conseillers municipaux. Dès lors, quatre (4) villages faisant autrefois partie de la "
        "sous-préfecture de Bingerville se rattachent à la commune. Ce sont Anono, M’pouto, "
        "M’badon et Akouédo.",
        "Arsène Usher Assouan fut le premier maire de la commune. Il a eu deux mandats : de 1980 à "
        "1990.",
        "De 1990 à 2000, ce fut Théodore Mel Eg avec deux mandats également.",
    ]
