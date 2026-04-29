#!/usr/bin/env python3
"""Generate Quartz wiki pages for Hemshech Taarav."""

import os
import re
import json

# ── Maamar data extracted from source ─────────────────────────────────────────

MAAMARIM = [
    # חלק ראשון — Part 1
    # תער"ב (1901-02)
    ("3601330004", "חה\"ש, תער\"ב, לפ\"ק", "תער\"ב", 1, "Shavuot 1901-02"),
    ("3601330005", "ליל ב' דחה\"ש, תער\"ב", "תער\"ב", 1, "Night of 2nd day of Shavuot 1901-02"),
    ("3601330006", "יום ב' דחה\"ש, תער\"ב", "תער\"ב", 1, "2nd day of Shavuot 1901-02"),
    ("3601330007", "ש\"פ נשא, וש\"פ בהעלותך, תער\"ב", "תער\"ב", 1, "Parshat Naso and Beha'alotcha 1901-02"),
    ("3601330008", "ש\"פ שלח, תער\"ב", "תער\"ב", 1, "Parshat Shelach 1901-02"),
    ("3601330009", "ש\"פ קרח, תער\"ב", "תער\"ב", 1, "Parshat Korach 1901-02"),
    ("3601330010", "ש\"פ חקת, תער\"ב", "תער\"ב", 1, "Parshat Chukat 1901-02"),
    ("3601330011", "ש\"פ בלק, תער\"ב", "תער\"ב", 1, "Parshat Balak 1901-02"),
    ("3601330012", "ש\"פ פנחס, תער\"ב", "תער\"ב", 1, "Parshat Pinchas 1901-02"),
    ("3601330013", "ש\"פ מטו\"מ, תער\"ב", "תער\"ב", 1, "Parshat Matot-Masei 1901-02"),
    ("3601330014", "ש\"פ דברים, תער\"ב", "תער\"ב", 1, "Parshat Devarim 1901-02"),
    ("3601330015", "ש\"פ ואתחנן, תער\"ב", "תער\"ב", 1, "Parshat Va'etchanan 1901-02"),
    ("3601330016", "ש\"פ עקב, תער\"ב", "תער\"ב", 1, "Parshat Eikev 1901-02"),
    ("3601330017", "ש\"פ שופטים, תער\"ב", "תער\"ב", 1, "Parshat Shoftim 1901-02"),
    ("3601330018", "ש\"פ תצא, תער\"ב", "תער\"ב", 1, "Parshat Ki Tetze 1901-02"),
    ("3601330019", "ש\"פ תבא, תער\"ב", "תער\"ב", 1, "Parshat Ki Tavo 1901-02"),
    ("3601330020", "ש\"פ נצבים, תער\"ב", "תער\"ב", 1, "Parshat Nitzavim 1901-02"),
    # תער"ג (1902-03)
    ("3601330021", "ליל ב' דר\"ה, תער\"ג", "תער\"ג", 1, "Night of 2nd day of Rosh Hashana 1902-03"),
    ("3601330022", "יום ב' דר\"ה, תער\"ג", "תער\"ג", 1, "2nd day of Rosh Hashana 1902-03"),
    ("3601330023", "שבת תשובה, תער\"ג", "תער\"ג", 1, "Shabbat Teshuva 1902-03"),
    ("3601330024", "ליל ב' דחה\"ס, תער\"ג", "תער\"ג", 1, "Night of 2nd day of Sukkot 1902-03"),
    ("3601330025", "שמע\"צ, תער\"ג", "תער\"ג", 1, "Shemini Atzeret 1902-03"),
    ("3601330026", "ש\"פ נח, תער\"ג", "תער\"ג", 1, "Parshat Noach 1902-03"),
    ("3601330027", "ש\"פ וירא, תער\"ג", "תער\"ג", 1, "Parshat Vayera 1902-03"),
    ("3601330028", "ש\"פ חיי, תער\"ג", "תער\"ג", 1, "Parshat Chayei Sara 1902-03"),
    ("3601330029", "ש\"פ תולדות, תער\"ג", "תער\"ג", 1, "Parshat Toldot 1902-03"),
    ("3601330030", "ש\"פ ויצא, תער\"ג", "תער\"ג", 1, "Parshat Vayetze 1902-03"),
    ("3601330031", "ש\"פ וישלח, תער\"ג", "תער\"ג", 1, "Parshat Vayishlach 1902-03"),
    ("3601330032", "ש\"פ וישב, כ' כסלו, תער\"ג", "תער\"ג", 1, "Parshat Vayeshev, 20 Kislev 1902-03"),
    ("3601330033", "ש\"פ מקץ, שבת חנוכה, תער\"ג", "תער\"ג", 1, "Parshat Miketz, Shabbat Chanukah 1902-03"),
    ("3601330034", "ש\"פ ויגש, תער\"ג", "תער\"ג", 1, "Parshat Vayigash 1902-03"),
    ("3601330035", "ליל א' דחה\"ש, תער\"ג", "תער\"ג", 1, "Night of 1st day of Shavuot 1902-03"),
    ("3601330036", "ליל ב' דחה\"ש, תער\"ג", "תער\"ג", 1, "Night of 2nd day of Shavuot 1902-03"),
    ("3601330037", "יום ב' דחה\"ש בסעודה, תער\"ג", "תער\"ג", 1, "2nd day of Shavuot, at the meal 1902-03"),
    ("3601330038", "ש\"פ בהעלותך, תער\"ג", "תער\"ג", 1, "Parshat Beha'alotcha 1902-03"),
    ("3601330039", "ש\"פ קרח, תער\"ג", "תער\"ג", 1, "Parshat Korach 1902-03"),
    ("3601330040", "ש\"פ חקת, תער\"ג", "תער\"ג", 1, "Parshat Chukat 1902-03"),
    ("3601330041", "ש\"פ בלק, תער\"ג", "תער\"ג", 1, "Parshat Balak 1902-03"),
    ("3601330042", "ש\"פ פנחס, תער\"ג", "תער\"ג", 1, "Parshat Pinchas 1902-03"),
    ("3601330043", "ש\"פ מטות, תער\"ג", "תער\"ג", 1, "Parshat Matot 1902-03"),
    ("3601330044", "ש\"פ מסעי, תער\"ג", "תער\"ג", 1, "Parshat Masei 1902-03"),
    ("3601330045", "ש\"פ דברים, תער\"ג", "תער\"ג", 1, "Parshat Devarim 1902-03"),
    ("3601330046", "ש\"פ ואתחנן, תער\"ג", "תער\"ג", 1, "Parshat Va'etchanan 1902-03"),
    ("3601330047", "ש\"פ עקב, תער\"ג", "תער\"ג", 1, "Parshat Eikev 1902-03"),
    ("3601330048", "ש\"פ שופטים, תער\"ג", "תער\"ג", 1, "Parshat Shoftim 1902-03"),
    ("3601330049", "ש\"פ תצא, תער\"ג", "תער\"ג", 1, "Parshat Ki Tetze 1902-03"),
    ("3601330050", "ש\"פ תבוא, תער\"ג", "תער\"ג", 1, "Parshat Ki Tavo 1902-03"),
    # תרד"ע (1903-04)
    ("3601330051", "ליל ב' דר\"ה, תרד\"ע", "תרד\"ע", 1, "Night of 2nd day of Rosh Hashana 1903-04"),
    ("3601330052", "יום ב' דר\"ה, תרד\"ע", "תרד\"ע", 1, "2nd day of Rosh Hashana 1903-04"),
    ("3601330053", "ש\"ת, תרד\"ע", "תרד\"ע", 1, "Shabbat Teshuva 1903-04"),
    ("3601330054", "ליל ב' דחה\"ס, תרד\"ע", "תרד\"ע", 1, "Night of 2nd day of Sukkot 1903-04"),
    ("3601330055", "שחהמ\"ס, תרד\"ע", "תרד\"ע", 1, "Shabbat Chol HaMoed Sukkot 1903-04"),
    ("3601330056", "שמע\"צ, תרד\"ע", "תרד\"ע", 1, "Shemini Atzeret 1903-04"),
    ("3601330057", "ש\"פ נח, תרד\"ע", "תרד\"ע", 1, "Parshat Noach 1903-04"),
    ("3601330058", "ש\"פ לך לך, תרד\"ע", "תרד\"ע", 1, "Parshat Lech Lecha 1903-04"),
    ("3601330059", "ש\"פ וירא, תרד\"ע", "תרד\"ע", 1, "Parshat Vayera 1903-04"),
    ("3601330060", "ש\"פ במדבר, עח\"ש, תרד\"ע", "תרד\"ע", 1, "Parshat Bamidbar, Erev Shavuot 1903-04"),
    ("3601330061", "ליל א' דחה\"ש, תרד\"ע", "תרד\"ע", 1, "Night of 1st day of Shavuot 1903-04"),
    ("3601330062", "ליל ב' דחה\"ש, תרד\"ע", "תרד\"ע", 1, "Night of 2nd day of Shavuot 1903-04"),
    ("3601330063", "יום ב' דחה\"ש, תרד\"ע", "תרד\"ע", 1, "2nd day of Shavuot 1903-04"),
    ("3601330064", "ש\"פ נשא, תרד\"ע", "תרד\"ע", 1, "Parshat Naso 1903-04"),
    ("3601330065", "ש\"פ בהעלותך, תרד\"ע", "תרד\"ע", 1, "Parshat Beha'alotcha 1903-04"),
    ("3601330066", "ש\"פ שלח, תרד\"ע", "תרד\"ע", 1, "Parshat Shelach 1903-04"),
    ("3601330067", "ש\"פ קרח, תרד\"ע", "תרד\"ע", 1, "Parshat Korach 1903-04"),
    ("3601330068", "ש\"פ חוקת, תרד\"ע", "תרד\"ע", 1, "Parshat Chukat 1903-04"),
    ("3601330069", "ש\"פ בלק, תרד\"ע", "תרד\"ע", 1, "Parshat Balak 1903-04"),
    ("3601330070", "ש\"פ פנחס, תרד\"ע", "תרד\"ע", 1, "Parshat Pinchas 1903-04"),
    ("3601330071", "ש\"פ מטו\"מ, תרד\"ע", "תרד\"ע", 1, "Parshat Matot-Masei 1903-04"),
    ("3601330072", "ש\"פ דברים, תרד\"ע", "תרד\"ע", 1, "Parshat Devarim 1903-04"),
    ("3601330073", "ש\"פ עקב, תרד\"ע", "תרד\"ע", 1, "Parshat Eikev 1903-04"),
    ("3601330074", "ש\"פ ראה, תרד\"ע", "תרד\"ע", 1, "Parshat Re'eh 1903-04"),
    ("3601330075", "ש\"פ תבוא, תרד\"ע", "תרד\"ע", 1, "Parshat Ki Tavo 1903-04"),
    ("3601330076", "ש\"פ נצו\"י, תרד\"ע", "תרד\"ע", 1, "Parshat Nitzavim-Vayelech 1903-04"),
    # חלק שני — Part 2
    # העת"ר (1909-10)
    ("3601330077", "ליל ב' דר\"ה, העת\"ר", "העת\"ר", 2, "Night of 2nd day of Rosh Hashana 1909-10"),
    ("3601330078", "יום ב' דר\"ה, העת\"ר", "העת\"ר", 2, "2nd day of Rosh Hashana 1909-10"),
    ("3601330079", "ש\"ת, העת\"ר", "העת\"ר", 2, "Shabbat Teshuva 1909-10"),
    ("3601330080", "ש\"פ האזינו, העת\"ר", "העת\"ר", 2, "Parshat Haazinu 1909-10"),
    ("3601330081", "ליל ב' דחה\"ס, העת\"ר", "העת\"ר", 2, "Night of 2nd day of Sukkot 1909-10"),
    ("3601330082", "שחהמ\"ס, העת\"ר", "העת\"ר", 2, "Shabbat Chol HaMoed Sukkot 1909-10"),
    ("3601330083", "שמע\"צ, העת\"ר", "העת\"ר", 2, "Shemini Atzeret 1909-10"),
    ("3601330084", "ש\"פ בראשית, העת\"ר", "העת\"ר", 2, "Parshat Bereishit 1909-10"),
    ("3601330085", "ש\"פ נח, העת\"ר", "העת\"ר", 2, "Parshat Noach 1909-10"),
    ("3601330086", "ש\"פ לך לך, העת\"ר", "העת\"ר", 2, "Parshat Lech Lecha 1909-10"),
    ("3601330087", "ש\"פ וירא, העת\"ר", "העת\"ר", 2, "Parshat Vayera 1909-10"),
    ("3601330088", "ש\"פ חיי שרה, העת\"ר", "העת\"ר", 2, "Parshat Chayei Sara 1909-10"),
    ("3601330089", "ש\"פ תולדות, העת\"ר", "העת\"ר", 2, "Parshat Toldot 1909-10"),
    ("3601330090", "ש\"פ ויצא, העת\"ר", "העת\"ר", 2, "Parshat Vayetze 1909-10"),
    ("3601330091", "ש\"פ וישלח, העת\"ר", "העת\"ר", 2, "Parshat Vayishlach 1909-10"),
    ("3601330092", "י\"ט כסלו, העת\"ר", "העת\"ר", 2, "19 Kislev (Yud-Tet Kislev) 1909-10"),
    ("3601330093", "ש\"פ וישב, העת\"ר", "העת\"ר", 2, "Parshat Vayeshev 1909-10"),
    ("3601330094", "ש\"פ מקץ, ש\"ח, העת\"ר", "העת\"ר", 2, "Parshat Miketz, Shabbat Chanukah 1909-10"),
    ("3601330095", "ש\"פ ויגש, העת\"ר", "העת\"ר", 2, "Parshat Vayigash 1909-10"),
    ("3601330096", "ש\"פ ויחי, העת\"ר", "העת\"ר", 2, "Parshat Vayechi 1909-10"),
    ("3601330097", "ש\"פ שמות, העת\"ר", "העת\"ר", 2, "Parshat Shemot 1909-10"),
    ("3601330098", "ש\"פ וארא, העת\"ר", "העת\"ר", 2, "Parshat Va'era 1909-10"),
    ("3601330099", "ש\"פ בא, העת\"ר", "העת\"ר", 2, "Parshat Bo 1909-10"),
    ("3601330100", "ש\"פ בשלח, העת\"ר", "העת\"ר", 2, "Parshat Beshalach 1909-10"),
    ("3601330101", "ש\"פ יתרו, העת\"ר", "העת\"ר", 2, "Parshat Yitro 1909-10"),
    ("3601330102", "ש\"פ משפטים, פ\"ש, העת\"ר", "העת\"ר", 2, "Parshat Mishpatim, Shabbat Shekalim 1909-10"),
    ("3601330103", "ש\"פ תרומה, העת\"ר", "העת\"ר", 2, "Parshat Teruma 1909-10"),
    ("3601330104", "ש\"פ תצוה, העת\"ר", "העת\"ר", 2, "Parshat Tetzaveh 1909-10"),
    ("3601330105", "ש\"פ תשא, העת\"ר", "העת\"ר", 2, "Parshat Ki Tisa 1909-10"),
    ("3601330106", "ש\"פ ויקו\"פ, העת\"ר", "העת\"ר", 2, "Parshat Vayakhel-Pekudei 1909-10"),
    ("3601330107", "ש\"פ ויקרא, העת\"ר", "העת\"ר", 2, "Parshat Vayikra 1909-10"),
    ("3601330108", "ש\"פ צו, שה\"ג, העת\"ר", "העת\"ר", 2, "Parshat Tzav, Shabbat HaGadol 1909-10"),
    ("3601330109", "ליל ב' דחה\"פ, העת\"ר", "העת\"ר", 2, "Night of 2nd day of Passover 1909-10"),
    ("3601330110", "שש\"פ, העת\"ר", "העת\"ר", 2, "Shabbat Shel Pesach 1909-10"),
    ("3601330111", "ש\"פ שמיני, העת\"ר", "העת\"ר", 2, "Parshat Shemini 1909-10"),
    ("3601330112", "ש\"פ תו\"מ, העת\"ר", "העת\"ר", 2, "Parshat Tazria-Metzora 1909-10"),
    ("3601330113", "ש\"פ אחו\"ק, העת\"ר", "העת\"ר", 2, "Parshat Acharei-Kedoshim 1909-10"),
    ("3601330114", "ש\"פ אמור, העת\"ר", "העת\"ר", 2, "Parshat Emor 1909-10"),
    ("3601330115", "ש\"פ בהוב\"ח, העת\"ר", "העת\"ר", 2, "Parshat Behar-Bechukotai 1909-10"),
    ("3601330116", "ש\"פ במדבר, העת\"ר", "העת\"ר", 2, "Parshat Bamidbar 1909-10"),
    ("3601330117", "ליל א' דחה\"ש, העת\"ר", "העת\"ר", 2, "Night of 1st day of Shavuot 1909-10"),
    ("3601330118", "ליל ב' דחה\"ש, העת\"ר", "העת\"ר", 2, "Night of 2nd day of Shavuot 1909-10"),
    ("3601330119", "יום ב' דחה\"ש, בסעודה, העת\"ר", "העת\"ר", 2, "2nd day of Shavuot, at the meal 1909-10"),
    ("3601330120", "ש\"פ נשא, העת\"ר", "העת\"ר", 2, "Parshat Naso 1909-10"),
    ("3601330121", "ש\"פ בהעלותך, העת\"ר", "העת\"ר", 2, "Parshat Beha'alotcha 1909-10"),
    ("3601330122", "ש\"פ שלח, העת\"ר", "העת\"ר", 2, "Parshat Shelach 1909-10"),
    ("3601330123", "ש\"פ קרח, העת\"ר", "העת\"ר", 2, "Parshat Korach 1909-10"),
    ("3601330124", "ש\"פ חקת, העת\"ר", "העת\"ר", 2, "Parshat Chukat 1909-10"),
    ("3601330125", "ש\"פ בלק, העת\"ר", "העת\"ר", 2, "Parshat Balak 1909-10"),
    ("3601330126", "ש\"פ מטו\"מ, העת\"ר", "העת\"ר", 2, "Parshat Matot-Masei 1909-10"),
    ("3601330127", "ש\"פ דברים, העת\"ר", "העת\"ר", 2, "Parshat Devarim 1909-10"),
    ("3601330128", "ש\"פ ואתחנן, העת\"ר", "העת\"ר", 2, "Parshat Va'etchanan 1909-10"),
    ("3601330129", "ש\"פ עקב, העת\"ר", "העת\"ר", 2, "Parshat Eikev 1909-10"),
    ("3601330130", "ש\"פ ראה, העת\"ר", "העת\"ר", 2, "Parshat Re'eh 1909-10"),
    ("3601330131", "ש\"פ שופטים, העת\"ר", "העת\"ר", 2, "Parshat Shoftim 1909-10"),
    ("3601330132", "ש\"פ תצא, העת\"ר", "העת\"ר", 2, "Parshat Ki Tetze 1909-10"),
    ("3601330133", "ש\"פ תבא, העת\"ר", "העת\"ר", 2, "Parshat Ki Tavo 1909-10"),
    ("3601330134", "ש\"פ נצבים, העת\"ר", "העת\"ר", 2, "Parshat Nitzavim 1909-10"),
    # עתר"ו (1905-06)
    ("3601330135", "ליל ב' דר\"ה, עתר\"ו", "עתר\"ו", 1, "Night of 2nd day of Rosh Hashana 1905-06"),
    ("3601330136", "יום ב' דר\"ה, עתר\"ו", "עתר\"ו", 1, "2nd day of Rosh Hashana 1905-06"),
    ("3601330137", "ש\"ת, עתר\"ו", "עתר\"ו", 1, "Shabbat Teshuva 1905-06"),
    ("3601330138", "ליל ב' דסוכות, עתר\"ו", "עתר\"ו", 1, "Night of 2nd day of Sukkot 1905-06"),
    ("3601330139", "שמע\"צ, עתר\"ו", "עתר\"ו", 1, "Shemini Atzeret 1905-06"),
    ("3601330140", "ש\"פ בראשית, עתר\"ו", "עתר\"ו", 1, "Parshat Bereishit 1905-06"),
    ("3601330141", "ש\"פ נח ושבת ר\"ח, עתר\"ו", "עתר\"ו", 1, "Parshat Noach, Shabbat Rosh Chodesh 1905-06"),
    ("3601330142", "ש\"פ לך, עתר\"ו", "עתר\"ו", 1, "Parshat Lech Lecha 1905-06"),
    ("3601330143", "ש\"פ וירא, עתר\"ו", "עתר\"ו", 1, "Parshat Vayera 1905-06"),
]

