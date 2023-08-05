"""yt_core
This module should ease the development of inofficial youtube apps.
The main class you are going to use is yt_core.Core.
(some lines you're were writing anyway can be found in yt_core.helper)
"""
#    This file is part of yt_core.
#
#    yt_core is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    yt_core is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with yt_core.  If not, see <http://www.gnu.org/licenses/>.
#

from ._Search import Search
from ._Video import Video
from ._dl import Downloader

# Yes, we really want everything in helper imported as yt_core.helperfunction
from .helper import *

# It's fun writing parse-code. There is no fun in writing
# this side of the interface where the humans are ;)


class Core:
    """yt_core.Core is needed for all the other classes in this library.
    This base class includes all the basic info the other classes need like Localization."""

    def __init__(self, language="de", country="DE"):
        """Initalizes the yt_core.Core class."""
        self._dl = Downloader(self)
        self.update_localization(language, country)

    def new_search(self, searchterm="", filters=list()):
        """Returns a search object
        Use help(yt_core.Search)!
        """
        return Search(self, searchterm=searchterm, filters=filters)

    def new_video(self, videoId):
        """Returns a video object
        Use help(yt_core.Video)!
        """
        return Video(self, videoId)

    # https://www.youtube.com/picker_ajax?action_country_json=1
    # youtube doesnt return anything from there anymore.
    def get_countrylist_from_youtube(self):
        """(Currently OUT OF ORDER) Downloads the currently supported countries from youtube."""
        #request = self._dl.local_country()
        #return self._parse_local_from_youtube(request)
        return self.get_countrylist_from_self() 

    # https://www.youtube.com/picker_ajax?action_language_json=1
    # youtube doesnt return anything from there anymore.
    def get_languagelist_from_youtube(self):
        """(Currently OUT OF ORDER) Downloads the currently supported languages from youtube."""
        #request = self._dl.local_language()
        #return self._parse_local_from_youtube(request)
        return self.get_languagelist_from_self()

    def _parse_local_from_youtube(self, raw):
        out = list()
        # I know, this isnt resilliant.
        if len(raw["data"]) == 2:
            array = raw["data"][1]
        else:
            array = raw["data"]
        for i in array:
            # (valid) Languages have 3 elements inside an array.
            # (language_code, name, choosen)
            if len(i) == 3:
                lang = [i[0], i[1]]
                out.append(lang)
            # countries 4. (preferred, country_code, name, choosen)
            if len(i) == 4:
                country = [i[1], i[2], i[0]]
                out.append(country)
        return out

    def get_countrylist_from_self(self):
        """Returns the cached country list in this object."""
        return self._country_list

    def update_country_list(self):
        """Downloads the current country list and sets it in this object."""
        self._country_list = self.get_countrylist_from_youtube()

    def get_languagelist_from_self(self):
        """Returns the language list in this object."""
        return self._language_list

    def update_language_list(self):
        """Downloads the current language list and sets it in this object."""
        self._language_list = self.get_languagelist_from_youtube()

    def get_current_language(self):
        """Returns the currently selected language.
        Returns [language_code:str, language_name:str]"""
        return self._language_current

    def get_current_country(self):
        """Returns the currently selected country.
        Returns [country_code:str, country_name:str, preferred_localization_for_country:str]"""
        return self._country_current

    def update_localization(self, language, country):
        """Sets the current language and country.
        Accepts both language's names and codes. Same for countries.
        If the language or country isn't found in the local cache it will try to download the current list from youtube."""
        self._update_language(language)
        self._update_country(country)
        self._update_header()

    def update_language(self, lang):
        """Sets the current language.
        Accepts both the name and the code as input.
        If the language isn't found in the local cache it will try to download the current list from youtube."""
        self._update_language(lang)
        self._update_header()

    def _update_language(self, lang, first_run=True):
        found = False
        for i in self._language_list:
            for u in i:
                if lang.lower() == u.lower():
                    found = True
                    self._language_current = i
        if found:
            pass
        elif first_run:
            self._language_list = self.get_languagelist_from_youtube()
            self._update_language(lang, first_run=False)
        else:
            pass  # FIXME: CREATE CUSTOM ERROR EXPECTION

    def update_country(self, country):
        """Sets the current country.
        Accepts both the name and the code as input.
        If the country isn't found in the local cache it will try to download the current list from youtube."""
        self._update_country(country)
        self._update_header()

    def _update_country(self, country, first_run=True):
        found = False
        for i in self._country_list:
            for u in i:
                if country.lower() == u.lower():
                    found = True
                    self._country_current = i
        if found:
            pass
        elif first_run:
            self._country_list = self.get_countrylist_from_youtube()
            self._update_country(country, first_run=False)
        else:
            pass  # FIXME: CREATE CUSTOM ERROR EXPECTION

    def _update_header(self):
        self._dl.YT_Headers["Accept-Language"] = self._language_current[0] + \
            "-" + self._country_current[0]

    _dl = None
    _language_current = ["de", "deutsch"]
    _country_current = ["DE", "Deutschland"]

    # Retrieved at 4.12.2020.
    _language_list = [['af', 'Afrikaans'], ['az', 'Azərbaycan'], ['id', 'Bahasa Indonesia'], ['ms', 'Bahasa Malaysia'], ['bs', 'Bosanski'], ['ca', 'Català'], ['cs', 'Čeština'], ['da', 'Dansk'], ['de', 'Deutsch'], ['et', 'Eesti'], ['en-IN', 'English (India)'], ['en-GB', 'English (UK)'], ['en', 'English (US)'], ['es', 'Español (España)'], ['es-419', 'Español (Latinoamérica)'], ['es-US', 'Español (US)'], ['eu', 'Euskara'], ['fil', 'Filipino'], ['fr', 'Français'], ['fr-CA', 'Français (Canada)'], ['gl', 'Galego'], ['hr', 'Hrvatski'], ['zu', 'IsiZulu'], ['is', 'Íslenska'], ['it', 'Italiano'], ['sw', 'Kiswahili'], ['lv', 'Latviešu valoda'], ['lt', 'Lietuvių'], ['hu', 'Magyar'], ['nl', 'Nederlands'], ['no', 'Norsk'], ['uz', 'O‘zbek'], ['pl', 'Polski'], ['pt-PT', 'Português'], ['pt', 'Português (Brasil)'], ['ro', 'Română'], ['sq', 'Shqip'], ['sk', 'Slovenčina'], ['sl', 'Slovenščina'], ['sr-Latn', 'Srpski'], ['fi', 'Suomi'], ['sv', 'Svenska'], ['vi', 'Tiếng Việt'], ['tr', 'Türkçe'], ['be', 'Беларуская'], ['bg', 'Български'], ['ky', 'Кыргызча'], ['kk', 'Қазақ Тілі'], ['mk', 'Македонски'], ['mn', 'Монгол'], ['ru', 'Русский'], ['sr', 'Српски'], ['uk', 'Українська'], ['el', 'Ελληνικά'], ['hy', 'Հայերեն'], ['iw', 'עברית'], ['ur', 'اردو'], ['ar', 'العربية'], ['fa', 'فارسی'], ['ne', 'नेपाली'], ['mr', 'मराठी'], ['hi', 'हिन्दी'], ['as', 'অসমীয়া'], ['bn', 'বাংলা'], ['pa', 'ਪੰਜਾਬੀ'], ['gu', 'ગુજરાતી'], ['or', 'ଓଡ଼ିଆ'], ['ta', 'தமிழ்'], ['te', 'తెలుగు'], ['kn', 'ಕನ್ನಡ'], ['ml', 'മലയാളം'], ['si', 'සිංහල'], ['th', 'ภาษาไทย'], ['lo', 'ລາວ'], ['my', 'ဗမာ'], ['ka', 'ქართული'], ['am', 'አማርኛ'], ['km', 'ខ្មែរ'], ['zh-CN', '中文 (简体)'], ['zh-TW', '中文 (繁體)'], ['zh-HK', '中文 (香港)'], ['ja', '日本語'], ['ko', '한국어']]  # Ignore PEP8Bear
    _country_list = [['EG', 'Ägypten', 'ar_EG'], ['DZ', 'Algerien', 'ar_DZ'], ['AR', 'Argentinien', 'es_AR'], ['AZ', 'Aserbaidschan', 'az_AZ'], ['AU', 'Australien', 'en_AU'], ['BH', 'Bahrain', 'ar_BH'], ['BD', 'Bangladesch', 'bn_BD'], ['BE', 'Belgien', 'en_BE'], ['BO', 'Bolivien', 'es_BO'], ['BA', 'Bosnien und Herzegowina', 'bs_BA'], ['BR', 'Brasilien', 'pt_BR'], ['BG', 'Bulgarien', 'bg_BG'], ['CL', 'Chile', 'es_CL'], ['CR', 'Costa Rica', 'es_CR'], ['DK', 'Dänemark', 'da_DK'], ['DE', 'Deutschland', 'de_DE'], ['DO', 'Dominikanische Republik', 'es_DO'], ['EC', 'Ecuador', 'es_EC'], ['SV', 'El Salvador', 'es_SV'], ['EE', 'Estland', 'et_EE'], ['FI', 'Finnland', 'fi_FI'], ['FR', 'Frankreich', 'fr_FR'], ['GE', 'Georgien', 'ka_GE'], ['GH', 'Ghana', 'en_GH'], ['GR', 'Griechenland', 'el_GR'], ['GT', 'Guatemala', 'es_GT'], ['HN', 'Honduras', 'es_HN'], ['HK', 'Hongkong', 'zh_HK'], ['IN', 'Indien', 'en_IN'], ['ID', 'Indonesien', 'id_ID'], ['IQ', 'Irak', 'ar_IQ'], ['IE', 'Irland', 'en_IE'], ['IS', 'Island', 'is_IS'], ['IL', 'Israel', 'en_IL'], ['IT', 'Italien', 'it_IT'], ['JM', 'Jamaika', 'en_JM'], ['JP', 'Japan', 'ja_JP'], ['YE', 'Jemen', 'ar_YE'], ['JO', 'Jordanien', 'ar_JO'], ['CA', 'Kanada', 'en_CA'], ['KZ', 'Kasachstan', 'kk_KZ'], ['QA', 'Katar', 'ar_QA'], ['KE', 'Kenia', 'en_KE'], ['CO', 'Kolumbien', 'es_CO'], ['HR', 'Kroatien', 'hr_HR'], ['KW', 'Kuwait', 'ar_KW'], ['LV', 'Lettland', 'lv_LV'], ['LB', 'Libanon', 'ar_LB'], ['LY', 'Libyen', 'ar_LY'], ['LI', 'Liechtenstein', 'zxx_LI'], ['LT', 'Litauen', 'lt_LT'], ['LU', 'Luxemburg', 'lb_LU'], ['MY', 'Malaysia', 'ms_MY'], ['MT', 'Malta', 'en_MT'], ['MA', 'Marokko', 'ar_MA'], ['MX', 'Mexiko', 'es_MX'], ['ME', 'Montenegro', 'sr_ME'], ['NP', 'Nepal', 'ne_NP'], ['NZ', 'Neuseeland', 'en_NZ'], ['NI', 'Nicaragua', 'es_NI'], ['NL', 'Niederlande', 'nl_NL'], ['NG', 'Nigeria', 'en_NG'], ['MK', 'Nordmazedonien', 'mk_MK'], ['NO', 'Norwegen', 'nb_NO'], ['OM', 'Oman', 'ar_OM'], ['AT', 'Österreich', 'de_AT'], ['PK', 'Pakistan', 'ur_PK'], ['PA', 'Panama', 'es_PA'], ['PG', 'Papua-Neuguinea', 'zxx_PG'], ['PY', 'Paraguay', 'es_PY'], ['PE', 'Peru', 'es_PE'], ['PH', 'Philippinen', 'fil_PH'], ['PL', 'Polen', 'pl_PL'], ['PT', 'Portugal', 'pt_PT'], ['PR', 'Puerto Rico', 'es_PR'], ['RO', 'Rumänien', 'ro_RO'], ['RU', 'Russland', 'ru_RU'], ['SA', 'Saudi-Arabien', 'ar_SA'], ['SE', 'Schweden', 'sv_SE'], ['CH', 'Schweiz', 'de_CH'], ['SN', 'Senegal', 'fr_SN'], ['RS', 'Serbien', 'sr_RS'], ['ZW', 'Simbabwe', 'en_ZW'], ['SG', 'Singapur', 'en_SG'], ['SK', 'Slowakei', 'sk_SK'], ['SI', 'Slowenien', 'sl_SI'], ['ES', 'Spanien', 'es_ES'], ['LK', 'Sri Lanka', 'si_LK'], ['ZA', 'Südafrika', 'en_ZA'], ['KR', 'Südkorea', 'ko_KR'], ['TW', 'Taiwan', 'zh_TW'], ['TZ', 'Tansania', 'sw_TZ'], ['TH', 'Thailand', 'th_TH'], ['CZ', 'Tschechien', 'cs_CZ'], ['TN', 'Tunesien', 'ar_TN'], ['TR', 'Türkei', 'tr_TR'], ['UG', 'Uganda', 'en_UG'], ['UA', 'Ukraine', 'uk_UA'], ['HU', 'Ungarn', 'hu_HU'], ['UY', 'Uruguay', 'es_UY'], ['US', 'USA', 'en_US'], ['VE', 'Venezuela', 'es_VE'], ['AE', 'Vereinigte Arabische Emirate', 'ar_AE'], ['GB', 'Vereinigtes Königreich', 'en_GB'], ['VN', 'Vietnam', 'vi_VN'], ['BY', 'Weißrussland', 'be_BY'], ['CY', 'Zypern', 'zxx_CY']]
