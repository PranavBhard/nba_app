#URL
https://site.web.api.espn.com/apis/personalized/v2/scoreboard/header?sport=basketball&league=nba&region=us&lang=en&contentorigin=espn&dates={YYYYMMDD}&tz=America%2FNew_York

Note: This example response has the "odds" section for each game (event). Typically, you see this structure before the game has started.

#Response
```json
{
  "sports": [
    {
      "id": "40",
      "uid": "s:40",
      "guid": "cd70a58e-a830-330c-93ed-52360b51b632",
      "name": "Basketball",
      "slug": "basketball",
      "logos": [
        {
          "href": "https://a.espncdn.com/combiner/i?img=/redesign/assets/img/icons/ESPN-icon-basketball.png",
          "alt": "",
          "rel": [
            "full",
            "default"
          ],
          "width": 500,
          "height": 500
        },
        {
          "href": "https://a.espncdn.com/guid/cd70a58e-a830-330c-93ed-52360b51b632/logos/default-dark.png",
          "alt": "",
          "rel": [
            "full",
            "dark"
          ],
          "width": 500,
          "height": 500
        }
      ],
      "leagues": [
        {
          "id": "46",
          "uid": "s:40~l:46",
          "name": "National Basketball Association",
          "abbreviation": "NBA",
          "shortName": "NBA",
          "slug": "nba",
          "tag": "nba",
          "isTournament": false,
          "smartdates": [
            "2025-12-01T08:00Z",
            "2025-12-02T08:00Z",
            "2025-12-03T08:00Z"
          ],
          "events": [
            {
              "id": "401810173",
              "uid": "s:40~l:46~e:401810173~c:401810173",
              "guid": "3ebb54ba-65e0-3dee-9bc9-c3a9b202d806",
              "date": "2025-12-03T00:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Washington Wizards at Philadelphia 76ers",
              "shortName": "WSH @ PHI",
              "seriesSummary": "PHI leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810173/wizards-76ers",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/philadelphia-76ers-tickets-xfinity-mobile-arena-12-2-2025--sports-nba-basketball/production/5940282?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/wells-fargo-center-pa-tickets/venue/564?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810173",
              "location": "Wells Fargo Center",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810173/wizards-76ers",
              "status": "pre",
              "summary": "12/2 - 7:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 894,
                  "broadcastId": 894,
                  "name": "NBC Sports Philadelphia",
                  "shortName": "NBC Sports Phil",
                  "callLetters": "NBC Sports Phil",
                  "station": "NBC Sports Phil",
                  "lang": "en",
                  "region": "us",
                  "slug": "nbc-sports-phil"
                },
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 812,
                  "broadcastId": 812,
                  "name": "Monumental Sports Network",
                  "shortName": "MNMT",
                  "callLetters": "MNMT",
                  "station": "MNMT",
                  "lang": "en",
                  "region": "us",
                  "slug": "mnmt"
                },
                {
                  "typeId": 6,
                  "priority": 3,
                  "type": "Subscription Package",
                  "isNational": false,
                  "broadcasterId": 887,
                  "broadcastId": 887,
                  "name": "NBA League Pass",
                  "shortName": "NBA League Pass",
                  "callLetters": "NBA League Pass",
                  "station": "NBA League Pass",
                  "lang": "en",
                  "region": "us",
                  "slug": "nba-league-pass"
                }
              ],
              "broadcast": "",
              "odds": {
                "details": "PHI -13.5",
                "overUnder": 235.5,
                "spread": -13.5,
                "overOdds": -108,
                "underOdds": -112,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": -850
                },
                "away": {
                  "moneyLine": 575
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 575,
                  "spreadOdds": -110,
                  "team": {
                    "id": "27",
                    "abbreviation": "WSH",
                    "displayName": "Washington Wizards",
                    "name": "Wizards"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -850,
                  "spreadOdds": -110,
                  "team": {
                    "id": "20",
                    "abbreviation": "PHI",
                    "displayName": "Philadelphia 76ers",
                    "name": "76ers"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "-13.5",
                      "odds": "-102"
                    },
                    "close": {
                      "line": "-13.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0HC82432683N1350_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:PHI-13.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+13.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+13.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0HC82432683P1350_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:WSH+13.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "-850"
                    },
                    "close": {
                      "odds": "-850",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0ML82432683_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+575"
                    },
                    "close": {
                      "odds": "+575",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0ML82432683_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o237.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o235.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0OU82432683O23550_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:235.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u237.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u235.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229977%3Foutcomes%3D0OU82432683U23550_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810173,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:235.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 7:00 PM EST",
                  "shortDetail": "12/2 - 7:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "27",
                  "guid": "64d73af6-b8ec-e213-87e8-a4eab3a692e7",
                  "uid": "s:40~l:46~t:27",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Washington Wizards",
                  "name": "Wizards",
                  "abbreviation": "WSH",
                  "location": "Washington",
                  "color": "e31837",
                  "alternateColor": "002b5c",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/wsh/washington-wizards",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/wsh/washington-wizards",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/wsh/washington-wizards",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/wsh",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/wsh",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/wsh/washington-wizards",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/wsh",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/wsh",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/wsh",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "3-16",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 3
                    },
                    "losses": {
                      "value": 16
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": -6.5
                    },
                    "pointsFor": {
                      "value": 2154
                    },
                    "pointsAgainst": {
                      "value": 2424
                    },
                    "avgPointsFor": {
                      "value": 113.368423461914
                    },
                    "avgPointsAgainst": {
                      "value": 127.578948974609
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.157894730567932
                    },
                    "leagueWinPercent": {
                      "value": 0.142857149243355
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 2
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.333333343267441
                    },
                    "streak": {
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 15
                    },
                    "gamesBehind": {
                      "value": 13
                    },
                    "conferenceWins": {
                      "value": 2
                    },
                    "conferenceLosses": {
                      "value": 12
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 6
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 10
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/wsh.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/wsh.png"
                },
                {
                  "id": "20",
                  "guid": "ca1685ed-b799-53e4-7924-e58ea6eb8f3a",
                  "uid": "s:40~l:46~t:20",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Philadelphia 76ers",
                  "name": "76ers",
                  "abbreviation": "PHI",
                  "location": "Philadelphia",
                  "color": "1d428a",
                  "alternateColor": "e01234",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/phi/philadelphia-76ers",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/phi/philadelphia-76ers",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/phi/philadelphia-76ers",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/phi",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/phi",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/phi/philadelphia-76ers",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/phi",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/phi",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/phi",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "10-9",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 10
                    },
                    "losses": {
                      "value": 9
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 0.5
                    },
                    "pointsFor": {
                      "value": 2245
                    },
                    "pointsAgainst": {
                      "value": 2258
                    },
                    "avgPointsFor": {
                      "value": 118.157897949219
                    },
                    "avgPointsAgainst": {
                      "value": 118.842102050781
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.526315808296204
                    },
                    "leagueWinPercent": {
                      "value": 0.5
                    },
                    "divisionWins": {
                      "value": 5
                    },
                    "divisionLosses": {
                      "value": 2
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.714285731315613
                    },
                    "streak": {
                      "value": -1
                    },
                    "playoffSeed": {
                      "value": 9
                    },
                    "gamesBehind": {
                      "value": 6
                    },
                    "conferenceWins": {
                      "value": 9
                    },
                    "conferenceLosses": {
                      "value": 9
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 5
                    },
                    "homeLosses": {
                      "value": 6
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 3
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phi.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/phi.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810173",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810174",
              "uid": "s:40~l:46~e:401810174~c:401810174",
              "guid": "fdcd9f25-5559-35e5-a387-c5e96776a099",
              "date": "2025-12-03T00:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Portland Trail Blazers at Toronto Raptors",
              "shortName": "POR @ TOR",
              "seriesSummary": "Series starts 12/2",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810174/trail-blazers-raptors",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/toronto-raptors-tickets-scotiabank-arena-12-2-2025--sports-nba-basketball/production/5940367?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/scotiabank-arena-tickets/venue/24?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810174",
              "location": "Scotiabank Arena",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810174/trail-blazers-raptors",
              "status": "pre",
              "summary": "12/2 - 7:30 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 492,
                  "broadcastId": 492,
                  "name": "The Sports Network",
                  "shortName": "TSN",
                  "callLetters": "TSN",
                  "station": "TSN",
                  "lang": "en",
                  "region": "us",
                  "slug": "tsn"
                },
                {
                  "typeId": 4,
                  "priority": 2,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1173,
                  "broadcastId": 1173,
                  "name": "BlazerVision",
                  "shortName": "BlazerVision",
                  "callLetters": "BlazerVision",
                  "station": "BlazerVision",
                  "lang": "en",
                  "region": "us",
                  "slug": "blazervision"
                },
                {
                  "typeId": 6,
                  "priority": 3,
                  "type": "Subscription Package",
                  "isNational": false,
                  "broadcasterId": 887,
                  "broadcastId": 887,
                  "name": "NBA League Pass",
                  "shortName": "NBA League Pass",
                  "callLetters": "NBA League Pass",
                  "station": "NBA League Pass",
                  "lang": "en",
                  "region": "us",
                  "slug": "nba-league-pass"
                }
              ],
              "broadcast": "",
              "odds": {
                "details": "TOR -5.5",
                "overUnder": 231.5,
                "spread": -5.5,
                "overOdds": -110,
                "underOdds": -110,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": -218
                },
                "away": {
                  "moneyLine": 180
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 180,
                  "spreadOdds": -120,
                  "team": {
                    "id": "22",
                    "abbreviation": "POR",
                    "displayName": "Portland Trail Blazers",
                    "name": "Trail Blazers"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -218,
                  "spreadOdds": 100,
                  "team": {
                    "id": "28",
                    "abbreviation": "TOR",
                    "displayName": "Toronto Raptors",
                    "name": "Raptors"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "-5.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-5.5",
                      "odds": "EVEN",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0HC82432684N550_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:TOR-5.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+5.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+5.5",
                      "odds": "-120",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0HC82432684P550_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:POR+5.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "-218"
                    },
                    "close": {
                      "odds": "-218",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0ML82432684_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+180"
                    },
                    "close": {
                      "odds": "+180",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0ML82432684_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o232.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o231.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0OU82432684O23150_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:231.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u232.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u231.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229978%3Foutcomes%3D0OU82432684U23150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810174,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:231.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 7:30 PM EST",
                  "shortDetail": "12/2 - 7:30 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "22",
                  "guid": "ed294c02-3c44-db14-9e06-1b4e8cff9558",
                  "uid": "s:40~l:46~t:22",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Portland Trail Blazers",
                  "name": "Trail Blazers",
                  "abbreviation": "POR",
                  "location": "Portland",
                  "color": "e03a3e",
                  "alternateColor": "000000",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/por/portland-trail-blazers",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/por/portland-trail-blazers",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/por/portland-trail-blazers",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/por",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/por",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/por/portland-trail-blazers",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/por",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/por",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/por",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "8-12",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 8
                    },
                    "losses": {
                      "value": 12
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": -2
                    },
                    "pointsFor": {
                      "value": 2365
                    },
                    "pointsAgainst": {
                      "value": 2423
                    },
                    "avgPointsFor": {
                      "value": 118.25
                    },
                    "avgPointsAgainst": {
                      "value": 121.150001525879
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.400000005960465
                    },
                    "leagueWinPercent": {
                      "value": 0.4375
                    },
                    "divisionWins": {
                      "value": 3
                    },
                    "divisionLosses": {
                      "value": 3
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.5
                    },
                    "streak": {
                      "value": -2
                    },
                    "playoffSeed": {
                      "value": 10
                    },
                    "gamesBehind": {
                      "value": 11.5
                    },
                    "conferenceWins": {
                      "value": 7
                    },
                    "conferenceLosses": {
                      "value": 9
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 3
                    },
                    "homeLosses": {
                      "value": 6
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 6
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/por.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/por.png"
                },
                {
                  "id": "28",
                  "guid": "5a9c33b8-63fd-ff34-a833-925fe89320a6",
                  "uid": "s:40~l:46~t:28",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Toronto Raptors",
                  "name": "Raptors",
                  "abbreviation": "TOR",
                  "location": "Toronto",
                  "color": "d91244",
                  "alternateColor": "000000",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/tor/toronto-raptors",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/tor/toronto-raptors",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/tor/toronto-raptors",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/tor",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/tor",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/tor/toronto-raptors",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/tor",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/tor",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/tor",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "14-7",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 14
                    },
                    "losses": {
                      "value": 7
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 3.5
                    },
                    "pointsFor": {
                      "value": 2469
                    },
                    "pointsAgainst": {
                      "value": 2371
                    },
                    "avgPointsFor": {
                      "value": 117.571426391602
                    },
                    "avgPointsAgainst": {
                      "value": 112.904762268066
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.666666686534882
                    },
                    "leagueWinPercent": {
                      "value": 0.764705896377564
                    },
                    "divisionWins": {
                      "value": 3
                    },
                    "divisionLosses": {
                      "value": 2
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.600000023841858
                    },
                    "streak": {
                      "value": -2
                    },
                    "playoffSeed": {
                      "value": 4
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 13
                    },
                    "conferenceLosses": {
                      "value": 4
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 7
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 7
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/tor.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/tor.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810174",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810175",
              "uid": "s:40~l:46~e:401810175~c:401810175",
              "guid": "49aa88ab-1c6f-34a1-aac1-e06cd2a7faf6",
              "date": "2025-12-03T01:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "New York Knicks at Boston Celtics",
              "shortName": "NY @ BOS",
              "seriesSummary": "NY leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810175/knicks-celtics",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/boston-celtics-tickets-td-garden-12-2-2025--sports-nba-basketball/production/5939615?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/td-garden-tickets/venue/573?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810175",
              "location": "TD Banknorth Garden",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810175/knicks-celtics",
              "status": "pre",
              "summary": "12/2 - 8:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": true,
                  "broadcasterId": 379,
                  "broadcastId": 379,
                  "name": "NBC",
                  "shortName": "NBC",
                  "callLetters": "NBC",
                  "station": "NBC",
                  "lang": "en",
                  "region": "us",
                  "slug": "nbc"
                },
                {
                  "typeId": 1,
                  "priority": 3,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 346,
                  "broadcastId": 346,
                  "name": "MSG Network",
                  "shortName": "MSG",
                  "callLetters": "MSG",
                  "station": "MSG",
                  "lang": "en",
                  "region": "us",
                  "slug": "msg"
                },
                {
                  "typeId": 4,
                  "priority": 2,
                  "type": "Streaming",
                  "isNational": true,
                  "broadcasterId": 789,
                  "broadcastId": 789,
                  "name": "Peacock",
                  "shortName": "Peacock",
                  "callLetters": "Peacock",
                  "station": "Peacock",
                  "lang": "en",
                  "region": "us",
                  "slug": "peacock"
                }
              ],
              "broadcast": "NBC/Peacock",
              "odds": {
                "details": "BOS -1.5",
                "overUnder": 230.5,
                "spread": -1.5,
                "overOdds": -112,
                "underOdds": -108,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": -112
                },
                "away": {
                  "moneyLine": -108
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": true,
                  "underdog": true,
                  "moneyLine": -108,
                  "spreadOdds": -120,
                  "team": {
                    "id": "18",
                    "abbreviation": "NY",
                    "displayName": "New York Knicks",
                    "name": "Knicks"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": -112,
                  "spreadOdds": 100,
                  "team": {
                    "id": "2",
                    "abbreviation": "BOS",
                    "displayName": "Boston Celtics",
                    "name": "Celtics"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "+1.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-1.5",
                      "odds": "EVEN",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0HC82432685N150_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:BOS-1.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-1.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+1.5",
                      "odds": "-120",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0HC82432685P150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:NY+1.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "+102"
                    },
                    "close": {
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0ML82432685_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-122"
                    },
                    "close": {
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0ML82432685_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o229.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o230.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0OU82432685O23050_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:230.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u229.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u230.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229979%3Foutcomes%3D0OU82432685U23050_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810175,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:230.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 8:00 PM EST",
                  "shortDetail": "12/2 - 8:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "18",
                  "guid": "61719eb2-11c3-4e3d-90c3-0a1319fd850b",
                  "uid": "s:40~l:46~t:18",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "New York Knicks",
                  "name": "Knicks",
                  "abbreviation": "NY",
                  "location": "New York",
                  "color": "1d428a",
                  "alternateColor": "f58426",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/ny/new-york-knicks",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/ny/new-york-knicks",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/ny/new-york-knicks",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/ny",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/ny",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/ny/new-york-knicks",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/ny",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/ny",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/ny",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "13-6",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 13
                    },
                    "losses": {
                      "value": 6
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 3.5
                    },
                    "pointsFor": {
                      "value": 2288
                    },
                    "pointsAgainst": {
                      "value": 2146
                    },
                    "avgPointsFor": {
                      "value": 120.421051025391
                    },
                    "avgPointsAgainst": {
                      "value": 112.947364807129
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.684210538864136
                    },
                    "leagueWinPercent": {
                      "value": 0.625
                    },
                    "divisionWins": {
                      "value": 4
                    },
                    "divisionLosses": {
                      "value": 0
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 1
                    },
                    "streak": {
                      "value": 4
                    },
                    "playoffSeed": {
                      "value": 2
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 10
                    },
                    "conferenceLosses": {
                      "value": 6
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 10
                    },
                    "homeLosses": {
                      "value": 1
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 3
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/ny.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/ny.png"
                },
                {
                  "id": "2",
                  "guid": "2ca761df-5f60-b2e9-22ed-e099c46d889b",
                  "uid": "s:40~l:46~t:2",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Boston Celtics",
                  "name": "Celtics",
                  "abbreviation": "BOS",
                  "location": "Boston",
                  "color": "008348",
                  "alternateColor": "ffffff",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/bos/boston-celtics",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/bos/boston-celtics",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/bos/boston-celtics",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/bos",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/bos",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/bos/boston-celtics",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/bos",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/bos",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/bos",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "11-9",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 11
                    },
                    "losses": {
                      "value": 9
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 1
                    },
                    "pointsFor": {
                      "value": 2298
                    },
                    "pointsAgainst": {
                      "value": 2218
                    },
                    "avgPointsFor": {
                      "value": 114.900001525879
                    },
                    "avgPointsAgainst": {
                      "value": 110.900001525879
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.550000011920929
                    },
                    "leagueWinPercent": {
                      "value": 0.571428596973419
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.333333343267441
                    },
                    "streak": {
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 8
                    },
                    "gamesBehind": {
                      "value": 5.5
                    },
                    "conferenceWins": {
                      "value": 8
                    },
                    "conferenceLosses": {
                      "value": 6
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 6
                    },
                    "homeLosses": {
                      "value": 4
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/bos.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/bos.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810175",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810176",
              "uid": "s:40~l:46~e:401810176~c:401810176",
              "guid": "8cc3b11e-28f7-32a7-8edf-e211f07be303",
              "date": "2025-12-03T01:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Minnesota Timberwolves at New Orleans Pelicans",
              "shortName": "MIN @ NO",
              "seriesSummary": "Series starts 12/2",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810176/timberwolves-pelicans",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/new-orleans-pelicans-tickets-smoothie-king-center-12-2-2025--sports-nba-basketball/production/5940342?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/smoothie-king-center-tickets/venue/1191?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810176",
              "location": "Smoothie King Center",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810176/timberwolves-pelicans",
              "status": "pre",
              "summary": "12/2 - 8:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 4,
                  "priority": 1,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1159,
                  "broadcastId": 1159,
                  "name": "Gulf Coast Sports",
                  "shortName": "GCSEN",
                  "callLetters": "GCSEN",
                  "station": "GCSEN",
                  "lang": "en",
                  "region": "us",
                  "slug": "gcsen"
                },
                {
                  "typeId": 4,
                  "priority": 2,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1083,
                  "broadcastId": 1083,
                  "name": "Pelicans.com",
                  "shortName": "Pelicans.com",
                  "callLetters": "Pelicans.com",
                  "station": "Pelicans.com",
                  "lang": "en",
                  "region": "us",
                  "slug": "pelicanscom"
                },
                {
                  "typeId": 4,
                  "priority": 3,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 964,
                  "broadcastId": 964,
                  "name": "FanDuel Sports Network North Extra",
                  "shortName": "FanDuel SN North Extra",
                  "callLetters": "FanDuel SN North Extra",
                  "station": "FanDuel SN North Extra",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-north-extra"
                },
                {
                  "typeId": 6,
                  "priority": 4,
                  "type": "Subscription Package",
                  "isNational": false,
                  "broadcasterId": 887,
                  "broadcastId": 887,
                  "name": "NBA League Pass",
                  "shortName": "NBA League Pass",
                  "callLetters": "NBA League Pass",
                  "station": "NBA League Pass",
                  "lang": "en",
                  "region": "us",
                  "slug": "nba-league-pass"
                }
              ],
              "broadcast": "",
              "odds": {
                "details": "MIN -11.5",
                "overUnder": 232.5,
                "spread": 11.5,
                "overOdds": -108,
                "underOdds": -112,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": 455
                },
                "away": {
                  "moneyLine": -625
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -625,
                  "spreadOdds": -115,
                  "team": {
                    "id": "16",
                    "abbreviation": "MIN",
                    "displayName": "Minnesota Timberwolves",
                    "name": "Timberwolves"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 455,
                  "spreadOdds": -105,
                  "team": {
                    "id": "3",
                    "abbreviation": "NO",
                    "displayName": "New Orleans Pelicans",
                    "name": "Pelicans"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "+8.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+11.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0HC82432686P1150_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:NO+11.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-8.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-11.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0HC82432686N1150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:MIN-11.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "+260"
                    },
                    "close": {
                      "odds": "+455",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0ML82432686_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-325"
                    },
                    "close": {
                      "odds": "-625",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0ML82432686_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o231.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o232.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0OU82432686O23250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:232.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u231.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u232.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229980%3Foutcomes%3D0OU82432686U23250_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810176,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:232.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 8:00 PM EST",
                  "shortDetail": "12/2 - 8:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "16",
                  "guid": "13f727cb-254d-b484-a337-93fcc0047add",
                  "uid": "s:40~l:46~t:16",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Minnesota Timberwolves",
                  "name": "Timberwolves",
                  "abbreviation": "MIN",
                  "location": "Minnesota",
                  "color": "266092",
                  "alternateColor": "79bc43",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/min/minnesota-timberwolves",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/min/minnesota-timberwolves",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/min/minnesota-timberwolves",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/min",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/min",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/min/minnesota-timberwolves",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/min",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/min",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/min",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "12-8",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 12
                    },
                    "losses": {
                      "value": 8
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 2
                    },
                    "pointsFor": {
                      "value": 2383
                    },
                    "pointsAgainst": {
                      "value": 2282
                    },
                    "avgPointsFor": {
                      "value": 119.150001525879
                    },
                    "avgPointsAgainst": {
                      "value": 114.099998474121
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.600000023841858
                    },
                    "leagueWinPercent": {
                      "value": 0.5
                    },
                    "divisionWins": {
                      "value": 3
                    },
                    "divisionLosses": {
                      "value": 3
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.5
                    },
                    "streak": {
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 6
                    },
                    "gamesBehind": {
                      "value": 7.5
                    },
                    "conferenceWins": {
                      "value": 7
                    },
                    "conferenceLosses": {
                      "value": 7
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 7
                    },
                    "homeLosses": {
                      "value": 3
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/min.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/min.png"
                },
                {
                  "id": "3",
                  "guid": "9461f397-7882-94c0-c18c-e89bdc9e570e",
                  "uid": "s:40~l:46~t:3",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "New Orleans Pelicans",
                  "name": "Pelicans",
                  "abbreviation": "NO",
                  "location": "New Orleans",
                  "color": "0a2240",
                  "alternateColor": "b4975a",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/no/new-orleans-pelicans",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/no/new-orleans-pelicans",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/no/new-orleans-pelicans",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/no",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/no",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/no/new-orleans-pelicans",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/no",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/no",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/no",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "3-18",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 3
                    },
                    "losses": {
                      "value": 18
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": -7.5
                    },
                    "pointsFor": {
                      "value": 2335
                    },
                    "pointsAgainst": {
                      "value": 2564
                    },
                    "avgPointsFor": {
                      "value": 111.190475463867
                    },
                    "avgPointsAgainst": {
                      "value": 122.095237731934
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.142857149243355
                    },
                    "leagueWinPercent": {
                      "value": 0.0588235296308994
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 5
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.16666667163372
                    },
                    "streak": {
                      "value": -3
                    },
                    "playoffSeed": {
                      "value": 15
                    },
                    "gamesBehind": {
                      "value": 17
                    },
                    "conferenceWins": {
                      "value": 1
                    },
                    "conferenceLosses": {
                      "value": 16
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 9
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 9
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/no.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/no.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810176",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810177",
              "uid": "s:40~l:46~e:401810177~c:401810177",
              "guid": "c5952654-865d-3663-bab2-bfaf07a0a340",
              "date": "2025-12-03T01:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Memphis Grizzlies at San Antonio Spurs",
              "shortName": "MEM @ SA",
              "seriesSummary": "SA leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810177/grizzlies-spurs",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/san-antonio-spurs-tickets-frost-bank-center-12-2-2025--sports-nba-basketball/production/5939883?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/att-center-tickets/venue/2455?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810177",
              "location": "AT&T Center",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810177/grizzlies-spurs",
              "status": "pre",
              "summary": "12/2 - 8:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 841,
                  "broadcastId": 841,
                  "name": "FanDuel Sports Network Southwest",
                  "shortName": "FanDuel SN SW",
                  "callLetters": "FanDuel SN SW",
                  "station": "FanDuel SN SW",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-sw"
                },
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 840,
                  "broadcastId": 840,
                  "name": "FanDuel Sports Network Southeast",
                  "shortName": "FanDuel SN SE",
                  "callLetters": "FanDuel SN SE",
                  "station": "FanDuel SN SE",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-se"
                },
                {
                  "typeId": 6,
                  "priority": 3,
                  "type": "Subscription Package",
                  "isNational": false,
                  "broadcasterId": 887,
                  "broadcastId": 887,
                  "name": "NBA League Pass",
                  "shortName": "NBA League Pass",
                  "callLetters": "NBA League Pass",
                  "station": "NBA League Pass",
                  "lang": "en",
                  "region": "us",
                  "slug": "nba-league-pass"
                }
              ],
              "broadcast": "",
              "odds": {
                "details": "SA -5.5",
                "overUnder": 232.5,
                "spread": -5.5,
                "overOdds": -105,
                "underOdds": -115,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": -205
                },
                "away": {
                  "moneyLine": 170
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 170,
                  "spreadOdds": -112,
                  "team": {
                    "id": "29",
                    "abbreviation": "MEM",
                    "displayName": "Memphis Grizzlies",
                    "name": "Grizzlies"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -205,
                  "spreadOdds": -108,
                  "team": {
                    "id": "24",
                    "abbreviation": "SA",
                    "displayName": "San Antonio Spurs",
                    "name": "Spurs"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "-5.5",
                      "odds": "-105"
                    },
                    "close": {
                      "line": "-5.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0HC82432689N550_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:SA-5.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+5.5",
                      "odds": "-115"
                    },
                    "close": {
                      "line": "+5.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0HC82432689P550_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:MEM+5.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "-205"
                    },
                    "close": {
                      "odds": "-205",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0ML82432689_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+170"
                    },
                    "close": {
                      "odds": "+170",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0ML82432689_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o230.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o232.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0OU82432689O23250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:232.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u230.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u232.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229981%3Foutcomes%3D0OU82432689U23250_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810177,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:232.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 8:00 PM EST",
                  "shortDetail": "12/2 - 8:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "29",
                  "guid": "af5d4942-aeb5-2d07-2a8a-f70b54617e51",
                  "uid": "s:40~l:46~t:29",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Memphis Grizzlies",
                  "name": "Grizzlies",
                  "abbreviation": "MEM",
                  "location": "Memphis",
                  "color": "5d76a9",
                  "alternateColor": "12173f",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/mem/memphis-grizzlies",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/mem/memphis-grizzlies",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/mem/memphis-grizzlies",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/mem",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/mem",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/mem/memphis-grizzlies",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/mem",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/mem",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/mem",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "9-12",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 9
                    },
                    "losses": {
                      "value": 12
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": -1.5
                    },
                    "pointsFor": {
                      "value": 2381
                    },
                    "pointsAgainst": {
                      "value": 2447
                    },
                    "avgPointsFor": {
                      "value": 113.380950927734
                    },
                    "avgPointsAgainst": {
                      "value": 116.523811340332
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0.571428596973419
                    },
                    "divisionWins": {
                      "value": 4
                    },
                    "divisionLosses": {
                      "value": 2
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.666666686534882
                    },
                    "streak": {
                      "value": 3
                    },
                    "playoffSeed": {
                      "value": 9
                    },
                    "gamesBehind": {
                      "value": 11
                    },
                    "conferenceWins": {
                      "value": 8
                    },
                    "conferenceLosses": {
                      "value": 6
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 4
                    },
                    "homeLosses": {
                      "value": 6
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 6
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mem.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/mem.png"
                },
                {
                  "id": "24",
                  "guid": "8aef8547-32f5-0943-a1de-e734567674cc",
                  "uid": "s:40~l:46~t:24",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "San Antonio Spurs",
                  "name": "Spurs",
                  "abbreviation": "SA",
                  "location": "San Antonio",
                  "color": "000000",
                  "alternateColor": "c4ced4",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/sa/san-antonio-spurs",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/sa/san-antonio-spurs",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/sa/san-antonio-spurs",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/sa",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/sa",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/sa/san-antonio-spurs",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/sa",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/sa",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/sa",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "13-6",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 13
                    },
                    "losses": {
                      "value": 6
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 3.5
                    },
                    "pointsFor": {
                      "value": 2258
                    },
                    "pointsAgainst": {
                      "value": 2158
                    },
                    "avgPointsFor": {
                      "value": 118.842102050781
                    },
                    "avgPointsAgainst": {
                      "value": 113.578948974609
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.684210538864136
                    },
                    "leagueWinPercent": {
                      "value": 0.571428596973419
                    },
                    "divisionWins": {
                      "value": 5
                    },
                    "divisionLosses": {
                      "value": 0
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 1
                    },
                    "streak": {
                      "value": -1
                    },
                    "playoffSeed": {
                      "value": 5
                    },
                    "gamesBehind": {
                      "value": 6
                    },
                    "conferenceWins": {
                      "value": 8
                    },
                    "conferenceLosses": {
                      "value": 6
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 8
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 5
                    },
                    "roadLosses": {
                      "value": 4
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/sa.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/sa.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810177",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810178",
              "uid": "s:40~l:46~e:401810178~c:401810178",
              "guid": "33183167-96b4-3c45-b84e-9072247b9823",
              "date": "2025-12-03T04:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Oklahoma City Thunder at Golden State Warriors",
              "shortName": "OKC @ GS",
              "seriesSummary": "OKC leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810178/thunder-warriors",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/golden-state-warriors-tickets-chase-center-12-2-2025--sports-nba-basketball/production/5939871?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/chase-center-tickets/venue/23001?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810178",
              "location": "Chase Center",
              "season": 2026,
              "seasonStartDate": "2025-10-01T07:00:00Z",
              "seasonEndDate": "2026-04-13T06:59:00Z",
              "seasonType": "2",
              "seasonTypeHasGroups": false,
              "group": {
                "groupId": "2",
                "name": "Regular Season",
                "abbreviation": "reg",
                "shortName": "reg"
              },
              "week": 7,
              "weekText": "Week 7",
              "link": "https://www.espn.com/nba/game/_/gameId/401810178/thunder-warriors",
              "status": "pre",
              "summary": "12/2 - 11:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": true,
                  "broadcasterId": 379,
                  "broadcastId": 379,
                  "name": "NBC",
                  "shortName": "NBC",
                  "callLetters": "NBC",
                  "station": "NBC",
                  "lang": "en",
                  "region": "us",
                  "slug": "nbc"
                },
                {
                  "typeId": 1,
                  "priority": 3,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 890,
                  "broadcastId": 890,
                  "name": "NBC Sports Bay Area",
                  "shortName": "NBC Sports BA",
                  "callLetters": "NBC Sports BA",
                  "station": "NBC Sports BA",
                  "lang": "en",
                  "region": "us",
                  "slug": "nbc-sports-ba"
                },
                {
                  "typeId": 1,
                  "priority": 4,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 836,
                  "broadcastId": 836,
                  "name": "FanDuel Sports Network Oklahoma",
                  "shortName": "FanDuel SN OK",
                  "callLetters": "FanDuel SN OK",
                  "station": "FanDuel SN OK",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-ok"
                },
                {
                  "typeId": 4,
                  "priority": 2,
                  "type": "Streaming",
                  "isNational": true,
                  "broadcasterId": 789,
                  "broadcastId": 789,
                  "name": "Peacock",
                  "shortName": "Peacock",
                  "callLetters": "Peacock",
                  "station": "Peacock",
                  "lang": "en",
                  "region": "us",
                  "slug": "peacock"
                }
              ],
              "broadcast": "NBC/Peacock",
              "odds": {
                "details": "OKC -11.5",
                "overUnder": 223.5,
                "spread": 11.5,
                "overOdds": -110,
                "underOdds": -110,
                "provider": {
                  "id": "100",
                  "name": "Draft Kings",
                  "priority": 1,
                  "logos": [
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Light.svg",
                      "rel": [
                        "light"
                      ]
                    },
                    {
                      "href": "https://a.espncdn.com/i/betting/Draftkings_Dark.svg",
                      "rel": [
                        "dark"
                      ]
                    }
                  ]
                },
                "home": {
                  "moneyLine": 440
                },
                "away": {
                  "moneyLine": -600
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -600,
                  "spreadOdds": -112,
                  "team": {
                    "id": "25",
                    "abbreviation": "OKC",
                    "displayName": "Oklahoma City Thunder",
                    "name": "Thunder"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 440,
                  "spreadOdds": -108,
                  "team": {
                    "id": "9",
                    "abbreviation": "GS",
                    "displayName": "Golden State Warriors",
                    "name": "Warriors"
                  }
                },
                "links": [
                  {
                    "language": "en-US",
                    "rel": [
                      "game",
                      "desktop",
                      "bets"
                    ],
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982",
                    "text": "Game",
                    "shortText": "Game",
                    "isExternal": true,
                    "isPremium": false
                  }
                ],
                "pointSpread": {
                  "displayName": "Spread",
                  "shortDisplayName": "Spread",
                  "home": {
                    "open": {
                      "line": "+11.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+11.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0HC82432690P1150_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:GS+11.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-11.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-11.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0HC82432690N1150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:OKC-11.5"
                          }
                        }
                      }
                    }
                  }
                },
                "moneyline": {
                  "displayName": "Moneyline",
                  "shortDisplayName": "ML",
                  "home": {
                    "open": {
                      "odds": "+440"
                    },
                    "close": {
                      "odds": "+440",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0ML82432690_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-600"
                    },
                    "close": {
                      "odds": "-600",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0ML82432690_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "away",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  }
                },
                "total": {
                  "displayName": "Total",
                  "shortDisplayName": "Total",
                  "over": {
                    "open": {
                      "line": "o223.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o223.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0OU82432690O22350_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:223.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u223.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u223.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33229982%3Foutcomes%3D0OU82432690U22350_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810178,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:223.5"
                          }
                        }
                      }
                    }
                  }
                },
                "header": {
                  "logo": {
                    "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
                    "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
                    "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
                    "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
                  },
                  "text": "Game Odds"
                }
              },
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 0,
                "type": {
                  "id": "1",
                  "name": "STATUS_SCHEDULED",
                  "state": "pre",
                  "completed": false,
                  "description": "Scheduled",
                  "detail": "Tue, December 2nd at 11:00 PM EST",
                  "shortDetail": "12/2 - 11:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "25",
                  "guid": "bd458c44-2d33-47eb-cebc-35d3d4ac595c",
                  "uid": "s:40~l:46~t:25",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Oklahoma City Thunder",
                  "name": "Thunder",
                  "abbreviation": "OKC",
                  "location": "Oklahoma City",
                  "color": "007ac1",
                  "alternateColor": "ef3b24",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/okc/oklahoma-city-thunder",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/okc/oklahoma-city-thunder",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/okc/oklahoma-city-thunder",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/okc",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/okc",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/okc/oklahoma-city-thunder",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/okc",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/okc",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/okc",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "20-1",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 20
                    },
                    "losses": {
                      "value": 1
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 9.5
                    },
                    "pointsFor": {
                      "value": 2566
                    },
                    "pointsAgainst": {
                      "value": 2241
                    },
                    "avgPointsFor": {
                      "value": 122.190475463867
                    },
                    "avgPointsAgainst": {
                      "value": 106.714286804199
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.952380955219269
                    },
                    "leagueWinPercent": {
                      "value": 0.941176474094391
                    },
                    "divisionWins": {
                      "value": 4
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.800000011920929
                    },
                    "streak": {
                      "value": 12
                    },
                    "playoffSeed": {
                      "value": 1
                    },
                    "gamesBehind": {
                      "value": 0
                    },
                    "conferenceWins": {
                      "value": 16
                    },
                    "conferenceLosses": {
                      "value": 1
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 10
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 10
                    },
                    "roadLosses": {
                      "value": 1
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/okc.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/okc.png"
                },
                {
                  "id": "9",
                  "guid": "77a8546f-24bf-a333-8161-bf9f75396c49",
                  "uid": "s:40~l:46~t:9",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Golden State Warriors",
                  "name": "Warriors",
                  "abbreviation": "GS",
                  "location": "Golden State",
                  "color": "fdb927",
                  "alternateColor": "1d428a",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/gs/golden-state-warriors",
                      "text": "Clubhouse",
                      "shortText": "Clubhouse",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "roster",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/roster/_/name/gs/golden-state-warriors",
                      "text": "Roster",
                      "shortText": "Roster",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "stats",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/stats/_/name/gs/golden-state-warriors",
                      "text": "Statistics",
                      "shortText": "Statistics",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "schedule",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/schedule/_/name/gs",
                      "text": "Schedule",
                      "shortText": "Schedule",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "photos",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/photos/_/name/gs",
                      "text": "photos",
                      "shortText": "photos",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "draftpicks",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/draft/teams/_/name/gs/golden-state-warriors",
                      "text": "Draft Picks",
                      "shortText": "Draft Picks",
                      "isExternal": false,
                      "isPremium": true,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "transactions",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/transactions/_/name/gs",
                      "text": "Transactions",
                      "shortText": "Transactions",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "injuries",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/injuries/_/name/gs",
                      "text": "Injuries",
                      "shortText": "Injuries",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    },
                    {
                      "language": "en-US",
                      "rel": [
                        "depthchart",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/depth/_/name/gs",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "11-10",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 11
                    },
                    "losses": {
                      "value": 10
                    },
                    "ties": {
                      "value": 0
                    },
                    "OTWins": {
                      "value": 0
                    },
                    "OTLosses": {
                      "value": 0
                    },
                    "points": {
                      "value": 0.5
                    },
                    "pointsFor": {
                      "value": 2405
                    },
                    "pointsAgainst": {
                      "value": 2385
                    },
                    "avgPointsFor": {
                      "value": 114.523811340332
                    },
                    "avgPointsAgainst": {
                      "value": 113.571426391602
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.523809552192688
                    },
                    "leagueWinPercent": {
                      "value": 0.625
                    },
                    "divisionWins": {
                      "value": 3
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.75
                    },
                    "streak": {
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 8
                    },
                    "gamesBehind": {
                      "value": 9
                    },
                    "conferenceWins": {
                      "value": 10
                    },
                    "conferenceLosses": {
                      "value": 6
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 7
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 4
                    },
                    "roadLosses": {
                      "value": 8
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/gs.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/gs.png"
                }
              ],
              "neutralSite": false,
              "onDisneyNetwork": false,
              "appLinks": [
                {
                  "rel": [
                    "summary",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810178",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```