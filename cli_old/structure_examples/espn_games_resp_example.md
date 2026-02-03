# URL
https://site.web.api.espn.com/apis/personalized/v2/scoreboard/header?sport=basketball&league=nba&region=us&lang=en&contentorigin=espn&dates={YYYYMMDD}&tz=America%2FNew_York

# Response
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
            "2025-11-30T08:00Z",
            "2025-12-01T08:00Z",
            "2025-12-02T08:00Z"
          ],
          "events": [
            {
              "id": "401810164",
              "uid": "s:40~l:46~e:401810164~c:401810164",
              "guid": "3084da0b-5b13-3b85-bc27-460cd6511e9f",
              "date": "2025-12-02T00:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Atlanta Hawks at Detroit Pistons",
              "shortName": "ATL @ DET",
              "seriesSummary": "DET leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810164/hawks-pistons",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/detroit-pistons-tickets-little-caesars-arena-12-1-2025--sports-nba-basketball/production/5939762?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/little-caesars-arena-tickets/venue/16388?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810164",
              "location": "Little Caesars Arena",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810164/hawks-pistons",
              "status": "pre",
              "summary": "12/1 - 7:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
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
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 825,
                  "broadcastId": 825,
                  "name": "FanDuel Sports Network Detroit",
                  "shortName": "FanDuel SN DET",
                  "callLetters": "FanDuel SN DET",
                  "station": "FanDuel SN DET",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-det"
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
                "details": "DET -10.5",
                "overUnder": 233.5,
                "spread": -10.5,
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
                  "moneyLine": -440
                },
                "away": {
                  "moneyLine": 340
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 340,
                  "spreadOdds": -115,
                  "team": {
                    "id": "1",
                    "abbreviation": "ATL",
                    "displayName": "Atlanta Hawks",
                    "name": "Hawks"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -440,
                  "spreadOdds": -105,
                  "team": {
                    "id": "8",
                    "abbreviation": "DET",
                    "displayName": "Detroit Pistons",
                    "name": "Pistons"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696",
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
                      "line": "-7.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-10.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0HC82419830N1050_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:DET-10.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+7.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+10.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0HC82419830P1050_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:ATL+10.5"
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
                      "odds": "-298"
                    },
                    "close": {
                      "odds": "-440",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0ML82419830_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+240"
                    },
                    "close": {
                      "odds": "+340",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0ML82419830_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
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
                      "line": "o233.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0OU82419830O23350_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:233.5"
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
                      "line": "u233.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224696%3Foutcomes%3D0OU82419830U23350_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810164,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:233.5"
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
                  "detail": "Mon, December 1st at 7:00 PM EST",
                  "shortDetail": "12/1 - 7:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "1",
                  "guid": "15096a54-f015-c987-5ec8-55afedf6272f",
                  "uid": "s:40~l:46~t:1",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Atlanta Hawks",
                  "name": "Hawks",
                  "abbreviation": "ATL",
                  "location": "Atlanta",
                  "color": "c8102e",
                  "alternateColor": "fdb927",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/atl/atlanta-hawks",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/atl/atlanta-hawks",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/atl/atlanta-hawks",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/atl",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/atl",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/atl/atlanta-hawks",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/atl",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/atl",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/atl",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "13-8",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 13
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
                      "value": 2.5
                    },
                    "pointsFor": {
                      "value": 2497
                    },
                    "pointsAgainst": {
                      "value": 2448
                    },
                    "avgPointsFor": {
                      "value": 118.904762268066
                    },
                    "avgPointsAgainst": {
                      "value": 116.571426391602
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.61904764175415
                    },
                    "leagueWinPercent": {
                      "value": 0.538461565971375
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
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 5
                    },
                    "gamesBehind": {
                      "value": 3.5
                    },
                    "conferenceWins": {
                      "value": 7
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
                      "value": 4
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 9
                    },
                    "roadLosses": {
                      "value": 4
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/atl.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/atl.png"
                },
                {
                  "id": "8",
                  "guid": "4e096981-dc02-51d0-3dcd-2468fcc1e22d",
                  "uid": "s:40~l:46~t:8",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Detroit Pistons",
                  "name": "Pistons",
                  "abbreviation": "DET",
                  "location": "Detroit",
                  "color": "1d428a",
                  "alternateColor": "c8102e",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/det/detroit-pistons",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/det/detroit-pistons",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/det/detroit-pistons",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/det",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/det",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/det/detroit-pistons",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/det",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/det",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/det",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "16-4",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 16
                    },
                    "losses": {
                      "value": 4
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
                      "value": 6
                    },
                    "pointsFor": {
                      "value": 2395
                    },
                    "pointsAgainst": {
                      "value": 2279
                    },
                    "avgPointsFor": {
                      "value": 119.75
                    },
                    "avgPointsAgainst": {
                      "value": 113.949996948242
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.800000011920929
                    },
                    "leagueWinPercent": {
                      "value": 0.75
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
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 1
                    },
                    "gamesBehind": {
                      "value": 0
                    },
                    "conferenceWins": {
                      "value": 12
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
                      "value": 8
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/det.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/det.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810164",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810165",
              "uid": "s:40~l:46~e:401810165~c:401810165",
              "guid": "bc2fbd65-c24e-3720-baba-95145581213f",
              "date": "2025-12-02T00:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Cleveland Cavaliers at Indiana Pacers",
              "shortName": "CLE @ IND",
              "seriesSummary": "CLE leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810165/cavaliers-pacers",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/indiana-pacers-tickets-gainbridge-fieldhouse-12-1-2025--sports-nba-basketball/production/5940413?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/gainbridge-fieldhouse-tickets/venue/9847?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810165",
              "location": "Bankers Life Fieldhouse",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810165/cavaliers-pacers",
              "status": "pre",
              "summary": "12/1 - 7:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 987,
                  "broadcastId": 987,
                  "name": "FanDuel Sports Network Ohio",
                  "shortName": "FanDuel SN OH",
                  "callLetters": "FanDuel SN OH",
                  "station": "FanDuel SN OH",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-oh"
                },
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 830,
                  "broadcastId": 830,
                  "name": "FanDuel Sports Network Indiana",
                  "shortName": "FanDuel SN IN",
                  "callLetters": "FanDuel SN IN",
                  "station": "FanDuel SN IN",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-in"
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
                "details": "CLE -5.5",
                "overUnder": 232.5,
                "spread": 5.5,
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
                  "moneyLine": 180
                },
                "away": {
                  "moneyLine": -218
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -218,
                  "spreadOdds": -105,
                  "team": {
                    "id": "5",
                    "abbreviation": "CLE",
                    "displayName": "Cleveland Cavaliers",
                    "name": "Cavaliers"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 180,
                  "spreadOdds": -115,
                  "team": {
                    "id": "11",
                    "abbreviation": "IND",
                    "displayName": "Indiana Pacers",
                    "name": "Pacers"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698",
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
                      "line": "+5.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+5.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0HC82419832P550_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:IND+5.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-5.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-5.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0HC82419832N550_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:CLE-5.5"
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
                      "odds": "+180"
                    },
                    "close": {
                      "odds": "+180",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0ML82419832_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-218"
                    },
                    "close": {
                      "odds": "-218",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0ML82419832_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
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
                      "line": "o233.5",
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
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0OU82419832O23250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
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
                      "line": "u233.5",
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
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224698%3Foutcomes%3D0OU82419832U23250_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810165,
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
                  "detail": "Mon, December 1st at 7:00 PM EST",
                  "shortDetail": "12/1 - 7:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "5",
                  "guid": "ec79ad1f-e6d2-7762-a2db-7fe97d35126b",
                  "uid": "s:40~l:46~t:5",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Cleveland Cavaliers",
                  "name": "Cavaliers",
                  "abbreviation": "CLE",
                  "location": "Cleveland",
                  "color": "860038",
                  "alternateColor": "bc945c",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/cle/cleveland-cavaliers",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/cle/cleveland-cavaliers",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/cle",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/cle",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/cle/cleveland-cavaliers",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/cle",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/cle",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/cle",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "12-9",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 12
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
                      "value": 1.5
                    },
                    "pointsFor": {
                      "value": 2495
                    },
                    "pointsAgainst": {
                      "value": 2428
                    },
                    "avgPointsFor": {
                      "value": 118.809524536133
                    },
                    "avgPointsAgainst": {
                      "value": 115.619049072266
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.571428596973419
                    },
                    "leagueWinPercent": {
                      "value": 0.555555582046509
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
                      "value": -3
                    },
                    "playoffSeed": {
                      "value": 7
                    },
                    "gamesBehind": {
                      "value": 4.5
                    },
                    "conferenceWins": {
                      "value": 10
                    },
                    "conferenceLosses": {
                      "value": 8
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 8
                    },
                    "homeLosses": {
                      "value": 4
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 4
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/cle.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/cle.png"
                },
                {
                  "id": "11",
                  "guid": "547fc042-3e02-4795-9637-9ab84322b625",
                  "uid": "s:40~l:46~t:11",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Indiana Pacers",
                  "name": "Pacers",
                  "abbreviation": "IND",
                  "location": "Indiana",
                  "color": "0c2340",
                  "alternateColor": "ffd520",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/ind/indiana-pacers",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/ind/indiana-pacers",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/ind/indiana-pacers",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/ind",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/ind",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/ind/indiana-pacers",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/ind",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/ind",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/ind",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "4-16",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 4
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
                      "value": -6
                    },
                    "pointsFor": {
                      "value": 2195
                    },
                    "pointsAgainst": {
                      "value": 2372
                    },
                    "avgPointsFor": {
                      "value": 109.75
                    },
                    "avgPointsAgainst": {
                      "value": 118.599998474121
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.200000002980232
                    },
                    "leagueWinPercent": {
                      "value": 0.272727280855179
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.200000002980232
                    },
                    "streak": {
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 13
                    },
                    "gamesBehind": {
                      "value": 12
                    },
                    "conferenceWins": {
                      "value": 3
                    },
                    "conferenceLosses": {
                      "value": 8
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
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 10
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/ind.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/ind.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810165",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810166",
              "uid": "s:40~l:46~e:401810166~c:401810166",
              "guid": "3ae4acee-4a6d-33d0-8a7f-3cfe1950e792",
              "date": "2025-12-02T00:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Milwaukee Bucks at Washington Wizards",
              "shortName": "MIL @ WSH",
              "seriesSummary": "MIL leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810166/bucks-wizards",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/washington-wizards-tickets-capital-one-arena-12-1-2025--sports-nba-basketball/production/5939976?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/capital-one-arena-tickets/venue/1034?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810166",
              "location": "Capital One Arena",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810166/bucks-wizards",
              "status": "pre",
              "summary": "12/1 - 7:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 846,
                  "broadcastId": 846,
                  "name": "FanDuel Sports Network Wisconsin",
                  "shortName": "FanDuel SN WI",
                  "callLetters": "FanDuel SN WI",
                  "station": "FanDuel SN WI",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-wi"
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
                "details": "MIL -9.5",
                "overUnder": 232.5,
                "spread": 9.5,
                "overOdds": -105,
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
                  "moneyLine": 320
                },
                "away": {
                  "moneyLine": -410
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -410,
                  "spreadOdds": -112,
                  "team": {
                    "id": "15",
                    "abbreviation": "MIL",
                    "displayName": "Milwaukee Bucks",
                    "name": "Bucks"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 320,
                  "spreadOdds": -108,
                  "team": {
                    "id": "27",
                    "abbreviation": "WSH",
                    "displayName": "Washington Wizards",
                    "name": "Wizards"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700",
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
                      "line": "+9.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+9.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0HC82419834P950_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:WSH+9.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-9.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-9.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0HC82419834N950_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:MIL-9.5"
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
                      "odds": "+330"
                    },
                    "close": {
                      "odds": "+320",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0ML82419834_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-425"
                    },
                    "close": {
                      "odds": "-410",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0ML82419834_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
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
                      "line": "o232.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0OU82419834O23250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
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
                      "line": "u237.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u232.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224700%3Foutcomes%3D0OU82419834U23150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810166,
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
                  "detail": "Mon, December 1st at 7:00 PM EST",
                  "shortDetail": "12/1 - 7:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "15",
                  "guid": "f59bbabc-eedb-9ad2-c5dd-9bcd9f450a2f",
                  "uid": "s:40~l:46~t:15",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Milwaukee Bucks",
                  "name": "Bucks",
                  "abbreviation": "MIL",
                  "location": "Milwaukee",
                  "color": "00471b",
                  "alternateColor": "eee1c6",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/mil/milwaukee-bucks",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/mil/milwaukee-bucks",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/mil/milwaukee-bucks",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/mil",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/mil",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/mil/milwaukee-bucks",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/mil",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/mil",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/mil",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "9-12",
                  "records": [],
                  "group": "2",
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
                      "value": 2425
                    },
                    "pointsAgainst": {
                      "value": 2471
                    },
                    "avgPointsFor": {
                      "value": 115.476188659668
                    },
                    "avgPointsAgainst": {
                      "value": 117.666664123535
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0.466666668653488
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 3
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.400000005960465
                    },
                    "streak": {
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 11
                    },
                    "gamesBehind": {
                      "value": 7.5
                    },
                    "conferenceWins": {
                      "value": 7
                    },
                    "conferenceLosses": {
                      "value": 8
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 6
                    },
                    "homeLosses": {
                      "value": 6
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 3
                    },
                    "roadLosses": {
                      "value": 6
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mil.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/mil.png"
                },
                {
                  "id": "27",
                  "guid": "64d73af6-b8ec-e213-87e8-a4eab3a692e7",
                  "uid": "s:40~l:46~t:27",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
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
                  "record": "2-16",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 2
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
                      "value": -7
                    },
                    "pointsFor": {
                      "value": 2025
                    },
                    "pointsAgainst": {
                      "value": 2298
                    },
                    "avgPointsFor": {
                      "value": 112.5
                    },
                    "avgPointsAgainst": {
                      "value": 127.666664123535
                    },
                    "gamesPlayed": {
                      "value": 18
                    },
                    "winPercent": {
                      "value": 0.111111111938953
                    },
                    "leagueWinPercent": {
                      "value": 0.0769230797886848
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
                      "value": -1
                    },
                    "playoffSeed": {
                      "value": 15
                    },
                    "gamesBehind": {
                      "value": 13
                    },
                    "conferenceWins": {
                      "value": 1
                    },
                    "conferenceLosses": {
                      "value": 12
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 1
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810166",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810167",
              "uid": "s:40~l:46~e:401810167~c:401810167",
              "guid": "a25f30e4-bcec-34a3-86f4-1c3ac0750f06",
              "date": "2025-12-02T00:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Charlotte Hornets at Brooklyn Nets",
              "shortName": "CHA @ BKN",
              "seriesSummary": "CHA leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810167/hornets-nets",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/brooklyn-nets-tickets-barclays-center-12-1-2025--sports-nba-basketball/production/5939834?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/barclays-center-tickets/venue/9671?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810167",
              "location": "Barclays Center",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810167/hornets-nets",
              "status": "pre",
              "summary": "12/1 - 7:30 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 600,
                  "broadcastId": 600,
                  "name": "Yankees Entertainment and Sports Network",
                  "shortName": "YES",
                  "callLetters": "YES",
                  "station": "YES",
                  "lang": "en",
                  "region": "us",
                  "slug": "yes"
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
                "details": "CHA -4.5",
                "overUnder": 228.5,
                "spread": 4.5,
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
                  "moneyLine": 160
                },
                "away": {
                  "moneyLine": -192
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -192,
                  "spreadOdds": -110,
                  "team": {
                    "id": "30",
                    "abbreviation": "CHA",
                    "displayName": "Charlotte Hornets",
                    "name": "Hornets"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 160,
                  "spreadOdds": -110,
                  "team": {
                    "id": "17",
                    "abbreviation": "BKN",
                    "displayName": "Brooklyn Nets",
                    "name": "Nets"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701",
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
                      "line": "+4.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+4.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0HC82419835P450_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:BKN+4.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-4.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-4.5",
                      "odds": "-110",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0HC82419835N450_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:CHA-4.5"
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
                      "odds": "+154"
                    },
                    "close": {
                      "odds": "+160",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0ML82419835_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-185"
                    },
                    "close": {
                      "odds": "-192",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0ML82419835_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
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
                      "line": "o226.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o228.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0OU82419835O22850_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:228.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u226.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u228.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224701%3Foutcomes%3D0OU82419835U22850_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810167,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:228.5"
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
                  "detail": "Mon, December 1st at 7:30 PM EST",
                  "shortDetail": "12/1 - 7:30 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "30",
                  "guid": "377633c2-0dd1-91a1-83c0-9ed2d0c00ea1",
                  "uid": "s:40~l:46~t:30",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Charlotte Hornets",
                  "name": "Hornets",
                  "abbreviation": "CHA",
                  "location": "Charlotte",
                  "color": "008ca8",
                  "alternateColor": "1d1060",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/cha/charlotte-hornets",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/cha/charlotte-hornets",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/cha/charlotte-hornets",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/cha",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/cha",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/cha/charlotte-hornets",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/cha",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/cha",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/cha",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "6-14",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 6
                    },
                    "losses": {
                      "value": 14
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
                      "value": -4
                    },
                    "pointsFor": {
                      "value": 2317
                    },
                    "pointsAgainst": {
                      "value": 2403
                    },
                    "avgPointsFor": {
                      "value": 115.849998474121
                    },
                    "avgPointsAgainst": {
                      "value": 120.150001525879
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.300000011920929
                    },
                    "leagueWinPercent": {
                      "value": 0.357142865657806
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.200000002980232
                    },
                    "streak": {
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 12
                    },
                    "gamesBehind": {
                      "value": 10
                    },
                    "conferenceWins": {
                      "value": 5
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
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 8
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/cha.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/cha.png"
                },
                {
                  "id": "17",
                  "guid": "926db769-d35e-e282-9d7e-a05001d774ab",
                  "uid": "s:40~l:46~t:17",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Brooklyn Nets",
                  "name": "Nets",
                  "abbreviation": "BKN",
                  "location": "Brooklyn",
                  "color": "000000",
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
                      "href": "https://www.espn.com/nba/team/_/name/bkn/brooklyn-nets",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/bkn/brooklyn-nets",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/bkn/brooklyn-nets",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/bkn",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/bkn",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/bkn/brooklyn-nets",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/bkn",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/bkn",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/bkn",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "3-16",
                  "records": [],
                  "group": "1",
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
                      "value": 2059
                    },
                    "pointsAgainst": {
                      "value": 2266
                    },
                    "avgPointsFor": {
                      "value": 108.368423461914
                    },
                    "avgPointsAgainst": {
                      "value": 119.263160705566
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.157894730567932
                    },
                    "leagueWinPercent": {
                      "value": 0.1875
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 7
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.125
                    },
                    "streak": {
                      "value": -4
                    },
                    "playoffSeed": {
                      "value": 14
                    },
                    "gamesBehind": {
                      "value": 12.5
                    },
                    "conferenceWins": {
                      "value": 3
                    },
                    "conferenceLosses": {
                      "value": 13
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 0
                    },
                    "homeLosses": {
                      "value": 9
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 3
                    },
                    "roadLosses": {
                      "value": 7
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/bkn.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/bkn.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810167",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810168",
              "uid": "s:40~l:46~e:401810168~c:401810168",
              "guid": "08cc978d-a603-3b75-893d-9c9fec13d5d0",
              "date": "2025-12-02T00:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "LA Clippers at Miami Heat",
              "shortName": "LAC @ MIA",
              "seriesSummary": "MIA leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810168/clippers-heat",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/miami-heat-tickets-kaseya-center-12-1-2025--sports-nba-basketball/production/5939828?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/ftx-arena-tickets/venue/56?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810168",
              "location": "AmericanAirlines Are",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810168/clippers-heat",
              "status": "pre",
              "summary": "12/1 - 7:30 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 838,
                  "broadcastId": 838,
                  "name": "FanDuel Sports Network SoCal",
                  "shortName": "FanDuel SN SoCal",
                  "callLetters": "FanDuel SN SoCal",
                  "station": "FanDuel SN SoCal",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-socal"
                },
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 843,
                  "broadcastId": 843,
                  "name": "FanDuel Sports Network Sun",
                  "shortName": "FanDuel SN Sun",
                  "callLetters": "FanDuel SN Sun",
                  "station": "FanDuel SN Sun",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-sun"
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
                "details": "MIA -6.5",
                "overUnder": 235.5,
                "spread": -6.5,
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
                  "moneyLine": -245
                },
                "away": {
                  "moneyLine": 200
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 200,
                  "spreadOdds": -118,
                  "team": {
                    "id": "12",
                    "abbreviation": "LAC",
                    "displayName": "LA Clippers",
                    "name": "Clippers"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -245,
                  "spreadOdds": -102,
                  "team": {
                    "id": "14",
                    "abbreviation": "MIA",
                    "displayName": "Miami Heat",
                    "name": "Heat"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702",
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
                      "line": "-6.5",
                      "odds": "-102",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0HC82419836N650_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:MIA-6.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+5.5",
                      "odds": "-105"
                    },
                    "close": {
                      "line": "+6.5",
                      "odds": "-118",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0HC82419836P650_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:LAC+6.5"
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
                      "odds": "-245",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0ML82419836_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
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
                      "odds": "+200",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0ML82419836_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
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
                      "line": "o235.5",
                      "odds": "-115"
                    },
                    "close": {
                      "line": "o235.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0OU82419836O23550_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
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
                      "line": "u235.5",
                      "odds": "-105"
                    },
                    "close": {
                      "line": "u235.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224702%3Foutcomes%3D0OU82419836U23550_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810168,
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
                  "detail": "Mon, December 1st at 7:30 PM EST",
                  "shortDetail": "12/1 - 7:30 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "12",
                  "guid": "083a58a6-b849-3501-e67b-059290d12295",
                  "uid": "s:40~l:46~t:12",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "LA Clippers",
                  "name": "Clippers",
                  "abbreviation": "LAC",
                  "location": "LA",
                  "color": "12173f",
                  "alternateColor": "c8102e",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/lac/la-clippers",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/lac/la-clippers",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/lac/la-clippers",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/lac",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/lac",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/lac/la-clippers",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/lac",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/lac",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/lac",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "5-15",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 5
                    },
                    "losses": {
                      "value": 15
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
                      "value": -5
                    },
                    "pointsFor": {
                      "value": 2236
                    },
                    "pointsAgainst": {
                      "value": 2354
                    },
                    "avgPointsFor": {
                      "value": 111.800003051758
                    },
                    "avgPointsAgainst": {
                      "value": 117.699996948242
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.25
                    },
                    "leagueWinPercent": {
                      "value": 0.307692319154739
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.200000002980232
                    },
                    "streak": {
                      "value": -4
                    },
                    "playoffSeed": {
                      "value": 13
                    },
                    "gamesBehind": {
                      "value": 14.5
                    },
                    "conferenceWins": {
                      "value": 4
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
                      "value": 7
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 2
                    },
                    "roadLosses": {
                      "value": 8
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/lac.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/lac.png"
                },
                {
                  "id": "14",
                  "guid": "81e3212c-30ef-9b1b-5edb-453b13ff265a",
                  "uid": "s:40~l:46~t:14",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Miami Heat",
                  "name": "Heat",
                  "abbreviation": "MIA",
                  "location": "Miami",
                  "color": "98002e",
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
                      "href": "https://www.espn.com/nba/team/_/name/mia/miami-heat",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/mia/miami-heat",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/mia/miami-heat",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/mia",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/mia",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/mia/miami-heat",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/mia",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/mia",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/mia",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "13-7",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 13
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
                      "value": 3
                    },
                    "pointsFor": {
                      "value": 2471
                    },
                    "pointsAgainst": {
                      "value": 2364
                    },
                    "avgPointsFor": {
                      "value": 123.550003051758
                    },
                    "avgPointsAgainst": {
                      "value": 118.199996948242
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.649999976158142
                    },
                    "leagueWinPercent": {
                      "value": 0.666666686534882
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.666666686534882
                    },
                    "streak": {
                      "value": -1
                    },
                    "playoffSeed": {
                      "value": 4
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 8
                    },
                    "conferenceLosses": {
                      "value": 4
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 9
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
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mia.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/mia.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810168",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810169",
              "uid": "s:40~l:46~e:401810169~c:401810169",
              "guid": "124d33b5-2e8a-38ab-9848-454325a7070c",
              "date": "2025-12-02T00:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Chicago Bulls at Orlando Magic",
              "shortName": "CHI @ ORL",
              "seriesSummary": "CHI leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810169/bulls-magic",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/orlando-magic-tickets-kia-center-12-1-2025--sports-nba-basketball/production/5940356?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/amway-center-tickets/venue/8513?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810169",
              "location": "Amway Center",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810169/bulls-magic",
              "status": "pre",
              "summary": "12/1 - 7:30 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 828,
                  "broadcastId": 828,
                  "name": "FanDuel Sports Network Florida",
                  "shortName": "FanDuel SN FL",
                  "callLetters": "FanDuel SN FL",
                  "station": "FanDuel SN FL",
                  "lang": "en",
                  "region": "us",
                  "slug": "fanduel-sn-fl"
                },
                {
                  "typeId": 4,
                  "priority": 1,
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
              "broadcast": "Peacock",
              "odds": {
                "details": "ORL -8.5",
                "overUnder": 239.5,
                "spread": -8.5,
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
                  "moneyLine": -360
                },
                "away": {
                  "moneyLine": 285
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 285,
                  "spreadOdds": -108,
                  "team": {
                    "id": "4",
                    "abbreviation": "CHI",
                    "displayName": "Chicago Bulls",
                    "name": "Bulls"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -360,
                  "spreadOdds": -112,
                  "team": {
                    "id": "19",
                    "abbreviation": "ORL",
                    "displayName": "Orlando Magic",
                    "name": "Magic"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703",
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
                      "line": "-7.5",
                      "odds": "-105"
                    },
                    "close": {
                      "line": "-8.5",
                      "odds": "-112",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0HC82419837N850_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:ORL-8.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+7.5",
                      "odds": "-115"
                    },
                    "close": {
                      "line": "+8.5",
                      "odds": "-108",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0HC82419837P850_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:CHI+8.5"
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
                      "odds": "-290"
                    },
                    "close": {
                      "odds": "-360",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0ML82419837_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+235"
                    },
                    "close": {
                      "odds": "+285",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0ML82419837_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
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
                      "line": "o239.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o239.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0OU82419837O23950_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:239.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u239.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u239.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224703%3Foutcomes%3D0OU82419837U23950_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810169,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:239.5"
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
                  "detail": "Mon, December 1st at 7:30 PM EST",
                  "shortDetail": "12/1 - 7:30 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "4",
                  "guid": "e588ccf1-ba03-ea43-c34c-9a9c8d1895ca",
                  "uid": "s:40~l:46~t:4",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Chicago Bulls",
                  "name": "Bulls",
                  "abbreviation": "CHI",
                  "location": "Chicago",
                  "color": "ce1141",
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
                      "href": "https://www.espn.com/nba/team/_/name/chi/chicago-bulls",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/chi/chicago-bulls",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/chi/chicago-bulls",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/chi",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/chi",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/chi/chicago-bulls",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/chi",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/chi",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/chi",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "9-10",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 9
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 2279
                    },
                    "pointsAgainst": {
                      "value": 2338
                    },
                    "avgPointsFor": {
                      "value": 119.947364807129
                    },
                    "avgPointsAgainst": {
                      "value": 123.052635192871
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.473684221506119
                    },
                    "leagueWinPercent": {
                      "value": 0.461538463830948
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.200000002980232
                    },
                    "streak": {
                      "value": -3
                    },
                    "playoffSeed": {
                      "value": 10
                    },
                    "gamesBehind": {
                      "value": 6.5
                    },
                    "conferenceWins": {
                      "value": 6
                    },
                    "conferenceLosses": {
                      "value": 7
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 6
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 3
                    },
                    "roadLosses": {
                      "value": 8
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/chi.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/chi.png"
                },
                {
                  "id": "19",
                  "guid": "74c23102-8c27-c8e6-ec1b-8a8fd4d42554",
                  "uid": "s:40~l:46~t:19",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Orlando Magic",
                  "name": "Magic",
                  "abbreviation": "ORL",
                  "location": "Orlando",
                  "color": "0150b5",
                  "alternateColor": "9ca0a3",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/orl/orlando-magic",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/orl/orlando-magic",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/orl/orlando-magic",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/orl",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/orl",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/orl/orlando-magic",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/orl",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/orl",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/orl",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "12-8",
                  "records": [],
                  "group": "9",
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
                      "value": 2385
                    },
                    "pointsAgainst": {
                      "value": 2281
                    },
                    "avgPointsFor": {
                      "value": 119.25
                    },
                    "avgPointsAgainst": {
                      "value": 114.050003051758
                    },
                    "gamesPlayed": {
                      "value": 20
                    },
                    "winPercent": {
                      "value": 0.600000023841858
                    },
                    "leagueWinPercent": {
                      "value": 0.5625
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
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 6
                    },
                    "gamesBehind": {
                      "value": 4
                    },
                    "conferenceWins": {
                      "value": 9
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
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/orl.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/orl.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810169",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810170",
              "uid": "s:40~l:46~e:401810170~c:401810170",
              "guid": "28f32c01-50a4-3461-8b47-53c2232d9525",
              "date": "2025-12-02T02:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Dallas Mavericks at Denver Nuggets",
              "shortName": "DAL @ DEN",
              "seriesSummary": "Series starts 12/1",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810170/mavericks-nuggets",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/denver-nuggets-tickets-ball-arena-12-1-2025--sports-nba-basketball/production/5940630?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/ball-arena-tickets/venue/1315?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810170",
              "location": "Pepsi Center",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810170/mavericks-nuggets",
              "status": "pre",
              "summary": "12/1 - 9:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 1165,
                  "broadcastId": 1165,
                  "name": "KFAA-TV",
                  "shortName": "KFAA-TV",
                  "callLetters": "KFAA-TV",
                  "station": "KFAA-TV",
                  "lang": "en",
                  "region": "us",
                  "slug": "kfaa-tv"
                },
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 24,
                  "broadcastId": 24,
                  "name": "Altitude Sports",
                  "shortName": "Altitude Sports",
                  "callLetters": "Altitude Sports",
                  "station": "Altitude Sports",
                  "lang": "en",
                  "region": "us",
                  "slug": "altitude-sports"
                },
                {
                  "typeId": 4,
                  "priority": 3,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1085,
                  "broadcastId": 1085,
                  "name": "Mavs.com",
                  "shortName": "Mavs.com",
                  "callLetters": "Mavs.com",
                  "station": "Mavs.com",
                  "lang": "en",
                  "region": "us",
                  "slug": "mavscom"
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
                "details": "DEN -11.5",
                "overUnder": 233.5,
                "spread": -11.5,
                "overOdds": -115,
                "underOdds": -105,
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
                  "moneyLine": -520
                },
                "away": {
                  "moneyLine": 390
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 390,
                  "spreadOdds": -115,
                  "team": {
                    "id": "6",
                    "abbreviation": "DAL",
                    "displayName": "Dallas Mavericks",
                    "name": "Mavericks"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -520,
                  "spreadOdds": -105,
                  "team": {
                    "id": "7",
                    "abbreviation": "DEN",
                    "displayName": "Denver Nuggets",
                    "name": "Nuggets"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704",
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
                      "line": "-10.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-11.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0HC82419838N1150_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:DEN-11.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+10.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+11.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0HC82419838P1150_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:DAL+11.5"
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
                      "odds": "-455"
                    },
                    "close": {
                      "odds": "-520",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0ML82419838_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+350"
                    },
                    "close": {
                      "odds": "+390",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0ML82419838_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
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
                      "line": "o234.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o233.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0OU82419838O23350_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:233.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u234.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u233.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224704%3Foutcomes%3D0OU82419838U23350_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810170,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:233.5"
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
                  "detail": "Mon, December 1st at 9:00 PM EST",
                  "shortDetail": "12/1 - 9:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "6",
                  "guid": "f00d1f4e-4ce6-d581-466c-5b52531cf7ad",
                  "uid": "s:40~l:46~t:6",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Dallas Mavericks",
                  "name": "Mavericks",
                  "abbreviation": "DAL",
                  "location": "Dallas",
                  "color": "0064b1",
                  "alternateColor": "bbc4ca",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/dal/dallas-mavericks",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/dal/dallas-mavericks",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/dal/dallas-mavericks",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/dal",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/dal",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/dal/dallas-mavericks",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/dal",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/dal",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/dal",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "6-15",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 6
                    },
                    "losses": {
                      "value": 15
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
                      "value": -4.5
                    },
                    "pointsFor": {
                      "value": 2314
                    },
                    "pointsAgainst": {
                      "value": 2433
                    },
                    "avgPointsFor": {
                      "value": 110.190475463867
                    },
                    "avgPointsAgainst": {
                      "value": 115.857139587402
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.28571429848671
                    },
                    "leagueWinPercent": {
                      "value": 0.230769231915474
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
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 12
                    },
                    "gamesBehind": {
                      "value": 14
                    },
                    "conferenceWins": {
                      "value": 3
                    },
                    "conferenceLosses": {
                      "value": 10
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 4
                    },
                    "homeLosses": {
                      "value": 9
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 2
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/dal.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/dal.png"
                },
                {
                  "id": "7",
                  "guid": "c4aceb39-0eb9-a30b-1120-9cb5b12b677a",
                  "uid": "s:40~l:46~t:7",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Denver Nuggets",
                  "name": "Nuggets",
                  "abbreviation": "DEN",
                  "location": "Denver",
                  "color": "0e2240",
                  "alternateColor": "fec524",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/den/denver-nuggets",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/den/denver-nuggets",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/den/denver-nuggets",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/den",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/den",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/den/denver-nuggets",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/den",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/den",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/den",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "14-5",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 14
                    },
                    "losses": {
                      "value": 5
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
                      "value": 4.5
                    },
                    "pointsFor": {
                      "value": 2371
                    },
                    "pointsAgainst": {
                      "value": 2186
                    },
                    "avgPointsFor": {
                      "value": 124.789474487305
                    },
                    "avgPointsAgainst": {
                      "value": 115.052635192871
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.736842095851898
                    },
                    "leagueWinPercent": {
                      "value": 0.75
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.666666686534882
                    },
                    "streak": {
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 4
                    },
                    "gamesBehind": {
                      "value": 5
                    },
                    "conferenceWins": {
                      "value": 12
                    },
                    "conferenceLosses": {
                      "value": 4
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 6
                    },
                    "homeLosses": {
                      "value": 3
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 8
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/den.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/den.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810170",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810171",
              "uid": "s:40~l:46~e:401810171~c:401810171",
              "guid": "29aa78f2-edda-3d19-bab8-44f86a96b3bf",
              "date": "2025-12-02T02:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Houston Rockets at Utah Jazz",
              "shortName": "HOU @ UTAH",
              "seriesSummary": "HOU leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810171/rockets-jazz",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/utah-jazz-tickets-delta-center-12-1-2025--sports-nba-basketball/production/5939935?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/vivint-smart-home-arena-tickets/venue/459?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810171",
              "location": "Vivint Arena",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810171/rockets-jazz",
              "status": "pre",
              "summary": "12/1 - 9:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 962,
                  "broadcastId": 962,
                  "name": "Space City Home Network",
                  "shortName": "Space City Home Network",
                  "callLetters": "Space City Home Network",
                  "station": "Space City Home Network",
                  "lang": "en",
                  "region": "us",
                  "slug": "space-city-home-network"
                },
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 867,
                  "broadcastId": 867,
                  "name": "KJZZ-TV",
                  "shortName": "KJZZ-TV",
                  "callLetters": "KJZZ-TV",
                  "station": "KJZZ-TV",
                  "lang": "en",
                  "region": "us",
                  "slug": "kjzz-tv"
                },
                {
                  "typeId": 4,
                  "priority": 3,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1107,
                  "broadcastId": 1107,
                  "name": "Jazz+",
                  "shortName": "Jazz+",
                  "callLetters": "Jazz+",
                  "station": "Jazz+",
                  "lang": "en",
                  "region": "us",
                  "slug": "jazzplus"
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
                "details": "HOU -12.5",
                "overUnder": 232.5,
                "spread": 12.5,
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
                  "moneyLine": 470
                },
                "away": {
                  "moneyLine": -650
                },
                "awayTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -650,
                  "spreadOdds": -105,
                  "team": {
                    "id": "10",
                    "abbreviation": "HOU",
                    "displayName": "Houston Rockets",
                    "name": "Rockets"
                  }
                },
                "homeTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": false,
                  "moneyLine": 470,
                  "spreadOdds": -115,
                  "team": {
                    "id": "26",
                    "abbreviation": "UTAH",
                    "displayName": "Utah Jazz",
                    "name": "Jazz"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705",
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
                      "line": "+12.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+12.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0HC82419839P1250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:UTAH+12.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "-12.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-12.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0HC82419839N1250_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:HOU-12.5"
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
                      "odds": "+455"
                    },
                    "close": {
                      "odds": "+470",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0ML82419839_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "-625"
                    },
                    "close": {
                      "odds": "-650",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0ML82419839_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
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
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0OU82419839O23250_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
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
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224705%3Foutcomes%3D0OU82419839U23250_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810171,
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
                  "detail": "Mon, December 1st at 9:00 PM EST",
                  "shortDetail": "12/1 - 9:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "10",
                  "guid": "78113ad4-1ac7-0c04-dada-388a6ff4e15e",
                  "uid": "s:40~l:46~t:10",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Houston Rockets",
                  "name": "Rockets",
                  "abbreviation": "HOU",
                  "location": "Houston",
                  "color": "ce1141",
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
                      "href": "https://www.espn.com/nba/team/_/name/hou/houston-rockets",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/hou/houston-rockets",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/hou/houston-rockets",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/hou",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/hou",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/hou/houston-rockets",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/hou",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/hou",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/hou",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "13-4",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 13
                    },
                    "losses": {
                      "value": 4
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
                      "value": 4.5
                    },
                    "pointsFor": {
                      "value": 2067
                    },
                    "pointsAgainst": {
                      "value": 1868
                    },
                    "avgPointsFor": {
                      "value": 121.588233947754
                    },
                    "avgPointsAgainst": {
                      "value": 109.882354736328
                    },
                    "gamesPlayed": {
                      "value": 17
                    },
                    "winPercent": {
                      "value": 0.764705896377564
                    },
                    "leagueWinPercent": {
                      "value": 0.666666686534882
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 1
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
                      "value": 3
                    },
                    "gamesBehind": {
                      "value": 5
                    },
                    "conferenceWins": {
                      "value": 6
                    },
                    "conferenceLosses": {
                      "value": 3
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 5
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 8
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/hou.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/hou.png"
                },
                {
                  "id": "26",
                  "guid": "77cea2fb-1388-b7c8-d171-2e72b3aecbfb",
                  "uid": "s:40~l:46~t:26",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Utah Jazz",
                  "name": "Jazz",
                  "abbreviation": "UTAH",
                  "location": "Utah",
                  "color": "4e008e",
                  "alternateColor": "79a3dc",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/utah/utah-jazz",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/utah/utah-jazz",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/utah/utah-jazz",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/utah",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/utah",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/utah/utah-jazz",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/utah",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/utah",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/utah",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "6-13",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 6
                    },
                    "losses": {
                      "value": 13
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
                      "value": -3.5
                    },
                    "pointsFor": {
                      "value": 2235
                    },
                    "pointsAgainst": {
                      "value": 2382
                    },
                    "avgPointsFor": {
                      "value": 117.631576538086
                    },
                    "avgPointsAgainst": {
                      "value": 125.368423461914
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.315789461135864
                    },
                    "leagueWinPercent": {
                      "value": 0.230769231915474
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 4
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": -1
                    },
                    "playoffSeed": {
                      "value": 11
                    },
                    "gamesBehind": {
                      "value": 13
                    },
                    "conferenceWins": {
                      "value": 3
                    },
                    "conferenceLosses": {
                      "value": 10
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
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 7
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/utah.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/utah.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810171",
                  "text": "Gamecast",
                  "shortText": "Summary"
                }
              ]
            },
            {
              "id": "401810172",
              "uid": "s:40~l:46~e:401810172~c:401810172",
              "guid": "0b38ab23-fab7-3264-8141-5cca954d4230",
              "date": "2025-12-02T03:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Phoenix Suns at Los Angeles Lakers",
              "shortName": "PHX @ LAL",
              "seriesSummary": "Series starts 12/1",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810172/suns-lakers",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.vividseats.com/los-angeles-lakers-tickets-cryptocom-arena-12-1-2025--sports-nba-basketball/production/5939671?wsUser=717",
                  "text": "Tickets"
                },
                {
                  "rel": [
                    "tickets",
                    "desktop",
                    "venue"
                  ],
                  "href": "https://www.vividseats.com/crypto-arena-tickets/venue/1604?wsUser=717",
                  "text": "Tickets"
                }
              ],
              "gamecastAvailable": false,
              "playByPlayAvailable": false,
              "commentaryAvailable": false,
              "wallclockAvailable": false,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810172",
              "location": "Staples Center",
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
              "week": 6,
              "weekText": "Week 6",
              "link": "https://www.espn.com/nba/game/_/gameId/401810172/suns-lakers",
              "status": "pre",
              "summary": "12/1 - 10:00 PM EST",
              "period": 0,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 2,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 912,
                  "broadcastId": 912,
                  "name": "Spectrum Sports Network",
                  "shortName": "Spectrum Sports Net",
                  "callLetters": "Spectrum Sports Net",
                  "station": "Spectrum Sports Net",
                  "lang": "en",
                  "region": "us",
                  "slug": "spectrum-sports-net"
                },
                {
                  "typeId": 4,
                  "priority": 1,
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
                },
                {
                  "typeId": 4,
                  "priority": 3,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1175,
                  "broadcastId": 1175,
                  "name": "Spectrum Sports Net +",
                  "shortName": "Spectrum Sports Net +",
                  "callLetters": "Spectrum Sports Net +",
                  "station": "Spectrum Sports Net +",
                  "lang": "en",
                  "region": "us",
                  "slug": "spectrum-sports-net-plus"
                }
              ],
              "broadcast": "Peacock",
              "odds": {
                "details": "LAL -4.5",
                "overUnder": 234.5,
                "spread": -4.5,
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
                  "moneyLine": -198
                },
                "away": {
                  "moneyLine": 164
                },
                "awayTeamOdds": {
                  "favorite": false,
                  "favoriteAtOpen": false,
                  "underdog": true,
                  "moneyLine": 164,
                  "spreadOdds": -105,
                  "team": {
                    "id": "21",
                    "abbreviation": "PHX",
                    "displayName": "Phoenix Suns",
                    "name": "Suns"
                  }
                },
                "homeTeamOdds": {
                  "favorite": true,
                  "favoriteAtOpen": true,
                  "underdog": false,
                  "moneyLine": -198,
                  "spreadOdds": -115,
                  "team": {
                    "id": "13",
                    "abbreviation": "LAL",
                    "displayName": "Los Angeles Lakers",
                    "name": "Lakers"
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
                    "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706",
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
                      "line": "-6.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "-4.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "homeSpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0HC82419840N450_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
                            "betSide": "home",
                            "betType": "straight",
                            "betDetails": "Spread:LAL-4.5"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "line": "+6.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "+4.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "awaySpread",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0HC82419840P450_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
                            "betSide": "away",
                            "betType": "straight",
                            "betDetails": "Spread:PHX+4.5"
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
                      "odds": "-245"
                    },
                    "close": {
                      "odds": "-198",
                      "link": {
                        "rel": [
                          "home",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0ML82419840_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
                            "betSide": "home",
                            "betType": "straight"
                          }
                        }
                      }
                    }
                  },
                  "away": {
                    "open": {
                      "odds": "+200"
                    },
                    "close": {
                      "odds": "+164",
                      "link": {
                        "rel": [
                          "away",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0ML82419840_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
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
                      "line": "o234.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "o234.5",
                      "odds": "-105",
                      "link": {
                        "rel": [
                          "over",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0OU82419840O23450_1",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
                            "betSide": "over",
                            "betType": "straight",
                            "betDetails": "Over:234.5"
                          }
                        }
                      }
                    }
                  },
                  "under": {
                    "open": {
                      "line": "u234.5",
                      "odds": "-110"
                    },
                    "close": {
                      "line": "u234.5",
                      "odds": "-115",
                      "link": {
                        "rel": [
                          "under",
                          "bets"
                        ],
                        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33224706%3Foutcomes%3D0OU82419840U23450_3",
                        "tracking": {
                          "campaign": "betting-integrations",
                          "tags": {
                            "league": "nba",
                            "sport": "basketball",
                            "gameId": 401810172,
                            "betSide": "under",
                            "betType": "straight",
                            "betDetails": "Under:234.5"
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
                  "detail": "Mon, December 1st at 10:00 PM EST",
                  "shortDetail": "12/1 - 10:00 PM EST"
                }
              },
              "competitors": [
                {
                  "id": "21",
                  "guid": "c6eade89-5971-0e84-8ccb-cd91482b2b50",
                  "uid": "s:40~l:46~t:21",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Phoenix Suns",
                  "name": "Suns",
                  "abbreviation": "PHX",
                  "location": "Phoenix",
                  "color": "29127a",
                  "alternateColor": "e56020",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/phx/phoenix-suns",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/phx/phoenix-suns",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/phx/phoenix-suns",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/phx",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/phx",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/phx/phoenix-suns",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/phx",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/phx",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/phx",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "12-9",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 12
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
                      "value": 1.5
                    },
                    "pointsFor": {
                      "value": 2450
                    },
                    "pointsAgainst": {
                      "value": 2393
                    },
                    "avgPointsFor": {
                      "value": 116.666664123535
                    },
                    "avgPointsAgainst": {
                      "value": 113.952377319336
                    },
                    "gamesPlayed": {
                      "value": 21
                    },
                    "winPercent": {
                      "value": 0.571428596973419
                    },
                    "leagueWinPercent": {
                      "value": 0.578947365283966
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
                      "value": -2
                    },
                    "playoffSeed": {
                      "value": 7
                    },
                    "gamesBehind": {
                      "value": 8
                    },
                    "conferenceWins": {
                      "value": 11
                    },
                    "conferenceLosses": {
                      "value": 8
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 8
                    },
                    "homeLosses": {
                      "value": 4
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 4
                    },
                    "roadLosses": {
                      "value": 5
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phx.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/phx.png"
                },
                {
                  "id": "13",
                  "guid": "2876e98b-b9bc-2920-4319-46e6943f8be4",
                  "uid": "s:40~l:46~t:13",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": false,
                  "displayName": "Los Angeles Lakers",
                  "name": "Lakers",
                  "abbreviation": "LAL",
                  "location": "Los Angeles",
                  "color": "552583",
                  "alternateColor": "fdb927",
                  "score": "",
                  "links": [
                    {
                      "language": "en-US",
                      "rel": [
                        "clubhouse",
                        "desktop",
                        "team"
                      ],
                      "href": "https://www.espn.com/nba/team/_/name/lal/los-angeles-lakers",
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
                      "href": "https://www.espn.com/nba/team/roster/_/name/lal/los-angeles-lakers",
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
                      "href": "https://www.espn.com/nba/team/stats/_/name/lal/los-angeles-lakers",
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
                      "href": "https://www.espn.com/nba/team/schedule/_/name/lal",
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
                      "href": "https://www.espn.com/nba/team/photos/_/name/lal",
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
                      "href": "https://www.espn.com/nba/draft/teams/_/name/lal/los-angeles-lakers",
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
                      "href": "https://www.espn.com/nba/team/transactions/_/name/lal",
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
                      "href": "https://www.espn.com/nba/team/injuries/_/name/lal",
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
                      "href": "https://www.espn.com/nba/team/depth/_/name/lal",
                      "text": "Depth Chart",
                      "shortText": "Depth Chart",
                      "isExternal": false,
                      "isPremium": false,
                      "isHidden": false
                    }
                  ],
                  "record": "15-4",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 15
                    },
                    "losses": {
                      "value": 4
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
                      "value": 5.5
                    },
                    "pointsFor": {
                      "value": 2273
                    },
                    "pointsAgainst": {
                      "value": 2191
                    },
                    "avgPointsFor": {
                      "value": 119.631576538086
                    },
                    "avgPointsAgainst": {
                      "value": 115.315788269043
                    },
                    "gamesPlayed": {
                      "value": 19
                    },
                    "winPercent": {
                      "value": 0.789473712444305
                    },
                    "leagueWinPercent": {
                      "value": 0.800000011920929
                    },
                    "divisionWins": {
                      "value": 2
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.666666686534882
                    },
                    "streak": {
                      "value": 7
                    },
                    "playoffSeed": {
                      "value": 2
                    },
                    "gamesBehind": {
                      "value": 4
                    },
                    "conferenceWins": {
                      "value": 12
                    },
                    "conferenceLosses": {
                      "value": 3
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
                      "value": 8
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/lal.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/lal.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810172",
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