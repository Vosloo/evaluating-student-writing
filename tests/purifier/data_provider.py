def get_test_cases() -> list[dict[str, str]]:
    return [
        {
            "input": (
                "dear\xa0state senator,\n\ni belive we should\xa0trash the electoral college and do "
                + "popular votes. this way it is simiple and easyer to control. people may think they "
                + "are voting for president when there not (even know they shouod be).we are really "
                + "voting for electors. i dont see where it is right that thoses electors have to fight"
                + " for are vote. we should be able to put in are balliets and that be it, not worry "
                + "weather the electors had a good agument and won the fight. the electors dont always "
                + "vote for who that state wants. when some people go to vote the are confused on the "
                + "electores and vote the wrong candidate. the electors dont alawys vote for who we "
                + "want sometimes they put that voite aside and vote for whom ever they wish. in all "
                + "realaity we dont need them all they do is cause a mess in the prosses. so i belive "
                + "that we shuld stop the electoral college and do direct voit insted.    "
            ),
            "expected": (
                "dear state senator i belive we should trash the electoral college and do popular "
                + "votes. this way it is simiple and easyer to control. people may think they are "
                + "voting for president when there not even know they shouod be.we are really voting "
                + "for electors. i dont see where it is right that thoses electors have to fight for "
                + "are vote. we should be able to put in are balliets and that be it not worry weather "
                + "the electors had a good agument and won the fight. the electors dont always vote for"
                + " who that state wants. when some people go to vote the are confused on the electores"
                + " and vote the wrong candidate. the electors dont alawys vote for who we want "
                + "sometimes they put that voite aside and vote for whom ever they wish. in all "
                + "realaity we dont need them all they do is cause a mess in the prosses. so i belive "
                + "that we shuld stop the electoral college and do direct voit insted."
            ),
        },
    ]
