from bs4 import BeautifulSoup
import requests
import cleantext
from pydantic.dataclasses import dataclass
from typing import List
from enum import Enum
from loguru import logger

# we want to bypass SSLError [SSL: DH_KEY_TOO_SMALL] dh key too small that occurs in recent OS (ubuntu 20.04+)
# we lower the standard level of security.
# It's ok, we don't really care as we only get open source non critical data
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

@dataclass
class Reference:
    ref: int
    description: str


class Detail(Enum):
    """hardcoded useful reference to retrieve data from rmn.

    `ref` can be passed to `collectdata`

    note: `Detail` is generated using `Meta` class
    """

    BIO = Reference(ref=3000, description="Bio magasins spécialisés")
    BIO_DRIVE = Reference(ref=3021, description="Bio magasins spécialisés (DRIVE)")
    FRUIT_GMS = Reference(ref=2503, description="Fruits France DETAIL GMS")
    LAIT_OEUF_GMS = Reference(ref=2504, description="Lait Oeuf DETAIL GMS")
    LEGUME_GMS = Reference(ref=2502, description="Légumes France DETAIL GMS")
    POISSON_GMS = Reference(ref=2500, description="Marée France DETAIL GMS")
    VIANDE_GMS = Reference(ref=2501, description="Viande France DETAIL GMS")


@dataclass
class Meta:
    url: str = "https://rnm.franceagrimer.fr/prix?MARCHES&TOUT&DETAIL"

    @staticmethod
    def get_id_page(url):
        try:
            return url.split("?")[1].split(":")[0]
        except IndexError:
            return ""

    @staticmethod
    def get_pair_id(soup: BeautifulSoup) -> Reference:
        """
        get tuple of (marche,description)
        """

        def clean_str(elt):
            return cleantext.clean(elt.text, lower=False, to_ascii=False)

        for elt in soup.select(".listunmarche"):
            yield Reference(
                ref=Meta.get_id_page(elt.a["href"])[1:], description=clean_str(elt.a)
            )

    def get(self) -> List[Reference]:
        """retrieve references to be used as input for query"""
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text)
        return list(self.get_pair_id(soup))


@dataclass
class Collect:
    baseurl: str = "https://rnm.franceagrimer.fr/prix"

    def collectdata(self,marche: Reference, deb: str, fin: str) -> str:
        """dump une periode du site rnm.franceagrimer.fr

        Parameters
        ----------
        marche: 
            code (e.g. '3000')
        deb: 
            debut de l'interval au format(fr): '01-01-2019'
        fin: 
            fin de l'interval au format(fr): '01-01-2019'
        """
        logger.info(f"marche:{marche.ref},deb:{deb},fin:{fin}")
        payload = {"MARCHE_HISTO": marche.ref, "DEB": deb, "FIN": fin}
        resp = requests.post(self.baseurl, payload)
        resp.raise_for_status()
        text = resp.text
        nb_lines = len(text.split("\n"))
        logger.info(f"response nb lines: {nb_lines}")
        return resp.text