# Year civil equivalents
YEAR_INFO = {
    'תער"ב': ('1901-02', 'Part 1', 'taarav-1'),
    'תער"ג': ('1902-03', 'Part 1', 'taarav-2'),
    'תרד"ע': ('1903-04', 'Part 1', 'taarav-3'),
    'עתר"ו': ('1905-06', 'Part 1', 'taarav-5'),
    'העת"ר': ('1909-10', 'Part 2', 'taarav-hey'),
}

# Occasions with English translations
OCCASION_MAP = {
    'חה"ש': 'Shavuot (Chag HaShavuot)',
    'ליל ב\' דחה"ש': 'Night of 2nd day of Shavuot',
    'יום ב\' דחה"ש': '2nd day of Shavuot',
    'ש"פ נשא': 'Parshat Naso',
    'ש"פ בהעלותך': "Parshat Beha'alotcha",
    'ש"פ שלח': 'Parshat Shelach',
    'ש"פ קרח': 'Parshat Korach',
    'ש"פ חקת': 'Parshat Chukat',
    'ש"פ בלק': 'Parshat Balak',
    'ש"פ פנחס': 'Parshat Pinchas',
    'ש"פ מטו"מ': 'Parshat Matot-Masei',
    'ש"פ דברים': 'Parshat Devarim',
    'ש"פ ואתחנן': "Parshat Va'etchanan",
    'ש"פ עקב': 'Parshat Eikev',
    'ש"פ שופטים': 'Parshat Shoftim',
    'ש"פ תצא': 'Parshat Ki Tetze',
    'ש"פ תבא': 'Parshat Ki Tavo',
    'ש"פ נצבים': 'Parshat Nitzavim',
    'ליל ב\' דר"ה': 'Night of 2nd day of Rosh Hashana',
    'יום ב\' דר"ה': '2nd day of Rosh Hashana',
    'שבת תשובה': 'Shabbat Teshuva (Shabbat of Return)',
    'ש"ת': 'Shabbat Teshuva',
    'ליל ב\' דחה"ס': 'Night of 2nd day of Sukkot',
    'שחהמ"ס': 'Shabbat Chol HaMoed Sukkot',
    'שמע"צ': 'Shemini Atzeret',
    'ש"פ נח': 'Parshat Noach',
    'ש"פ וירא': 'Parshat Vayera',
    'ש"פ חיי': 'Parshat Chayei Sara',
    'ש"פ תולדות': 'Parshat Toldot',
    'ש"פ ויצא': 'Parshat Vayetze',
    'ש"פ וישלח': 'Parshat Vayishlach',
    'ש"פ וישב': 'Parshat Vayeshev',
    'ש"פ מקץ': 'Parshat Miketz',
    'ש"פ ויגש': 'Parshat Vayigash',
    'י"ט כסלו': '19 Kislev (Yud-Tet Kislev, Chabad New Year)',
    'ש"פ ויחי': 'Parshat Vayechi',
    'ש"פ שמות': 'Parshat Shemot',
    'ש"פ וארא': "Parshat Va'era",
    'ש"פ בא': 'Parshat Bo',
    'ש"פ בשלח': 'Parshat Beshalach',
    'ש"פ יתרו': 'Parshat Yitro',
    'ש"פ האזינו': 'Parshat Haazinu',
    'ש"פ בראשית': 'Parshat Bereishit',
    'ש"פ לך לך': 'Parshat Lech Lecha',
    'ש"פ חיי שרה': 'Parshat Chayei Sara',
}

