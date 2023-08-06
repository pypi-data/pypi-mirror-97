from newsworthycharts.custom.pts import BroadbandTargetChart
from newsworthycharts.storage import LocalStorage


OUTPUT_DIR = "test/rendered_charts"
local_storage = LocalStorage(OUTPUT_DIR)


def test_lines_to_2030_target():

    chart_obj = {
        "data": [
            [
                ("Stockholms län"	, .9204),
                ("Gotlands län"	, .8868),
                ("Västra Götalands län"	, .8260),
                ("Hallands län"	, .8193),
                ("Västerbottens län"	, .7974),
                ("Skåne län"	, .7746),
                ("Östergötlands län"	, .7639),
                ("Jönköpings län"	, .7617),
                ("Värmlands län"	, .7612),
                ("Västmanlands län"	, .7578),
                ("Södermanlands län"	, .7536),
                ("Gävleborgs län"	, .7468),
                ("Kronobergs län"	, .7306),
                ("Uppsala län"	, .7204),
                ("Örebro län"	, .7176),
                ("Blekinge län"	, .6918),
                ("Norrbottens län"	, .6830),
                ("Dalarnas län"	, .6719),
                ("Hallands län"	, .6650),
                ("Västernorrlands län"	, .6546),
                ("Kalmar län"	, .6332),
            ],
            [
                ("Stockholms län",	.0296),
                ("Gotlands län",	.0632),
                ("Västra Götalands län",	.1240),
                ("Hallands län",	.1307),
                ("Västerbottens län",	.1526),
                ("Skåne län",	.1754),
                ("Östergötlands län",	.1861),
                ("Jönköpings län",	.1883),
                ("Värmlands län",	.1888),
                ("Västmanlands län",	.1922),
                ("Södermanlands län",	.1964),
                ("Gävleborgs län",	.2032),
                ("Kronobergs län",	.2194),
                ("Uppsala län",	.2296),
                ("Örebro län",	.2324),
                ("Blekinge län",	.2582),
                ("Norrbottens län",	.2670),
                ("Dalarnas län",	.2781),
                ("Hallands län",	.2850),
                ("Västernorrlands län",	.2954),
                ("Kalmar län",	.3168),
            ]
        ],
        "labels": ["Täckning i dag", "Kvar till målet"],
        "width": 600,
        "height": 900,
        "stacked": True,
        "units": "percent",
        "bar_orientation": "horizontal",
        "title": "Inga regioner klarar målet"
    }
    c = BroadbandTargetChart.init_from(chart_obj, storage=local_storage)

    c.render("custom_pts_broadband_target", "png")

    