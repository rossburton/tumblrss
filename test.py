#! /usr/bin/env python

from tumblrss import tumblrss

def compare(rss, expected):
    assert len(rss.items) == len(expected)
    for i in range(0, len(rss.items)):
        assert rss.items[i].author == expected[i][0]
        assert rss.items[i].link == expected[i][1]
        assert rss.items[i].guid == expected[i][1]
        if len(expected[i]) == 3:
            assert rss.items[i].title == expected[i][2]
        else:
            assert rss.items[i].title == ""


rss = tumblrss(open("tests/test-1.html").read())
assert len(rss.items) == 5
compare(rss, (
        ("rulesformyunbornson",
         "http://rulesformyunbornson.tumblr.com/post/153115498/383-framing-a-poster-does-not-make-it-valuable",
         "383. Framing a poster does not make it valuable."
         ),
        ("conundrum",
         "http://conundrum.tumblr.com/post/153003804/after-an-evening-of-drinking-wild-turkey-and",
         "7 High Tech Products And Their Cheap Ass Ingredients"
         ),
        ("joshual",
         "http://joshual.tumblr.com/post/152893624/xml-is-like-violence-if-it-doesnt-solve-your",
         "nokogiri-1.3.2 Documentation"
         ),
        ("conundrum",
         "http://conundrum.tumblr.com/post/152196239/dottorcarlo-puscic-comicbooks-death-by-charles"
         ),
        ("joshual",
         "http://joshual.tumblr.com/post/152155725/rossburton-holy-living-f-k"
         )
        ))

rss = tumblrss(open("tests/test-2.html").read())
assert len(rss.items) == 7
compare(rss, (
        ("conundrum",
         "http://conundrum.tumblr.com/post/151597536"),
        ("joshual",
         "http://joshual.tumblr.com/post/151494453/xkcd-a-webcomic-lease-this-is-me-a-month-or"),
        ("joshual",
         "http://joshual.tumblr.com/post/150985551/management-bullshit-generator-from-buzzwords4u-co-uk",
         "Management Bullshit Generator from buzzwords4u.co.uk"),
        ("glinner",
         "http://glinner.tumblr.com/post/150884779/dan-haggerty-kickin-bbq-sauce"),
        ("joshual",
         "http://joshual.tumblr.com/post/150860306/awesome-dan-zambonini"),
        ("conundrum",
         "http://conundrum.tumblr.com/post/150856620/dan-zambonini-london-tube-map-hat-tip-thomas"),
        ("joshual",
         "http://joshual.tumblr.com/post/150772409/the-game-named-page-hunt-presents-users-with-a",
         "Microsoft Bing Could Be Improved with Online Game"
         )
        ))