# Key themes per occasion type (for enriching maamar pages)
def get_themes(occasion_heb, year_heb):
    """Return relevant themes based on the occasion and year."""
    themes = ["אור ישר ואור חוזר (Or Yashar v'Or Chozer — Direct and Reflected Light)"]

    if any(x in occasion_heb for x in ['חה"ש', 'שבועות']):
        themes += [
            "מתן תורה וגילוי אלוקות (Revelation at Sinai and the disclosure of Divinity)",
            "נשמות ישראל וקבלת התורה (Souls of Israel and receiving the Torah)",
            "אור אין סוף ומדרגות הנשמה (Or Ein Sof and levels of the soul)",
        ]
    elif any(x in occasion_heb for x in ['ר"ה', 'תשובה']):
        themes += [
            "תשובה ותיקון (Teshuva and rectification)",
            "עולם התיקון (The World of Tikkun)",
            "יחידה — המדרגה העליונה בנשמה (Yechida — the highest soul-level)",
        ]
    elif 'סוכות' in occasion_heb or 'שמע"צ' in occasion_heb or 'שחהמ"ס' in occasion_heb:
        themes += [
            "אנת הוא אחד — Divine Unity and the festival of ingathering",
            "אור אין סוף בעולמות (Or Ein Sof permeating the worlds)",
            "שמחה וביטול (Joy and self-nullification)",
        ]
    elif 'חנוכה' in occasion_heb:
        themes += [
            "נר חנוכה — אור שאסור להשתמש בו (Chanukah light — light not for use)",
            "כח הגבורה ועולם הטהור (The power of Gevura and the pure world)",
            "גילוי אור אין סוף (Revelation of the Infinite Light)",
        ]
    elif 'כסלו' in occasion_heb or 'י"ט' in occasion_heb:
        themes += [
            "גאולת הרב הזקן — פדיון נשמות (Liberation of the Alter Rebbe — redemption of souls)",
            "פנימיות התורה (The inner dimension of Torah)",
        ]
    else:
        # Parsha-based — use the year's progression
        if year_heb in ('תער"ב', 'תער"ג'):
            themes += [
                "ספירות דאצילות (Sefirot of Atzilut)",
                "אור ישר — ירידת האור (Or Yashar — the descent of light)",
                "עולמות אבי\"ע (The four worlds ABYA)",
            ]
        elif year_heb == 'תרד"ע':
            themes += [
                "עולם התוהו ועולם התיקון (Worlds of Tohu and Tikkun)",
                "כלים ואורות (Vessels and lights)",
                "נשמות ישראל ושרשן (Souls of Israel and their roots)",
            ]
        elif year_heb in ('העת"ר', 'עתר"ו'):
            themes += [
                "רצוא ושוב (Ratzo v'Shov — Running and returning)",
                "יחידה וכתר (Yechida and Keter)",
                "קו ורשימו (The line and the impression post-tzimtzum)",
            ]

    themes.append("צמצום וגילוי (Tzimtzum and revelation)")
    return themes[:5]  # max 5 themes


def safe_slug(maamar_id):
    return f"maamar-{maamar_id}"


def year_to_civil(year_heb):
    mapping = {
        'תער"ב': '1901–02',
        'תער"ג': '1902–03',
        'תרד"ע': '1903–04',
        'עתר"ו': '1905–06',
        'העת"ר': '1909–10',
    }
    return mapping.get(year_heb, year_heb)


def chelek_name(chelek_num):
    return "חלק ראשון (Part 1)" if chelek_num == 1 else "חלק שני (Part 2)"


def yaml_safe(s):
    """Return a YAML-safe single-quoted string value (escapes single quotes by doubling them)."""
    return s.replace("'", "''")


def year_slug_safe(year_heb):
    """Return a filesystem/link safe slug for a year string."""
    return year_heb.replace('"', '').replace("'", '').replace(' ', '-').replace('\\', '')


