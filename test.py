#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tumblrss import tumblrss

def check(a, b):
    if a == b:
        return

    print "'%s' != '%s'" % (a, b)
    raise AssertionError

def compare(items, expected):
    assert len(items) == len(expected)
    for i in range(0, len(items)):
        check(items[i].author, expected[i][0])
        check(items[i].link, expected[i][1])
        check(items[i].guid, expected[i][1])
        if len(expected[i]) == 3:
            check(items[i].title, expected[i][2])
        else:
            check(items[i].title, "")


(items, url) = tumblrss(open("tests/test-1.html").read())
check (url, "http://tumblr.com/dashboard/2/151787926")
assert len(items) == 5
compare(items, (
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
         u"nokogiri-1.3.2 Documentation | I’m now sold on XML!"
         ),
        ("conundrum",
         "http://conundrum.tumblr.com/post/152196239/dottorcarlo-puscic-comicbooks-death-by-charles"
         ),
        ("joshual",
         "http://joshual.tumblr.com/post/152155725/rossburton-holy-living-f-k"
         )
        ))

(items, url) = tumblrss(open("tests/test-2.html").read())
check(url, "http://tumblr.com/dashboard/3/150772409")
assert len(items) == 7
compare(items, (
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
         u"Microsoft Bing Could Be Improved with Online Game\nYeah, “game” …"
         )
        ))


(items, url) = tumblrss(open("tests/test-3.html").read())
check(url, "http://tumblr.com/dashboard/4/150347591")
assert len(items) == 9
compare(items, (
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
         u"Microsoft Bing Could Be Improved with Online Game\nYeah, “game” …"
         ),
        ("conundrum",
         "http://conundrum.tumblr.com/post/150742879/we-welcome-people-of-any-gender-identity-or",
         u"Dreamwidth’s Diversity Statement | I want this on every open source  project I partecipate or contribute to."),
        ("rulesformyunbornson",
         "http://rulesformyunbornson.tumblr.com/post/150392453/mac-makes-a-strong-case-for-pleats"),
        ("rulesformyunbornson",
         "http://rulesformyunbornson.tumblr.com/post/150391892/never-give-an-order-that-cant-be-obeyed",
         "Gen. Douglas MacArthur"),
        ("rulesformyunbornson",
         "http://rulesformyunbornson.tumblr.com/post/150347591/required-listening-crowded-house-something-so")
))