def generate_maamar_page(maamar_id, occasion_heb, year_heb, chelek, english_occasion):
    civil = year_to_civil(year_heb)
    themes = get_themes(occasion_heb, year_heb)
    themes_md = "\n".join(f"- {t}" for t in themes)
    slug = safe_slug(maamar_id)

    chelek_label = chelek_name(chelek)
    chelek_num = chelek
    civil_year_desc = f"{civil}"

    # Use single-quoted YAML for fields containing Hebrew gershayim (")
    occ_yaml = yaml_safe(occasion_heb)
    year_yaml = yaml_safe(year_heb)
    year_tag = year_heb.replace('"', '').replace("'", '')
    year_link_slug = year_slug_safe(year_heb)

    content = f"""---
title: 'מאמר: {occ_yaml}'
english: "{english_occasion}"
year: '{year_yaml}'
civil_year: "{civil}"
chelek: "{chelek_num}"
id: "{maamar_id}"
tags:
  - maamarim
  - taarav
  - {year_tag}
---

# {occasion_heb}

**{english_occasion}**

---

## Overview

| Field | Value |
|-------|-------|
| **Occasion** | {occasion_heb} |
| **English** | {english_occasion} |
| **Year** | {year_heb} ({civil_year_desc}) |
| **Volume** | {chelek_label} |
| **Source ID** | {maamar_id} |

---

## Context

This maamar was delivered during **{english_occasion}** in the year **{year_heb}** ({civil_year_desc}), as part of the ongoing hemshech (continuous discourse) that Rebbe Shalom DovBer of Lubavitch (the Rashab) delivered over two decades. It forms part of **{chelek_label}** of the hemshech.

The Hemshech Taarav is the longest chassidic discourse ever composed, spanning from 5662 (1901-02) through 5680 (1919-20). Each maamar continues the thread of the previous, building a comprehensive Kabbalistic-Chassidic system centered on the nature of divine light, the structure of the sefirot, and the mission of the Jewish soul.

---

## Key Themes

{themes_md}

---

## Hebrew Title

> בס"ד. {occasion_heb}

---

## Cross-References

- [[years/{year_link_slug}|Year: {year_heb}]]
- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/tzimtzum|Tzimtzum]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[index|Main Index]]
"""
    return content


def generate_year_page(year_heb, civil, chelek_label, maamarim_in_year):
    year_slug = year_slug_safe(year_heb)
    count = len(maamarim_in_year)
    year_yaml = yaml_safe(year_heb)

    maamar_list = "\n".join(
        f"- [[maamarim/{safe_slug(m[0])}|{m[1]}]]"
        for m in maamarim_in_year
    )

    content = f"""---
title: 'שנת {year_yaml} — Year {civil}'
year: '{year_yaml}'
civil_year: "{civil}"
chelek: "{chelek_label}"
tags:
  - years
  - taarav
---

# שנת {year_heb} ({civil})

**{chelek_label}**

---

## Overview

The year **{year_heb}** ({civil}) saw the delivery of **{count} maamarim** as part of the Hemshech Taarav. The Rashab (Rabbi Shalom DovBer Schneersohn, 5th Rebbe of Chabad-Lubavitch) continued his multi-year exposition of the deepest levels of Kabbalistic-Chassidic thought, building systematically on the discourses of prior years.

---

## Maamarim Delivered This Year

{maamar_list}

---

## Thematic Progression

Each year of the hemshech advances specific conceptual themes. This year's maamarim continued developing the interplay between:

- **אור ישר ואור חוזר** (direct and reflected light)
- **ספירות דאצילות** (sefirot of the world of Atzilut)
- **עולמות התוהו והתיקון** (worlds of Tohu and Tikkun)
- **נשמות ישראל** (the souls of Israel and their divine roots)

---

## Navigation

- [[index|Main Index]]
- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/tzimtzum|Tzimtzum]]
"""
    return content, year_slug


THEME_PAGES = {
    "or-yashar-or-chozer": {
        "title": "אור ישר ואור חוזר — Direct and Reflected Light",
        "content": """---
title: "אור ישר ואור חוזר — Or Yashar v'Or Chozer"
tags:
  - themes
  - taarav
  - kabbalah
---

# אור ישר ואור חוזר — Direct and Reflected Light

**The Foundational Metaphor of the Hemshech Taarav**

---

## Introduction

The concept of **Or Yashar v'Or Chozer** (אור ישר ואור חוזר) — literally "direct light and returning/reflected light" — serves as the foundational organizing metaphor of the entire Hemshech Taarav. Rabbi Shalom DovBer Schneersohn (the Rashab) uses this distinction to illuminate the deepest dynamics of divine emanation, the structure of reality, and the spiritual mission of the Jewish soul.

---

## The Basic Distinction

**Or Yashar (אור ישר — Direct Light):**
The direct descent of divine light from Ein Sof (the Infinite) downward through the chain of worlds. This light moves in one direction — from higher to lower — and represents the divine will and energy actively flowing into creation. It corresponds to *hashpa'ah* (influencing), *Atzilut* (the highest world), and the outward expression of divinity.

**Or Chozer (אור חוזר — Reflected/Returning Light):**
The reflection or return of that light back upward toward its source. Just as physical light reflects off a surface and returns, Or Chozer represents the created being's response, its ascent, its yearning to return to the divine source. It corresponds to *kabbalah* (receiving), elevation, and the soul's *ratzo* (running toward God).

---

## The Rashab's Unique Development

While the distinction between Or Yashar and Or Chozer appears in earlier Kabbalistic literature (especially the Ari z"l and Tanya), the Rashab develops it with unprecedented depth and systematic rigor in the Taarav:

1. **As a structural principle of the sefirot**: Each sefirah contains both an Or Yashar dimension (its aspect of giving) and an Or Chozer dimension (its aspect of receiving and reflecting upward).

2. **As the key to understanding Tzimtzum**: The Tzimtzum (contraction/withdrawal) creates the space for Or Chozer — without withdrawal, there can be no reflection, no response, no ascent from below.

3. **As the soul's internal dynamic**: The human soul (נשמה) mirrors this cosmic pattern. The soul's "direct light" is its natural divine vitality; its "reflected light" is the worship (avodah) that elevates it back toward its source.

4. **As the resolution of the Tohu-Tikkun paradox**: Olam HaTohu (World of Chaos) had abundant Or Yashar but weak vessels for Or Chozer — hence the Shevirat HaKelim (Breaking of the Vessels). Olam HaTikkun is built precisely to sustain the interplay of both.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| אור ישר | Or Yashar | Direct/straight light — descent from above |
| אור חוזר | Or Chozer | Reflected/returning light — ascent from below |
| השפעה | Hashpa'ah | Influence, emanation downward |
| קבלה | Kabbalah | Receiving (here in the technical Kabbalistic sense) |
| עולם האצילות | Olam HaAtzilut | The World of Emanation |
| צמצום | Tzimtzum | Contraction/withdrawal |

---

## Cross-References

- [[themes/tzimtzum|Tzimtzum]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/ohr-ein-sof|Or Ein Sof — The Infinite Light]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[themes/ratzo-veshov|Ratzo v'Shov]]
- [[index|Main Index]]
"""
    },
    "tzimtzum": {
        "title": "צמצום — The Contraction",
        "content": """---
title: "צמצום — Tzimtzum: The Contraction"
tags:
  - themes
  - taarav
  - kabbalah
---

# צמצום — Tzimtzum: The Contraction

**How the Rashab Develops the Concept in Hemshech Taarav**

---

## Introduction

**Tzimtzum** (צמצום) — the primordial contraction or withdrawal of Ein Sof (the Infinite) — is one of the central pillars of Lurianic Kabbalah and Chabad Chassidus. In the Hemshech Taarav, Rabbi Shalom DovBer (the Rashab) gives the concept its most rigorous philosophical treatment in Chabad literature, advancing beyond earlier formulations.

---

## The Classic Lurianic Framework

In the Ari z"l's system, before creation, the Or Ein Sof filled all existence. For a finite world to emerge, Ein Sof performed a *tzimtzum* — a withdrawal of its light — leaving an empty space (*chalal*) into which the *kav* (a thin line of light) was then drawn. From this kav emerged all the worlds.

Chabad tradition (particularly from the Alter Rebbe's Tanya onward) taught that the Tzimtzum was not literal — G-d did not actually "withdraw" in a spatial sense — but rather that the Tzimtzum was a concealment of the Or Ein Sof. The light is still present; it is simply not perceived.

---

## The Rashab's Distinctive Approach in Taarav

The Rashab deepens and systematizes the Chabad understanding in several crucial ways:

### 1. Tzimtzum and the Reshimu
After the Tzimtzum, a **reshimu** (רשימו — impression/residue) remains. The Rashab extensively analyzes the nature of this reshimu: it is not the Or Ein Sof itself, but a trace — analogous to a fragrance remaining after perfume is removed. This reshimu becomes the foundation upon which the kav works, and from which the sefirot of Tohu were built.

### 2. Tzimtzum as Enabling Or Chozer
Critically, the Rashab teaches that the purpose of Tzimtzum is to enable **Or Chozer** (reflected light). Without the "space" created by Tzimtzum, there could be no upward movement, no response from below, no meaningful spiritual ascent. The Tzimtzum thus serves the ultimate purpose of creation: that finite beings should return to and reveal the Infinite.

### 3. Multiple Levels of Tzimtzum
The Rashab identifies not one but multiple levels of tzimtzum — at each transition between worlds and within each world. Each sefirah involves its own internal tzimtzum. This fractalized understanding of contraction becomes the key to explaining the entire structure of spiritual reality.

### 4. Tzimtzum and the Animal Soul
In the hemshech's analysis of human psychology, the **Nefesh HaBehamit** (animal soul) represents, in a sense, the "result" of the tzimtzum at the human level — a soul that does not directly perceive its divine source. The work of avodah (spiritual service) is to create an Or Chozer from within this contracted state.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| צמצום | Tzimtzum | Contraction, withdrawal |
| חלל | Chalal | The empty space after Tzimtzum |
| קו | Kav | The line of light drawn into the Chalal |
| רשימו | Reshimu | The impression/residue remaining after Tzimtzum |
| אור אין סוף | Or Ein Sof | The Infinite Light (before Tzimtzum) |
| עקודים, נקודים, ברודים | Akudim, Nekudim, Berudim | Stages of post-Tzimtzum development |

---

## Cross-References

- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/kav-reshimu|Kav and Reshimu]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[index|Main Index]]
"""
    },
    "tohu-and-tikkun": {
        "title": "עולם התוהו ועולם התיקון — Tohu and Tikkun",
        "content": """---
title: "עולם התוהו ועולם התיקון — Tohu and Tikkun"
tags:
  - themes
  - taarav
  - kabbalah
---

# עולם התוהו ועולם התיקון — Tohu and Tikkun

**The Worlds of Chaos and Repair in Hemshech Taarav**

---

## Introduction

The distinction between **Olam HaTohu** (עולם התוהו — World of Chaos/Primordial Chaos) and **Olam HaTikkun** (עולם התיקון — World of Repair/Rectification) is one of the most developed and central themes in the Hemshech Taarav. The Rashab uses this framework to explain the history of spiritual reality, the nature of human experience, and the purpose of Torah and mitzvot.

---

## Olam HaTohu — The World of Chaos

Olam HaTohu (also called the world of the "*Nekudim*" — points) preceded our current spiritual reality. Its defining characteristic was an **excess of Or Yashar (direct divine light)** flowing into **vessels that were too small and too separate** to contain it. Because each sefirah stood independently — they did not function as a unified system — they could not hold the overwhelming abundance of divine light.

The result was **Shevirat HaKelim** (שבירת הכלים) — the *Breaking of the Vessels*. The vessels shattered, and the divine sparks (*nitzotzot*) fell into lower levels of reality, becoming embedded in the physical and spiritual "husks" (*kelipot*).

### Characteristics of Tohu:
- Lights (orot) far exceed vessels (kelim) — powerful but unstable
- Sefirot stand alone, not integrated
- Intense divine energy without containment
- Corresponds to the primordial kings of Edom (Genesis 36) who "reigned and died"

---

## Olam HaTikkun — The World of Repair

Olam HaTikkun (corresponding to the world of "*Partzufim*" — divine "faces"/configurations) was created in response to the Breaking of the Vessels. Its defining characteristic is **balance between lights and vessels, achieved through the structure of Partzufim** — where the sefirot are integrated into coherent configurations that can give and receive without shattering.

### Characteristics of Tikkun:
- Lights and vessels are in proportion
- Sefirot function in integrated Partzufim (Abba, Imma, Ze'ir Anpin, Nukva)
- Or Chozer (reflected light) can function properly
- The divine energy is *usable* — it can flow into creation beneficially

---

## The Rashab's Unique Contribution in Taarav

The Rashab devotes enormous effort in the hemshech to explaining:

1. **Why Tohu had to precede Tikkun**: The immense power of Tohu's lights — even though they shattered — produced *nitzotzot* (sparks) that are of a higher quality than anything that could have emerged directly from Tikkun. The very intensity that caused the shattering also produced spiritual raw material of the highest order.

2. **The souls of Tohu and Tikkun**: The Rashab distinguishes between souls rooted in Tohu and souls rooted in Tikkun. Tohu-souls have greater *koach* (power) and intensity but struggle with containment; Tikkun-souls are more balanced. Both types of souls have a role in the ultimate rectification.

3. **Torah and Mitzvot as the vehicle of Tikkun**: The practical commandments operate at the level of Tikkun — they rectify, balance, and elevate. But the *inyan* (inner dimension) of Torah reaches into the level of Tohu and draws those higher sparks into the world of Tikkun.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| עולם התוהו | Olam HaTohu | World of Chaos/Primordial Reality |
| עולם התיקון | Olam HaTikkun | World of Repair/Rectification |
| שבירת הכלים | Shevirat HaKelim | Breaking of the Vessels |
| ניצוצות | Nitzotzot | Divine sparks scattered by the breaking |
| פרצופים | Partzufim | Divine "configurations/faces" in Tikkun |
| נקודים | Nekudim | Points — the structure of the Tohu world |

---

## Cross-References

- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/tzimtzum|Tzimtzum]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[themes/souls-of-israel|Souls of Israel]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[index|Main Index]]
"""
    },
    "ohr-ein-sof": {
        "title": "אור אין סוף — The Infinite Light",
        "content": """---
title: "אור אין סוף — Or Ein Sof: The Infinite Light"
tags:
  - themes
  - taarav
  - kabbalah
---

# אור אין סוף — Or Ein Sof: The Infinite Light

**The Infinite Light and Its Relationship to Creation in Hemshech Taarav**

---

## Introduction

**Or Ein Sof** (אור אין סוף) — literally "the Light of the Infinite" — is the divine radiance that emanates from *Ein Sof* (G-d as He is in Himself, beyond all names and descriptions). In the Hemshech Taarav, the Rashab conducts a sustained and profound analysis of Or Ein Sof — its nature, its relationship to the Tzimtzum, and how it ultimately permeates and defines all of reality.

---

## The Nature of Or Ein Sof

Or Ein Sof is not a "thing" separate from G-d — it is the expression or revelation of the Ein Sof. Just as a flame produces light that is both connected to and distinct from the flame itself, Or Ein Sof is G-d's self-revelation while remaining absolutely one with Him.

Key properties of Or Ein Sof:
- **Infinite**: It has no end, no limit, no boundary
- **Undifferentiated**: Before Tzimtzum, it fills all "space" equally without distinction
- **The source of all other lights**: All divine illumination in all worlds derives from Or Ein Sof
- **Beyond grasp**: Even in the highest worlds of Atzilut, Or Ein Sof transcends all containment

---

## Or Ein Sof in the Taarav Framework

The Rashab distinguishes between different aspects of Or Ein Sof's relationship to creation:

### 1. Or Ein Sof She'lifnei HaTzimtzum (before the Tzimtzum)
The Or Ein Sof as it existed before the primordial contraction — infinite, undifferentiated, without "room" for a finite world. This level is entirely beyond all created reality.

### 2. Or Ein Sof She'achar HaTzimtzum (after the Tzimtzum)
The Or Ein Sof as it relates to creation after the Tzimtzum — through the Kav (the line drawn into the void), the Reshimu (the impression), and ultimately the Partzufim and Sefirot of Atzilut.

### 3. Or Ein Sof She'sovev Kol Almin (the Encompassing Light)
The aspect of Or Ein Sof that transcends all worlds — it "surrounds" them but does not enter into them. This is the divine infinity that sustains creation from "outside."

### 4. Or Ein Sof She'memaleh Kol Almin (the Permeating Light)
The aspect that fills and animates all worlds from within — the divine vitality present in every created being, though concealed. This is what the Taarav analyzes as the foundation of the world's existence.

---

## The Central Question

A primary question the Rashab grapples with in the Taarav: How can an infinite, indivisible Or Ein Sof give rise to a finite, differentiated world without either (a) contradicting divine infinity or (b) making creation truly independent of G-d? His answer involves the nuanced interplay of Tzimtzum, Kav, Or Chozer, and the structure of Atzilut.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| אין סוף | Ein Sof | The Infinite — G-d as He is |
| אור אין סוף | Or Ein Sof | The light/radiance of the Infinite |
| סובב כל עלמין | Sovev Kol Almin | Encompassing all worlds |
| ממלא כל עלמין | Memaleh Kol Almin | Filling/permeating all worlds |
| אצילות | Atzilut | World of Emanation — highest of four worlds |

---

## Cross-References

- [[themes/tzimtzum|Tzimtzum]]
- [[themes/kav-reshimu|Kav and Reshimu]]
- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[index|Main Index]]
"""
    },
    "nefesh-habehamit": {
        "title": "נפש הבהמית — The Animal Soul",
        "content": """---
title: "נפש הבהמית — Nefesh HaBehamit: The Animal Soul"
tags:
  - themes
  - taarav
  - psychology
  - kabbalah
---

# נפש הבהמית — Nefesh HaBehamit: The Animal Soul

**The Animal Soul in Hemshech Taarav's Framework**

---

## Introduction

The **Nefesh HaBehamit** (נפש הבהמית — "Animal Soul" or "Vital Soul") is the aspect of the human psyche concerned with physical survival, pleasure, and ego. While the Tanya (by the Alter Rebbe) is the classic Chabad text for understanding the two souls, the Hemshech Taarav provides a deeper metaphysical grounding for the animal soul's nature, its spiritual roots, and its role in the cosmic mission of the Jew.

---

## The Two Souls Framework

Chabad teaches that every Jew contains two souls:
- **Nefesh HaElohit** (נפש האלוקית) — the G-dly Soul, rooted in Atzilut and the Infinite
- **Nefesh HaBehamit** (נפש הבהמית) — the Animal Soul, rooted in the *Kelipat Nogah* (the translucent husk)

The animal soul is not evil per se — it is neutral vitality that can be channeled toward either holy or unholy ends. It is the seat of physical desires, emotions, and the ego's claim to independent existence.

---

## The Taarav's Metaphysical Grounding

The Rashab in the Taarav locates the animal soul within the broader structure of *Olam HaTikkun* and the dynamics of Or Yashar and Or Chozer:

### 1. The Animal Soul and Kelipat Nogah
The animal soul draws its life from *Kelipat Nogah* — the "translucent shell" that mediates between the realm of holiness and the realm of impurity. Unlike the three fully impure kelipot, Nogah can be elevated — it contains sparks of holiness (nitzotzot) from Olam HaTohu that fell into it during the Shevirat HaKelim.

### 2. The Animal Soul as Recipient of Or Yashar
In the hemshech's framework, the animal soul represents the ultimate receiver of the Or Yashar — divine light has descended so far that it now animates a soul that doesn't consciously perceive its divine source. The work of *avodah* is to transform this into Or Chozer — to generate, from within this concealed state, an upward movement toward G-d.

### 3. The Taarav's Contribution: The "Outer" vs. "Inner" Animal Soul
The Rashab distinguishes between the animal soul's *outer* dimension (its manifest desires, emotions, and behaviors) and its *inner* dimension (the divine spark that sustains even the animal soul from within). This inner dimension is what makes transformation (*hafichat hayetzer*) possible — one does not merely suppress the animal soul but reveals its hidden divine root.

---

## The Spiritual Purpose

The Rashab emphasizes that the animal soul is not an obstacle to be destroyed but a vessel to be refined. The entire structure of Torah and mitzvot is designed to work with the animal soul — taking its energies (passion, drive, intensity) and channeling them toward holiness. This is the deeper meaning of *avodah* (service): the animal soul's own energy becoming the fuel for ascent.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| נפש הבהמית | Nefesh HaBehamit | Animal/Vital Soul |
| נפש האלוקית | Nefesh HaElohit | G-dly Soul |
| קליפת נוגה | Kelipat Nogah | Translucent husk/shell |
| ניצוצות | Nitzotzot | Divine sparks within Nogah |
| הפיכת היצר | Hafichat HaYetzer | Transformation of the evil inclination |
| עבודה | Avodah | Divine service/spiritual work |

---

## Cross-References

- [[themes/souls-of-israel|Souls of Israel]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/ratzo-veshov|Ratzo v'Shov]]
- [[themes/yechida|Yechida — The Highest Soul-Level]]
- [[index|Main Index]]
"""
    },
    "souls-of-israel": {
        "title": "נשמות ישראל — The Souls of Israel",
        "content": """---
title: "נשמות ישראל — Souls of Israel"
tags:
  - themes
  - taarav
  - kabbalah
  - theology
---

# נשמות ישראל — The Souls of Israel

**The Unique Nature of Jewish Souls as Explained in Hemshech Taarav**

---

## Introduction

One of the most developed and profound themes in the Hemshech Taarav is the nature of **Neshamos Yisrael** (נשמות ישראל — Souls of Israel). The Rashab provides an unprecedented metaphysical account of the Jewish soul — its divine root, its structure, its descent, and its mission — weaving together Kabbalistic frameworks with the deepest principles of Chassidic thought.

---

## The Divine Root of Jewish Souls

The Rashab teaches that Jewish souls are rooted in the **highest levels of the divine structure** — specifically in *Atzilut* (the World of Emanation), and ultimately in the *Yechida* level that connects to *Keter* (Crown) and beyond. This is not merely a metaphor: the soul is literally "a part of G-d from above" (*chelek Eloka mima'al mamash*) — not just a created being that was breathed into by G-d, but an actual extension of divinity.

### The Soul's Structure — Five Levels
The Rashab develops in detail the five levels of the soul:
1. **Nefesh** (נפש) — the animating level, connected to action and the body
2. **Ruach** (רוח) — the emotional level
3. **Neshama** (נשמה) — the intellectual level
4. **Chaya** (חיה) — the "living" level, connected to the Or Makif (surrounding light)
5. **Yechida** (יחידה) — the unique/singular level, connected directly to the Essence of G-d

The hemshech focuses especially on the higher levels (Chaya and Yechida) as the key to understanding the soul's mission.

---

## Souls of Tohu vs. Souls of Tikkun

A crucial distinction in the Taarav: not all Jewish souls have the same root. Some souls are rooted in **Olam HaTohu** (World of Chaos) — they carry within them the intense, powerful sparks that survived the Shevirat HaKelim. Other souls are rooted in **Olam HaTikkun** — they are oriented toward balance, containment, and systematic refinement.

- **Tohu-souls**: Characterized by great intensity, passion, and power; may be prone to extremism but capable of extraordinary spiritual heights
- **Tikkun-souls**: Characterized by balance, structure, and sustained service; their mission is the systematic elevation of the material world through Torah and mitzvot

Both types of souls are essential to the overall Tikkun (rectification) of reality.

---

## The Soul's Descent and Mission

Why does the soul descend into the physical world? The Rashab's answer in the Taarav is multi-layered:

1. **To reveal Or Chozer**: The soul's descent generates the "reflected light" that can only arise from below — an ascent from within the material world is more powerful than even the highest spiritual levels that never descended.

2. **To elevate the nitzotzot**: The scattered divine sparks embedded in the physical world can only be elevated by a soul that has descended into that world and engaged with it through Torah and mitzvot.

3. **To reveal the Yechida**: The ultimate purpose of all spiritual work is to reveal the *Yechida* — the soul's innermost point that is directly united with G-d — within the context of the material world.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| נשמה | Neshama | Soul (general) |
| חלק אלוקה ממעל | Chelek Eloka Mima'al | "A portion of G-d from above" |
| ירידה לצורך עלייה | Yeridah L'Tzorech Aliyah | Descent for the purpose of ascent |
| ניצוצות | Nitzotzot | Divine sparks to be elevated |
| תיקון | Tikkun | Rectification/repair |
| יחידה | Yechida | Singular — the highest soul-level |

---

## Cross-References

- [[themes/yechida|Yechida — The Highest Soul-Level]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/nefesh-habehamit|Nefesh HaBehamit]]
- [[themes/ratzo-veshov|Ratzo v'Shov]]
- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[index|Main Index]]
"""
    },
    "kav-reshimu": {
        "title": "קו ורשימו — The Line and the Impression",
        "content": """---
title: "קו ורשימו — Kav and Reshimu"
tags:
  - themes
  - taarav
  - kabbalah
---

# קו ורשימו — Kav and Reshimu: The Line and the Impression

**The Residual Divine Trace After Tzimtzum**

---

## Introduction

After the primordial **Tzimtzum** (צמצום — contraction/withdrawal) created the *chalal* (empty space), two crucial elements made the creation of worlds possible: the **Reshimu** (רשימו — the impression/trace that remained) and the **Kav** (קו — the thin line of Or Ein Sof drawn back into the chalal). The Hemshech Taarav provides the most detailed and philosophically rigorous analysis of these concepts in Chabad literature.

---

## The Reshimu — The Impression

When the Or Ein Sof withdrew in the Tzimtzum, it did not leave the chalal completely empty. A faint **reshimu** (impression, residue, or "fingerprint") of the Or Ein Sof remained.

The Rashab uses several analogies:
- Like the fragrance remaining in a vessel after its perfume has been poured out
- Like the impression left by a ring in wax after the ring is removed
- Like the warmth remaining in a room after the heat source has been removed

**Why is the Reshimu necessary?**
Without the reshimu, the chalal would be a true void — complete non-existence, utterly disconnected from divinity. With the reshimu, there is still a point of divine connection within the chalal, providing the "ground" upon which the Kav can act to build the worlds.

The reshimu corresponds to a very contracted, dim, almost imperceptible level of Or Ein Sof. It is "the minimum of the minimum" of divine illumination. Yet it is precisely this minimal quality that allows it to serve as the foundation for finite worlds — which require limitation.

---

## The Kav — The Line

After the Tzimtzum, a thin "line" of Or Ein Sof was extended from the Ein Sof into the chalal. This **Kav** is not a physical line but a metaphor for a single, sequential, directed flow of divine energy — in contrast to the undifferentiated fullness of Or Ein Sof before the Tzimtzum.

Key characteristics of the Kav:
- It has a beginning (close to the Ein Sof) and an end (at the lowest level of the chalal)
- It carries a graduated, sequential light that can interact with the reshimu
- It is the vehicle through which all the *sefirot* and *partzufim* develop
- It represents the divine will actively entering the space of creation

The **interaction of the Kav with the Reshimu** produces the various levels of spiritual reality — from the highest world of Atzilut down to the physical world.

---

## The Rashab's Deepest Analysis

In the Taarav, the Rashab asks and answers the profound question: **What is the relationship between the Kav and the Reshimu?**

His answer: The Reshimu contains the potential for all the worlds in a dormant, contracted form. The Kav "activates" this potential — like a spark activating dormant material. The particular quality of the Reshimu determines the nature and limitations of each world. The Kav provides the active divine energy; the Reshimu provides the "mold" or "template."

This analysis becomes the basis for understanding why the worlds of Tohu and Tikkun differ: they represent different relationships between the Kav's energy and the Reshimu's capacity for containment.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| קו | Kav | Line — the directed beam of Or Ein Sof after Tzimtzum |
| רשימו | Reshimu | Impression/trace remaining in the chalal after Tzimtzum |
| חלל | Chalal | The empty space created by the Tzimtzum |
| עיגולים | Igulim | Circles — one model of post-Tzimtzum light |
| יושר | Yosher | Straightness/linearity — the structure of the Kav |

---

## Cross-References

- [[themes/tzimtzum|Tzimtzum]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[index|Main Index]]
"""
    },
    "sefirot-in-taarav": {
        "title": "הספירות בתער\"ב — The Sefirot in Hemshech Taarav",
        "content": """---
title: "הספירות בתער\"ב — Sefirot in Hemshech Taarav"
tags:
  - themes
  - taarav
  - kabbalah
---

# הספירות בתער"ב — The Sefirot in Hemshech Taarav

**How the Ten Sefirot Are Analyzed Uniquely in Hemshech Taarav**

---

## Introduction

The **Sefirot** (ספירות — divine attributes/emanations) are the foundational structure of Kabbalistic thought. The Hemshech Taarav provides the most systematic and philosophically sophisticated analysis of the sefirot in Chabad literature, going far beyond the standard Lurianic and earlier Chabad treatments.

---

## The Ten Sefirot — Overview

The ten sefirot are:

| # | Hebrew | Transliteration | Dimension |
|---|--------|-----------------|-----------|
| 1 | כתר | Keter | Crown — divine will and delight |
| 2 | חכמה | Chochma | Wisdom — the point of divine thought |
| 3 | בינה | Bina | Understanding — the womb of divine thought |
| 4 | חסד | Chesed | Lovingkindness |
| 5 | גבורה | Gevura | Strength/severity |
| 6 | תפארת | Tiferet | Beauty/harmony |
| 7 | נצח | Netzach | Victory/eternity |
| 8 | הוד | Hod | Splendor |
| 9 | יסוד | Yesod | Foundation |
| 10 | מלכות | Malchut | Kingship/presence |

---

## The Rashab's Unique Contributions in Taarav

### 1. The "Inner" vs. "Outer" Dimensions of Each Sefirah
The Rashab analyzes each sefirah as containing both a *pnimiyut* (inner dimension) and a *chitzoniyut* (outer dimension). The pnimiyut of a sefirah is its essential divine quality; the chitzoniyut is its functional expression in relation to other sefirot and worlds below.

### 2. The Sefirot of Tohu vs. Sefirot of Tikkun
A crucial distinction in the Taarav: the sefirot of Olam HaTohu functioned as independent points (*nekudim*), with each sefirah expressing itself fully but without integration. The sefirot of Olam HaTikkun function as integrated *Partzufim* — each sefirah contains all ten sefirot within itself, and all sefirot are coordinated into larger personalities.

This distinction explains why Tohu was more powerful but unstable: greater lights, but no vessels to sustain them.

### 3. The Sefirot and Or Yashar/Or Chozer
Each sefirah participates in the dual dynamic of Or Yashar (receiving from above, giving below) and Or Chozer (reflecting upward). The Rashab analyzes how each sefirah mediates between the infinite and the finite, making divine energy accessible to lower levels while also generating an upward response.

### 4. Chochma — The Primordial Point
The Rashab gives special attention to **Chochma** (Wisdom) as the first emanation of true differentiation from Keter. Chochma is called the *nekudah ha'rishonah* (first point) — the initial contraction of divine wisdom into a specific, distinct "thought." Its characteristic of *bitul* (self-nullification) makes it the channel for divine revelation into the structured worlds below.

### 5. The Relationship Between Keter and Ein Sof
The Taarav extensively analyzes the mysterious relationship between **Keter** (Crown) — the highest sefirah, which is really beyond the sefirot — and the Or Ein Sof above it. Keter is the divine will that initiated creation; it stands at the boundary between the Ein Sof (beyond all structure) and Chochma (the beginning of structure).

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| ספירות | Sefirot | Divine emanations/attributes |
| אצילות | Atzilut | World of Emanation where sefirot dwell |
| פרצופים | Partzufim | Divine configurations (Tikkun structure) |
| בטול | Bitul | Self-nullification — key quality of Chochma |
| מקיף | Makif | Surrounding/encompassing light |
| פנימי | Pnimi | Inner/internalized light |

---

## Cross-References

- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/tohu-and-tikkun|Tohu and Tikkun]]
- [[themes/kav-reshimu|Kav and Reshimu]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[themes/yechida|Yechida]]
- [[index|Main Index]]
"""
    },
    "yechida": {
        "title": "יחידה — The Highest Level of the Soul",
        "content": """---
title: "יחידה — Yechida: The Highest Soul-Level"
tags:
  - themes
  - taarav
  - kabbalah
  - psychology
---

# יחידה — Yechida: The Highest Soul-Level

**The Unique/Singular Dimension of the Soul in Hemshech Taarav**

---

## Introduction

**Yechida** (יחידה — literally "unique" or "singular one") is the fifth and highest level of the Jewish soul. In the Hemshech Taarav, the Rashab gives the most detailed and philosophically developed account of the Yechida in Chabad literature, revealing it as the key to understanding both the soul's ultimate nature and the purpose of all spiritual work.

---

## The Five Levels of the Soul — Brief Review

1. **Nefesh** — animating soul; connected to the body and action
2. **Ruach** — spirit; the seat of emotions
3. **Neshama** — soul proper; the seat of intellect
4. **Chaya** — life; connected to the encompassing light (*Or Makif*) of the soul
5. **Yechida** — the singular one; the essential point of the soul

---

## The Nature of Yechida

The Yechida is called "singular" for two reasons:

1. **It is singular within the soul**: Just as G-d is one and unique, the Yechida is the singular, essential point of the soul that cannot be further subdivided. All other soul-levels can be analyzed into sub-components; the Yechida is the irreducible core.

2. **It is united with the Divine**: The Yechida is the dimension of the soul that is *literally* at one with the Ein Sof. It does not merely connect to or reflect G-d — it *is* a genuine aspect of the divine oneness, present within the human soul.

---

## The Yechida and Keter

The Rashab draws a precise correspondence: the five soul-levels parallel the five levels of the divine structure:
- Nefesh ↔ Malchut/Asiya
- Ruach ↔ Ze'ir Anpin/Yetzira
- Neshama ↔ Bina/Beriya
- Chaya ↔ Chochma/Atzilut
- **Yechida ↔ Keter/**Adam Kadmon

The Yechida corresponds to **Keter** — the divine crown that transcends all the sefirot and borders on the Or Ein Sof itself. This means the Yechida is not merely a created spiritual entity but genuinely partakes of the divine essence.

---

## The Yechida in Spiritual Practice

The Rashab emphasizes that while the Yechida is always present in the soul, it is generally *hidden* and must be *revealed* through spiritual work:

- **In ordinary times**: The Yechida operates as the hidden foundation of the soul's connection to G-d, sustaining it even when the conscious levels (Nefesh, Ruach, Neshama) are not aware of it.

- **In *mesirut nefesh* (self-sacrifice)**: When a Jew faces a situation requiring him to give up his life for G-d, it is the Yechida that is activated — the individual transcends all personal interests and unites purely with G-d. This is the highest expression of the Yechida.

- **In deep meditation (*hisponenut*)**: The systematic meditation on divine concepts (central to Chabad practice) can cultivate an awareness that reaches toward the Yechida.

---

## The Ultimate Goal: Revealing Yechida Below

The Rashab teaches that the entire purpose of the descent of the soul into the physical world is ultimately to **reveal the Yechida within the material realm**. When a Jew lives a life of Torah and mitzvot with depth and intention, the Yechida's divine quality becomes manifest even in the lowest levels of physical existence — and this is the ultimate Tikkun (rectification) that creation is moving toward.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| יחידה | Yechida | Singular/unique — highest soul-level |
| מסירות נפש | Mesirut Nefesh | Self-sacrifice; activates Yechida |
| כתר | Keter | Crown — the sefirah corresponding to Yechida |
| אדם קדמון | Adam Kadmon | Primordial Man — cosmic level above Atzilut |
| אור מקיף | Or Makif | Surrounding/encompassing light |
| גילוי | Giluy | Revelation — bringing the hidden to light |

---

## Cross-References

- [[themes/souls-of-israel|Souls of Israel]]
- [[themes/ratzo-veshov|Ratzo v'Shov]]
- [[themes/sefirot-in-taarav|Sefirot in Taarav]]
- [[themes/nefesh-habehamit|Nefesh HaBehamit]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[index|Main Index]]
"""
    },
    "ratzo-veshov": {
        "title": "רצוא ושוב — Running and Returning",
        "content": """---
title: "רצוא ושוב — Ratzo v'Shov: Running and Returning"
tags:
  - themes
  - taarav
  - kabbalah
  - avodah
---

# רצוא ושוב — Ratzo v'Shov: Running and Returning

**The Dynamic of Spiritual Ascent and Descent in Hemshech Taarav**

---

## Introduction

**Ratzo v'Shov** (רצוא ושוב — "running and returning") is a biblical phrase from Ezekiel's vision of the *Chayot* (divine creatures): "And the living creatures ran and returned (*ratzo vashov*), like the appearance of lightning" (Ezekiel 1:14). In Chabad Chassidus, this becomes a fundamental metaphor for the dynamic of spiritual life. The Hemshech Taarav provides the deepest analysis of this concept, integrating it with the hemshech's broader framework of Or Yashar/Or Chozer, Tzimtzum, and the soul's mission.

---

## The Basic Framework

**Ratzo (רצוא — Running/Yearning):**
The movement of the soul upward — toward G-d, toward the Infinite, toward nullification of self (*bitul*). This corresponds to *Or Chozer* (reflected light) — the soul's response to the divine, its longing to transcend its limited existence and merge with its source.

**Shov (שוב — Returning/Coming Back):**
The return to engaged, purposeful existence in the world. After the soul has ascended in meditation, prayer, or divine inspiration, it returns to the practical work of life — Torah study, mitzvot, relationships, and the refinement of the material world. This corresponds to *Or Yashar* (direct light) — the divine flowing downward into active engagement with reality.

---

## The Rashab's Development in Taarav

### 1. Ratzo v'Shov as the Cosmic Pattern
The Rashab shows that Ratzo v'Shov is not merely a human psychological dynamic but a cosmic principle. The very existence of the worlds depends on a constant "pulsing" between Or Yashar (divine energy flowing down) and Or Chozer (created reality responding upward). All spiritual reality "breathes" in this rhythm.

### 2. The Danger of Ratzo Without Shov
The Rashab analyzes the *Chayot* of Ezekiel's vision: why do they run AND return? Because pure *ratzo* — unending ascent without return — leads to *bitul* (total nullification/dissolution). The soul might be so overwhelmed by the divine light that it loses its individuality and can no longer fulfill its mission in the world. *Shov* prevents this — it brings the soul back to serve G-d through practical engagement.

### 3. The Superiority of Shov
Paradoxically, the Rashab teaches that the *shov* — the return to the world — is ultimately more valuable than the *ratzo*. The reason: *ratzo* is the soul seeking what it needs (connection to G-d); *shov* is the soul giving — fulfilling G-d's desire for a dwelling in the lower realms. The divine purpose is not the soul's individual spiritual bliss but the transformation of the material world into a dwelling place for G-d (*dirah b'tachtonim*).

### 4. Ratzo v'Shov in Prayer
The classic context for Ratzo v'Shov in practice is **prayer** (*tefillah*). Chabad prayer involves a sustained, structured ascent (*ratzo*) through meditation on divine greatness, followed by a return (*shov*) to practical life carrying the consciousness gained in prayer. The Rashab analyzes how authentic prayer must contain both movements.

---

## Connection to Or Yashar and Or Chozer

The correspondence is precise:
- **Or Yashar** = the divine energy flowing down = **Shov** (G-d "returning" to engage with the world through us)
- **Or Chozer** = the soul's response ascending = **Ratzo** (the soul running toward its source)

This elegant symmetry shows how the cosmic light-dynamics and the experiential soul-dynamics are aspects of the same underlying reality.

---

## Key Hebrew Terms

| Hebrew | Transliteration | Meaning |
|--------|-----------------|---------|
| רצוא | Ratzo | Running, yearning — the upward movement |
| שוב | Shov | Returning — the downward movement back to world |
| ביטול | Bitul | Self-nullification; the goal of Ratzo |
| דירה בתחתונים | Dirah B'Tachtonim | G-d's dwelling in the lower realms |
| חיות | Chayot | Divine creatures in Ezekiel's vision |
| התפעלות | Hitpa'alut | Emotional/spiritual excitement (associated with Ratzo) |

---

## Cross-References

- [[themes/or-yashar-or-chozer|Or Yashar v'Or Chozer]]
- [[themes/souls-of-israel|Souls of Israel]]
- [[themes/yechida|Yechida]]
- [[themes/nefesh-habehamit|Nefesh HaBehamit]]
- [[themes/ohr-ein-sof|Or Ein Sof]]
- [[index|Main Index]]
"""
    },
}


def main():
    base = "/workspace/group/taarav-wiki/content"
    os.makedirs(f"{base}/maamarim", exist_ok=True)
    os.makedirs(f"{base}/themes", exist_ok=True)
    os.makedirs(f"{base}/years", exist_ok=True)

    # Generate maamar pages
    maamar_count = 0
    for m in MAAMARIM:
        maamar_id, occasion_heb, year_heb, chelek, english_occasion = m
        slug = safe_slug(maamar_id)
        page_content = generate_maamar_page(maamar_id, occasion_heb, year_heb, chelek, english_occasion)
        path = f"{base}/maamarim/{slug}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        maamar_count += 1

    print(f"Generated {maamar_count} maamar pages")

    # Group maamarim by year for year pages
    by_year = {}
    for m in MAAMARIM:
        year = m[2]
        by_year.setdefault(year, []).append(m)

    year_count = 0
    for year_heb, maamarim_in_year in by_year.items():
        civil = year_to_civil(year_heb)
        chelek = maamarim_in_year[0][3]
        chelek_label = chelek_name(chelek)
        content, year_slug = generate_year_page(year_heb, civil, chelek_label, maamarim_in_year)

        # Sanitize slug
        safe_year_slug = year_heb.replace('"', '').replace("'", '').replace(' ', '-').replace('\\', '')
        path = f"{base}/years/{safe_year_slug}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        year_count += 1

    print(f"Generated {year_count} year pages")

    # Generate theme pages
    theme_count = 0
    for slug, data in THEME_PAGES.items():
        path = f"{base}/themes/{slug}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data['content'])
        theme_count += 1

    print(f"Generated {theme_count} theme pages")

    # Generate index page
    # Build maamar table grouped by year
    maamar_table_parts = []
    year_order = ['תער"ב', 'תער"ג', 'תרד"ע', 'עתר"ו', 'העת"ר']
    for year in year_order:
        if year not in by_year:
            continue
        civil = year_to_civil(year)
        ms = by_year[year]
        chelek = ms[0][3]
        maamar_table_parts.append(f"\n### {year} ({civil}) — {chelek_name(chelek)}\n")
        for m in ms:
            maamar_id, occasion_heb, year_heb, ch, english = m
            slug = safe_slug(maamar_id)
            maamar_table_parts.append(f"- [[maamarim/{slug}|{occasion_heb}]] — {english}")

    maamar_table = "\n".join(maamar_table_parts)

    year_links = "\n".join(
        f"- [[years/{y.replace(chr(34), '').replace(chr(39), '').replace(' ', '-')}|{y} ({year_to_civil(y)})]]: {len(by_year[y])} maamarim"
        for y in year_order if y in by_year
    )

    theme_links = "\n".join(
        f"- [[themes/{slug}|{data['title']}]]"
        for slug, data in THEME_PAGES.items()
    )

    index_content = f"""---
title: "המשך תער״ב — Hemshech Taarav"
tags:
  - index
---

# המשך תער״ב — Hemshech Taarav

**The Longest Chassidic Discourse Ever Written**

---

## Overview

The **Hemshech Taarav** (המשך תער"ב) is the longest chassidic discourse (*hemshech* — a continuous, multi-part discourse) ever composed. It was delivered by **Rabbi Shalom DovBer Schneersohn** (known as the Rashab, the fifth Lubavitcher Rebbe) over approximately two decades, beginning in the year **תער"ב** (5662 / 1901-02) and continuing through **תר"פ** (5680 / 1919-20).

The hemshech spans two volumes and approximately **800 pages**, developing a comprehensive, systematic exposition of Kabbalistic-Chassidic thought. It is considered the pinnacle of the Rashab's literary output and one of the most intellectually demanding texts in the entire Chabad corpus.

---

## Central Themes

The hemshech is organized around several interconnected conceptual poles:

| Theme | Description |
|-------|-------------|
| **[[themes/or-yashar-or-chozer\|Or Yashar v'Or Chozer]]** | The dynamic of direct and reflected divine light — the foundational metaphor |
| **[[themes/tzimtzum\|Tzimtzum]]** | The primordial contraction and its implications for creation |
| **[[themes/tohu-and-tikkun\|Tohu and Tikkun]]** | The worlds of chaos and repair — their lights, vessels, and souls |
| **[[themes/ohr-ein-sof\|Or Ein Sof]]** | The Infinite Light and its relationship to the finite worlds |
| **[[themes/souls-of-israel\|Souls of Israel]]** | The unique divine nature of Jewish souls and their mission |
| **[[themes/yechida\|Yechida]]** | The highest soul-level and its connection to the divine Essence |
| **[[themes/kav-reshimu\|Kav and Reshimu]]** | The line and impression — the residual divine trace after Tzimtzum |
| **[[themes/sefirot-in-taarav\|Sefirot in Taarav]]** | The ten divine attributes as analyzed in this hemshech |
| **[[themes/nefesh-habehamit\|Nefesh HaBehamit]]** | The animal soul in the hemshech's framework |
| **[[themes/ratzo-veshov\|Ratzo v'Shov]]** | Running and returning — the rhythm of spiritual life |

---

## Structure

The hemshech is divided into two *chalakim* (volumes):

- **חלק ראשון (Part 1)**: Years תער"ב, תער"ג, תרד"ע, עתר"ו (1901–1906)
- **חלק שני (Part 2)**: Year העת"ר and beyond (1909-10 onward)

---

## Years of the Hemshech

{year_links}

---

## All Maamarim

{maamar_table}

---

## About the Rashab

Rabbi Shalom DovBer Schneersohn (1860–1920), known as the Rashab, was the fifth Rebbe of Chabad-Lubavitch. He established the Tomchei Tmimim yeshiva system and was renowned for the extraordinary depth and systematic rigor of his chassidic discourses. The Hemshech Taarav represents the culmination of his intellectual and spiritual legacy.

---

*This wiki was built from the Chabad Library edition of the Hemshech Taarav (794 pages, chabadlibrary.org).*
"""

    with open(f"{base}/index.md", 'w', encoding='utf-8') as f:
        f.write(index_content)

    print("Generated index page")
    print(f"\nTotal pages: {maamar_count + year_count + theme_count + 1}")
    print(f"  - Maamarim: {maamar_count}")
    print(f"  - Years: {year_count}")
    print(f"  - Themes: {theme_count}")
    print(f"  - Index: 1")


if __name__ == "__main__":
    main()
