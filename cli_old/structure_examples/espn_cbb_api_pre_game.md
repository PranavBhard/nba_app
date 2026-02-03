# URL
https://site.web.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?region=us&lang=en&contentorigin=espn&event={game_id}

# Response Example
```json
{
  "boxscore": {
    "teams": [
      {
        "team": {
          "id": "154",
          "uid": "s:40~l:41~t:154",
          "slug": "wake-forest-demon-deacons",
          "location": "Wake Forest",
          "name": "Demon Deacons",
          "abbreviation": "WAKE",
          "displayName": "Wake Forest Demon Deacons",
          "shortDisplayName": "Wake Forest",
          "color": "ceb888",
          "alternateColor": "2c2a29",
          "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png"
        },
        "statistics": [
          {
            "name": "streak",
            "displayValue": "L1",
            "abbreviation": "STRK",
            "label": "Streak"
          },
          {
            "name": "avgPointsAgainst",
            "displayValue": "75.8",
            "abbreviation": "OPP PPG",
            "label": "Points Against"
          },
          {
            "name": "avgPoints",
            "displayValue": "80.9",
            "abbreviation": "PTS",
            "label": "Points Per Game"
          },
          {
            "name": "fieldGoalPct",
            "displayValue": "45",
            "abbreviation": "FG%",
            "label": "Field Goal %"
          },
          {
            "name": "threePointFieldGoalPct",
            "displayValue": "33",
            "abbreviation": "3P%",
            "label": "Three Point %"
          },
          {
            "name": "avgRebounds",
            "displayValue": "33.9",
            "abbreviation": "REB",
            "label": "Rebounds Per Game"
          },
          {
            "name": "avgAssists",
            "displayValue": "15.1",
            "abbreviation": "AST",
            "label": "Assists Per Game"
          },
          {
            "name": "avgBlocks",
            "displayValue": "3.5",
            "abbreviation": "BLK",
            "label": "Blocks Per Game"
          },
          {
            "name": "avgSteals",
            "displayValue": "9.5",
            "abbreviation": "STL",
            "label": "Steals Per Game"
          },
          {
            "name": "avgTeamTurnovers",
            "displayValue": "0.4",
            "abbreviation": "TTO",
            "label": "Team Turnovers Per Game"
          },
          {
            "name": "avgTotalTurnovers",
            "displayValue": "12.3",
            "abbreviation": "ToTO",
            "label": "Total Turnovers Per Game"
          },
          {
            "name": "avgPointsAgainst",
            "displayValue": "75.8",
            "abbreviation": "PA",
            "label": "Points Against"
          }
        ],
        "displayOrder": 1,
        "homeAway": "away"
      },
      {
        "team": {
          "id": "150",
          "uid": "s:40~l:41~t:150",
          "slug": "duke-blue-devils",
          "location": "Duke",
          "name": "Blue Devils",
          "abbreviation": "DUKE",
          "displayName": "Duke Blue Devils",
          "shortDisplayName": "Duke",
          "color": "00539b",
          "alternateColor": "ffffff",
          "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png"
        },
        "statistics": [
          {
            "name": "streak",
            "displayValue": "W6",
            "abbreviation": "STRK",
            "label": "Streak"
          },
          {
            "name": "avgPointsAgainst",
            "displayValue": "65.1",
            "abbreviation": "OPP PPG",
            "label": "Points Against"
          },
          {
            "name": "avgPoints",
            "displayValue": "85.5",
            "abbreviation": "PTS",
            "label": "Points Per Game"
          },
          {
            "name": "fieldGoalPct",
            "displayValue": "50",
            "abbreviation": "FG%",
            "label": "Field Goal %"
          },
          {
            "name": "threePointFieldGoalPct",
            "displayValue": "35",
            "abbreviation": "3P%",
            "label": "Three Point %"
          },
          {
            "name": "avgRebounds",
            "displayValue": "40.0",
            "abbreviation": "REB",
            "label": "Rebounds Per Game"
          },
          {
            "name": "avgAssists",
            "displayValue": "17.6",
            "abbreviation": "AST",
            "label": "Assists Per Game"
          },
          {
            "name": "avgBlocks",
            "displayValue": "4.2",
            "abbreviation": "BLK",
            "label": "Blocks Per Game"
          },
          {
            "name": "avgSteals",
            "displayValue": "8.6",
            "abbreviation": "STL",
            "label": "Steals Per Game"
          },
          {
            "name": "avgTeamTurnovers",
            "displayValue": "0.1",
            "abbreviation": "TTO",
            "label": "Team Turnovers Per Game"
          },
          {
            "name": "avgTotalTurnovers",
            "displayValue": "11.6",
            "abbreviation": "ToTO",
            "label": "Total Turnovers Per Game"
          },
          {
            "name": "avgPointsAgainst",
            "displayValue": "65.1",
            "abbreviation": "PA",
            "label": "Points Against"
          }
        ],
        "displayOrder": 2,
        "homeAway": "home"
      }
    ]
  },
  "format": {
    "regulation": {
      "periods": 2,
      "displayName": "Half",
      "slug": "half",
      "clock": 1200
    },
    "overtime": {
      "clock": 300
    }
  },
  "gameInfo": {
    "venue": {
      "id": "1914",
      "guid": "0eb1127f-0db1-3c30-8a67-8abcee08d463",
      "fullName": "Cameron Indoor Stadium",
      "address": {
        "city": "Durham",
        "state": "NC"
      },
      "grass": false,
      "images": [
        {
          "href": "https://a.espncdn.com/i/venues/mens-college-basketball/day/1914.jpg",
          "width": 2000,
          "height": 1125,
          "alt": "",
          "rel": [
            "full",
            "day"
          ]
        }
      ]
    }
  },
  "lastFiveGames": [
    {
      "displayOrder": 2,
      "team": {
        "id": "150",
        "uid": "s:40~l:41~t:150",
        "displayName": "Duke Blue Devils",
        "abbreviation": "DUKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/150",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2026-01-05T20:04Z"
          }
        ]
      },
      "events": [
        {
          "id": "401820644",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820644/duke-florida-st",
              "text": "Gamecast"
            }
          ],
          "week": 9,
          "atVs": "@",
          "gameDate": "2026-01-03T20:45Z",
          "score": "91-87",
          "homeTeamId": "52",
          "awayTeamId": "150",
          "homeTeamScore": "87",
          "awayTeamScore": "91",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "opponent": {
            "id": "52",
            "uid": "s:40~l:41~t:52",
            "displayName": "Florida State Seminoles",
            "abbreviation": "FSU",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/52/florida-state-seminoles",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/52",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/52.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM"
        },
        {
          "id": "401820650",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820650/duke-louisville",
              "text": "Gamecast"
            }
          ],
          "week": 10,
          "atVs": "@",
          "gameDate": "2026-01-07T00:00Z",
          "score": "84-73",
          "homeTeamId": "97",
          "awayTeamId": "150",
          "homeTeamScore": "73",
          "awayTeamScore": "84",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "opponent": {
            "id": "97",
            "uid": "s:40~l:41~t:97",
            "displayName": "Louisville Cardinals",
            "abbreviation": "LOU",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/97/louisville-cardinals",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/97",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/97.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/97.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/97.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/97.png",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM"
        },
        {
          "id": "401820657",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820657/smu-duke",
              "text": "Gamecast"
            }
          ],
          "week": 10,
          "atVs": "vs",
          "gameDate": "2026-01-10T19:00Z",
          "score": "82-75",
          "homeTeamId": "150",
          "awayTeamId": "2567",
          "homeTeamScore": "82",
          "awayTeamScore": "75",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "opponent": {
            "id": "2567",
            "uid": "s:40~l:41~t:2567",
            "displayName": "SMU Mustangs",
            "abbreviation": "SMU",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/2567/smu-mustangs",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2567",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/2567.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM"
        },
        {
          "id": "401820666",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820666/duke-california",
              "text": "Gamecast"
            }
          ],
          "week": 11,
          "atVs": "@",
          "gameDate": "2026-01-15T04:10Z",
          "score": "71-56",
          "homeTeamId": "25",
          "awayTeamId": "150",
          "homeTeamScore": "56",
          "awayTeamScore": "71",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "25",
            "uid": "s:40~l:41~t:25",
            "displayName": "California Golden Bears",
            "abbreviation": "CAL",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/25/california-golden-bears",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/25",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/25.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/25.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/25.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/25.png"
        },
        {
          "id": "401820681",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820681/duke-stanford",
              "text": "Gamecast"
            }
          ],
          "week": 11,
          "atVs": "@",
          "gameDate": "2026-01-17T23:00Z",
          "score": "80-50",
          "homeTeamId": "24",
          "awayTeamId": "150",
          "homeTeamScore": "50",
          "awayTeamScore": "80",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "24",
            "uid": "s:40~l:41~t:24",
            "displayName": "Stanford Cardinal",
            "abbreviation": "STAN",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/24/stanford-cardinal",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/24",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/24.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/24.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/24.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/24.png"
        }
      ]
    },
    {
      "displayOrder": 1,
      "team": {
        "id": "154",
        "uid": "s:40~l:41~t:154",
        "displayName": "Wake Forest Demon Deacons",
        "abbreviation": "WAKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/154",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2025-12-19T22:35Z"
          }
        ]
      },
      "events": [
        {
          "id": "401820649",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820649/virginia-tech-wake-forest",
              "text": "Gamecast"
            }
          ],
          "week": 9,
          "atVs": "vs",
          "gameDate": "2026-01-03T17:00Z",
          "score": "81-78",
          "homeTeamId": "154",
          "awayTeamId": "259",
          "homeTeamScore": "81",
          "awayTeamScore": "78",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "259",
            "uid": "s:40~l:41~t:259",
            "displayName": "Virginia Tech Hokies",
            "abbreviation": "VT",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/259/virginia-tech-hokies",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/259",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/259.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/259.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/259.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/259.png"
        },
        {
          "id": "401820656",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820656/miami-wake-forest",
              "text": "Gamecast"
            }
          ],
          "week": 10,
          "atVs": "vs",
          "gameDate": "2026-01-08T00:00Z",
          "score": "81-77",
          "homeTeamId": "154",
          "awayTeamId": "2390",
          "homeTeamScore": "77",
          "awayTeamScore": "81",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "L",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "2390",
            "uid": "s:40~l:41~t:2390",
            "displayName": "Miami Hurricanes",
            "abbreviation": "MIA",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/2390/miami-hurricanes",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2390",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/2390.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png"
        },
        {
          "id": "401820661",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820661/wake-forest-north-carolina",
              "text": "Gamecast"
            }
          ],
          "week": 10,
          "atVs": "@",
          "gameDate": "2026-01-10T23:00Z",
          "score": "87-84",
          "homeTeamId": "153",
          "awayTeamId": "154",
          "homeTeamScore": "87",
          "awayTeamScore": "84",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "L",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "153",
            "uid": "s:40~l:41~t:153",
            "displayName": "North Carolina Tar Heels",
            "abbreviation": "UNC",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/153/north-carolina-tar-heels",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/153",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/153.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/153.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/153.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2026-01-05T20:06Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/153.png"
        },
        {
          "id": "401820677",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820677/wake-forest-florida-st",
              "text": "Gamecast"
            }
          ],
          "week": 11,
          "atVs": "@",
          "gameDate": "2026-01-17T23:00Z",
          "score": "69-68",
          "homeTeamId": "52",
          "awayTeamId": "154",
          "homeTeamScore": "68",
          "awayTeamScore": "69",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "W",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "52",
            "uid": "s:40~l:41~t:52",
            "displayName": "Florida State Seminoles",
            "abbreviation": "FSU",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/52/florida-state-seminoles",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/52",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/52.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png"
        },
        {
          "id": "401820683",
          "links": [
            {
              "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820683/smu-wake-forest",
              "text": "Gamecast"
            }
          ],
          "week": 12,
          "atVs": "vs",
          "gameDate": "2026-01-21T02:00Z",
          "score": "91-79",
          "homeTeamId": "154",
          "awayTeamId": "2567",
          "homeTeamScore": "79",
          "awayTeamScore": "91",
          "homeAggregateScore": "0",
          "awayAggregateScore": "0",
          "homeShootoutScore": "0",
          "awayShootoutScore": "0",
          "gameResult": "L",
          "leagueName": "NCAA Men's Basketball",
          "leagueAbbreviation": "NCAAM",
          "opponent": {
            "id": "2567",
            "uid": "s:40~l:41~t:2567",
            "displayName": "SMU Mustangs",
            "abbreviation": "SMU",
            "links": [
              {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/2567/smu-mustangs",
                "text": "Clubhouse"
              },
              {
                "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2567",
                "text": "Schedule"
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "default"
                ],
                "lastUpdated": "2025-12-19T22:33Z"
              },
              {
                "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/2567.png",
                "width": 500,
                "height": 500,
                "alt": "",
                "rel": [
                  "full",
                  "dark"
                ],
                "lastUpdated": "2025-12-19T22:35Z"
              }
            ]
          },
          "opponentLogo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png"
        }
      ]
    }
  ],
  "leaders": [
    {
      "team": {
        "id": "150",
        "uid": "s:40~l:41~t:150",
        "displayName": "Duke Blue Devils",
        "abbreviation": "DUKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/150",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2026-01-05T20:04Z"
          }
        ]
      },
      "leaders": [
        {
          "name": "pointsPerGame",
          "displayName": "Points",
          "leaders": [
            {
              "displayValue": "23.2",
              "athlete": {
                "id": "5041935",
                "uid": "s:40~l:41~a:5041935",
                "guid": "da7388f4-9ebf-3817-b810-a0711c384656",
                "lastName": "Boozer",
                "fullName": "Cameron Boozer",
                "displayName": "Cameron Boozer",
                "shortName": "C. Boozer",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5041935/cameron-boozer",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5041935.png",
                  "alt": "Cameron Boozer"
                },
                "jersey": "12",
                "position": {
                  "abbreviation": "F"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgPoints",
                  "displayName": "Points Per Game",
                  "shortDisplayName": "PPG",
                  "description": "The average number of points scored per game.",
                  "abbreviation": "PTS",
                  "value": 23.222221,
                  "displayValue": "23.2"
                },
                {
                  "name": "fieldGoalPct",
                  "displayName": "Field Goal Percentage",
                  "shortDisplayName": "FG%",
                  "description": "The ratio of field goals made to field goals attempted: FGM / FGA",
                  "abbreviation": "FG%",
                  "value": 58.6345374584198,
                  "displayValue": "58.6"
                },
                {
                  "name": "freeThrowPct",
                  "displayName": "Free Throw Percentage",
                  "shortDisplayName": "FT%",
                  "description": "The ratio of free throws made to free throws attempted: FTM / FTA",
                  "abbreviation": "FT%",
                  "value": 75.1879692077637,
                  "displayValue": "75.2"
                }
              ],
              "mainStat": {
                "value": "23.2",
                "label": "PPG"
              },
              "summary": "58.6 FG%, 75.2 FT%"
            }
          ]
        },
        {
          "name": "assistsPerGame",
          "displayName": "Assists",
          "leaders": [
            {
              "displayValue": "4.1",
              "athlete": {
                "id": "5041935",
                "uid": "s:40~l:41~a:5041935",
                "guid": "da7388f4-9ebf-3817-b810-a0711c384656",
                "lastName": "Boozer",
                "fullName": "Cameron Boozer",
                "displayName": "Cameron Boozer",
                "shortName": "C. Boozer",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5041935/cameron-boozer",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5041935.png",
                  "alt": "Cameron Boozer"
                },
                "jersey": "12",
                "position": {
                  "abbreviation": "F"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgAssists",
                  "displayName": "Assists Per Game",
                  "shortDisplayName": "APG",
                  "description": "The average assists per game.",
                  "abbreviation": "AST",
                  "value": 4.111111,
                  "displayValue": "4.1"
                },
                {
                  "name": "avgTurnovers",
                  "displayName": "Turnovers Per Game",
                  "shortDisplayName": "TOPG",
                  "description": "The average turnovers committed per game.",
                  "abbreviation": "TO",
                  "value": 2.2777777,
                  "displayValue": "2.3"
                },
                {
                  "name": "avgMinutes",
                  "displayName": "Minutes Per Game",
                  "shortDisplayName": "MPG",
                  "description": "The average number of minutes per game.",
                  "abbreviation": "MIN",
                  "value": 32.22222,
                  "displayValue": "32.2"
                }
              ],
              "mainStat": {
                "value": "4.1",
                "label": "APG"
              },
              "summary": "2.3 TOPG, 32.2 MPG"
            }
          ]
        },
        {
          "name": "reboundsPerGame",
          "displayName": "Rebounds",
          "leaders": [
            {
              "displayValue": "9.9",
              "athlete": {
                "id": "5041935",
                "uid": "s:40~l:41~a:5041935",
                "guid": "da7388f4-9ebf-3817-b810-a0711c384656",
                "lastName": "Boozer",
                "fullName": "Cameron Boozer",
                "displayName": "Cameron Boozer",
                "shortName": "C. Boozer",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5041935/cameron-boozer",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5041935.png",
                  "alt": "Cameron Boozer"
                },
                "jersey": "12",
                "position": {
                  "abbreviation": "F"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgRebounds",
                  "displayName": "Rebounds Per Game",
                  "shortDisplayName": "RPG",
                  "description": "The average rebounds per game.",
                  "abbreviation": "REB",
                  "value": 9.944445,
                  "displayValue": "9.9"
                },
                {
                  "name": "avgDefensiveRebounds",
                  "displayName": "Defensive Rebounds Per Game",
                  "shortDisplayName": "DRPG",
                  "description": "The average defensive rebounds per game.",
                  "abbreviation": "DR",
                  "value": 6.611111,
                  "displayValue": "6.6"
                },
                {
                  "name": "avgOffensiveRebounds",
                  "displayName": "Offensive Rebounds Per Game",
                  "shortDisplayName": "ORPG",
                  "description": "The average offensive rebounds per game.",
                  "abbreviation": "OR",
                  "value": 3.3333333,
                  "displayValue": "3.3"
                }
              ],
              "mainStat": {
                "value": "9.9",
                "label": "RPG"
              },
              "summary": "6.6 DRPG, 3.3 ORPG"
            }
          ]
        }
      ]
    },
    {
      "team": {
        "id": "154",
        "uid": "s:40~l:41~t:154",
        "displayName": "Wake Forest Demon Deacons",
        "abbreviation": "WAKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/154",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2025-12-19T22:35Z"
          }
        ]
      },
      "leaders": [
        {
          "name": "pointsPerGame",
          "displayName": "Points",
          "leaders": [
            {
              "displayValue": "20.5",
              "athlete": {
                "id": "5142609",
                "uid": "s:40~l:41~a:5142609",
                "guid": "9dda434d-3134-3964-8d8f-4987e05f12f4",
                "lastName": "Harris",
                "fullName": "Juke Harris",
                "displayName": "Juke Harris",
                "shortName": "J. Harris",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5142609/juke-harris",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5142609.png",
                  "alt": "Juke Harris"
                },
                "jersey": "2",
                "position": {
                  "abbreviation": "G"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgPoints",
                  "displayName": "Points Per Game",
                  "shortDisplayName": "PPG",
                  "description": "The average number of points scored per game.",
                  "abbreviation": "PTS",
                  "value": 20.473684,
                  "displayValue": "20.5"
                },
                {
                  "name": "fieldGoalPct",
                  "displayName": "Field Goal Percentage",
                  "shortDisplayName": "FG%",
                  "description": "The ratio of field goals made to field goals attempted: FGM / FGA",
                  "abbreviation": "FG%",
                  "value": 46.2450593709946,
                  "displayValue": "46.2"
                },
                {
                  "name": "freeThrowPct",
                  "displayName": "Free Throw Percentage",
                  "shortDisplayName": "FT%",
                  "description": "The ratio of free throws made to free throws attempted: FTM / FTA",
                  "abbreviation": "FT%",
                  "value": 75.8865237236023,
                  "displayValue": "75.9"
                }
              ],
              "mainStat": {
                "value": "20.5",
                "label": "PPG"
              },
              "summary": "46.2 FG%, 75.9 FT%"
            }
          ]
        },
        {
          "name": "assistsPerGame",
          "displayName": "Assists",
          "leaders": [
            {
              "displayValue": "5.2",
              "athlete": {
                "id": "5108081",
                "uid": "s:40~l:41~a:5108081",
                "guid": "50f620f5-69c1-363d-8ff6-c1436db9c4e6",
                "lastName": "Calmese",
                "fullName": "Nate Calmese",
                "displayName": "Nate Calmese",
                "shortName": "N. Calmese",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108081/nate-calmese",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5108081.png",
                  "alt": "Nate Calmese"
                },
                "jersey": "1",
                "position": {
                  "abbreviation": "G"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgAssists",
                  "displayName": "Assists Per Game",
                  "shortDisplayName": "APG",
                  "description": "The average assists per game.",
                  "abbreviation": "AST",
                  "value": 5.1578946,
                  "displayValue": "5.2"
                },
                {
                  "name": "avgTurnovers",
                  "displayName": "Turnovers Per Game",
                  "shortDisplayName": "TOPG",
                  "description": "The average turnovers committed per game.",
                  "abbreviation": "TO",
                  "value": 2.1578948,
                  "displayValue": "2.2"
                },
                {
                  "name": "avgMinutes",
                  "displayName": "Minutes Per Game",
                  "shortDisplayName": "MPG",
                  "description": "The average number of minutes per game.",
                  "abbreviation": "MIN",
                  "value": 26.789474,
                  "displayValue": "26.8"
                }
              ],
              "mainStat": {
                "value": "5.2",
                "label": "APG"
              },
              "summary": "2.2 TOPG, 26.8 MPG"
            }
          ]
        },
        {
          "name": "reboundsPerGame",
          "displayName": "Rebounds",
          "leaders": [
            {
              "displayValue": "6.4",
              "athlete": {
                "id": "5142609",
                "uid": "s:40~l:41~a:5142609",
                "guid": "9dda434d-3134-3964-8d8f-4987e05f12f4",
                "lastName": "Harris",
                "fullName": "Juke Harris",
                "displayName": "Juke Harris",
                "shortName": "J. Harris",
                "links": [
                  {
                    "rel": [
                      "playercard",
                      "desktop",
                      "athlete"
                    ],
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5142609/juke-harris",
                    "text": "Player Card"
                  }
                ],
                "headshot": {
                  "href": "https://a.espncdn.com/i/headshots/mens-college-basketball/players/full/5142609.png",
                  "alt": "Juke Harris"
                },
                "jersey": "2",
                "position": {
                  "abbreviation": "G"
                },
                "status": {
                  "id": "1",
                  "name": "Active",
                  "type": "active",
                  "abbreviation": "Active"
                }
              },
              "statistics": [
                {
                  "name": "avgRebounds",
                  "displayName": "Rebounds Per Game",
                  "shortDisplayName": "RPG",
                  "description": "The average rebounds per game.",
                  "abbreviation": "REB",
                  "value": 6.4210525,
                  "displayValue": "6.4"
                },
                {
                  "name": "avgDefensiveRebounds",
                  "displayName": "Defensive Rebounds Per Game",
                  "shortDisplayName": "DRPG",
                  "description": "The average defensive rebounds per game.",
                  "abbreviation": "DR",
                  "value": 5,
                  "displayValue": "5.0"
                },
                {
                  "name": "avgOffensiveRebounds",
                  "displayName": "Offensive Rebounds Per Game",
                  "shortDisplayName": "ORPG",
                  "description": "The average offensive rebounds per game.",
                  "abbreviation": "OR",
                  "value": 1.4210526,
                  "displayValue": "1.4"
                }
              ],
              "mainStat": {
                "value": "6.4",
                "label": "RPG"
              },
              "summary": "5.0 DRPG, 1.4 ORPG"
            }
          ]
        }
      ]
    }
  ],
  "broadcasts": [],
  "pickcenter": [
    {
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
      "details": "DUKE -18.5",
      "overUnder": 150.5,
      "spread": -18.5,
      "overOdds": -115,
      "underOdds": -105,
      "awayTeamOdds": {
        "favorite": false,
        "underdog": true,
        "moneyLine": 1100,
        "spreadOdds": -115,
        "team": {
          "$ref": "http://sports.core.api.espn.pvt/v2/sports/basketball/leagues/mens-college-basketball/seasons/2026/teams/154?lang=en&region=us"
        },
        "teamId": "154",
        "favoriteAtOpen": false
      },
      "homeTeamOdds": {
        "favorite": true,
        "underdog": false,
        "moneyLine": -2100,
        "spreadOdds": -105,
        "team": {
          "$ref": "http://sports.core.api.espn.pvt/v2/sports/basketball/leagues/mens-college-basketball/seasons/2026/teams/150?lang=en&region=us"
        },
        "teamId": "150",
        "favoriteAtOpen": true
      },
      "links": [
        {
          "language": "en-US",
          "rel": [
            "home",
            "desktop",
            "bets",
            "draft-kings"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0ML83116661_1",
          "text": "Home Bet",
          "shortText": "Home Bet",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "home",
              "betType": "straight"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "away",
            "desktop",
            "bets",
            "draft-kings"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0ML83116661_3",
          "text": "Away Bet",
          "shortText": "Away Bet",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "away",
              "betType": "straight"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "homeSpread",
            "desktop",
            "bets"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0HC83116661N1850_1",
          "text": "Home Point Spread",
          "shortText": "Home Point Spread",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "none",
              "betType": "straight",
              "betDetails": "Spread:DUKE-18.5"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "awaySpread",
            "desktop",
            "bets"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0HC83116661P1850_3",
          "text": "Away Point Spread",
          "shortText": "Away Point Spread",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "none",
              "betType": "straight",
              "betDetails": "Spread:WAKE+18.5"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "over",
            "desktop",
            "bets"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0OU83116661O15050_1",
          "text": "Over Odds",
          "shortText": "Over Odds",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "over",
              "betType": "straight",
              "betDetails": "Over:150.5"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "under",
            "desktop",
            "bets"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0OU83116661U15050_3",
          "text": "Under Odds",
          "shortText": "Under Odds",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "under",
              "betType": "straight",
              "betDetails": "Under:150.5"
            }
          }
        },
        {
          "language": "en-US",
          "rel": [
            "game",
            "desktop",
            "bets"
          ],
          "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277",
          "text": "See More Odds",
          "shortText": "Game",
          "isExternal": true,
          "isPremium": false,
          "tracking": {
            "campaign": "betting-integrations",
            "tags": {
              "league": "mens-college-basketball",
              "sport": "basketball",
              "gameId": 401820689,
              "betSide": "none",
              "betType": "straight"
            }
          }
        }
      ],
      "moneyline": {
        "displayName": "Moneyline",
        "shortDisplayName": "ML",
        "home": {
          "close": {
            "odds": "-2100",
            "link": {
              "language": "en-US",
              "rel": [
                "home",
                "desktop",
                "bets",
                "draft-kings"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0ML83116661_1",
              "text": "Home Bet",
              "shortText": "Home Bet",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "home",
                  "betType": "straight"
                }
              }
            }
          },
          "open": {
            "odds": "-6500"
          }
        },
        "away": {
          "close": {
            "odds": "+1100",
            "link": {
              "language": "en-US",
              "rel": [
                "away",
                "desktop",
                "bets",
                "draft-kings"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0ML83116661_3",
              "text": "Away Bet",
              "shortText": "Away Bet",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "away",
                  "betType": "straight"
                }
              }
            }
          },
          "open": {
            "odds": "+2000"
          }
        }
      },
      "pointSpread": {
        "displayName": "Spread",
        "shortDisplayName": "Spread",
        "home": {
          "close": {
            "line": "-18.5",
            "odds": "-105",
            "link": {
              "language": "en-US",
              "rel": [
                "homeSpread",
                "desktop",
                "bets"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0HC83116661N1850_1",
              "text": "Home Point Spread",
              "shortText": "Home Point Spread",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "none",
                  "betType": "straight",
                  "betDetails": "Spread:DUKE-18.5"
                }
              }
            }
          },
          "open": {
            "line": "-17.5",
            "odds": "-110"
          }
        },
        "away": {
          "close": {
            "line": "+18.5",
            "odds": "-115",
            "link": {
              "language": "en-US",
              "rel": [
                "awaySpread",
                "desktop",
                "bets"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0HC83116661P1850_3",
              "text": "Away Point Spread",
              "shortText": "Away Point Spread",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "none",
                  "betType": "straight",
                  "betDetails": "Spread:WAKE+18.5"
                }
              }
            }
          },
          "open": {
            "line": "+17.5",
            "odds": "-110"
          }
        }
      },
      "total": {
        "displayName": "Total",
        "shortDisplayName": "Total",
        "over": {
          "close": {
            "line": "o150.5",
            "odds": "-115",
            "link": {
              "language": "en-US",
              "rel": [
                "over",
                "desktop",
                "bets"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0OU83116661O15050_1",
              "text": "Over Odds",
              "shortText": "Over Odds",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "over",
                  "betType": "straight",
                  "betDetails": "Over:150.5"
                }
              }
            }
          },
          "open": {
            "line": "o149.5",
            "odds": "-110"
          }
        },
        "under": {
          "close": {
            "line": "u150.5",
            "odds": "-105",
            "link": {
              "language": "en-US",
              "rel": [
                "under",
                "desktop",
                "bets"
              ],
              "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277%3Foutcomes%3D0OU83116661U15050_3",
              "text": "Under Odds",
              "shortText": "Under Odds",
              "isExternal": true,
              "isPremium": false,
              "tracking": {
                "campaign": "betting-integrations",
                "tags": {
                  "league": "mens-college-basketball",
                  "sport": "basketball",
                  "gameId": 401820689,
                  "betSide": "under",
                  "betType": "straight",
                  "betDetails": "Under:150.5"
                }
              }
            }
          },
          "open": {
            "line": "u149.5",
            "odds": "-110"
          }
        }
      },
      "link": {
        "language": "en-US",
        "rel": [
          "game",
          "desktop",
          "bets"
        ],
        "href": "https://sportsbook.draftkings.com/gateway?s=__s__&wpcid=__wpcid__&wpsrc=413&wpcn=ESPN&wpscn=Widget&wpcrn=BetSlipDeepLink&wpscid=__wpscid__&wpcrid=xx&preurl=https%3A%2F%2Fsportsbook.draftkings.com%2Fevent%2F33516277",
        "text": "See More Odds",
        "shortText": "Game",
        "isExternal": true,
        "isPremium": false,
        "tracking": {
          "campaign": "betting-integrations",
          "tags": {
            "league": "mens-college-basketball",
            "sport": "basketball",
            "gameId": 401820689,
            "betSide": "none",
            "betType": "straight"
          }
        }
      },
      "header": {
        "logo": {
          "dark": "https://a.espncdn.com/i/espnbet/dark/espn-bet-square-off.svg",
          "light": "https://a.espncdn.com/i/espnbet/espn-bet-square-off.svg",
          "exclusivesLogoDark": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg",
          "exclusivesLogoLight": "https://a.espncdn.com/i/espnbet/espn-bet-square-mint.svg"
        },
        "text": "Game Odds"
      },
      "footer": {
        "disclaimer": "Odds by DraftKings\nGAMBLING PROBLEM? CALL 1-800-GAMBLER, (800) 327-5050 or visit gamblinghelplinema.org (MA). Call 877-8-HOPENY/text HOPENY (467369) (NY).\nPlease Gamble Responsibly. 888-789-7777/visit ccpg.org (CT), or visit www.mdgamblinghelp.org (MD).\n21+ and present in most states. (18+ DC/KY/NH/WY). Void in ONT/OR/NH. Eligibility restrictions apply. On behalf of Boot Hill Casino & Resort (KS). Terms: sportsbook.draftkings.com/promos."
      }
    }
  ],
  "odds": [],
  "againstTheSpread": [
    {
      "team": {
        "id": "154",
        "uid": "s:40~l:41~t:154",
        "displayName": "Wake Forest Demon Deacons",
        "abbreviation": "WAKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/154",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/154.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2025-12-19T22:35Z"
          }
        ]
      },
      "records": []
    },
    {
      "team": {
        "id": "150",
        "uid": "s:40~l:41~t:150",
        "displayName": "Duke Blue Devils",
        "abbreviation": "DUKE",
        "links": [
          {
            "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils",
            "text": "Clubhouse"
          },
          {
            "href": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/150",
            "text": "Schedule"
          }
        ],
        "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
        "logos": [
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "default"
            ],
            "lastUpdated": "2025-12-19T22:33Z"
          },
          {
            "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/150.png",
            "width": 500,
            "height": 500,
            "alt": "",
            "rel": [
              "full",
              "dark"
            ],
            "lastUpdated": "2026-01-05T20:04Z"
          }
        ]
      },
      "records": []
    }
  ],
  "winprobability": [],
  "predictor": {
    "header": "Matchup Predictor",
    "homeTeam": {
      "id": "150",
      "gameProjection": "95.2",
      "teamChanceLoss": "4.8"
    },
    "awayTeam": {
      "id": "154",
      "gameProjection": "4.8",
      "teamChanceLoss": "95.2"
    }
  },
  "news": {
    "header": "Men's College Basketball News",
    "link": {
      "language": "en-US",
      "rel": [
        "index",
        "desktop",
        "league"
      ],
      "href": "https://www.espn.com/mens-college-basketball/",
      "text": "All NCAAM News",
      "shortText": "All News",
      "isExternal": false,
      "isPremium": false
    },
    "articles": [
      {
        "id": 47710909,
        "nowId": "1-47710909",
        "contentKey": "47710909-1-21-1",
        "dataSourceIdentifier": "35f42c3562c2f",
        "type": "Recap",
        "headline": "Yaxel Lendeborg scores 18 points, grabs 9 rebounds and No. 3 Michigan beats Ohio State 74-62",
        "description": "— Yaxel Lendeborg had 18 points and nine rebounds, Morez Johnson scored 12 points and No. 3 Michigan beat Ohio State 74-62 on Friday night.",
        "lastModified": "2026-01-24T04:07:01Z",
        "published": "2026-01-24T04:07:01Z",
        "images": [
          {
            "type": "stitcher",
            "name": "espn.applewatch.awayhome.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.applewatch.awayhome.1"
          },
          {
            "type": "stitcher",
            "name": "espn.applewatch.homeaway.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.applewatch.homeaway.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.awayhome.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.homeaway.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.awayhome.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.homeaway.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.awayhome.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.homeaway.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.awayhome.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.homeaway.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.awayhome.5x2.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401825464.png?templateId=espn.all.homeaway.5x2.2"
          }
        ],
        "categories": [
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 3207,
            "type": "team",
            "uid": "s:40~l:41~t:130",
            "guid": "c00151c6-cdd4-5aab-0130-37416052eb2a",
            "description": "Michigan Wolverines",
            "sportId": 41,
            "teamId": 130,
            "team": {
              "id": 130,
              "description": "Michigan Wolverines",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/130/michigan-wolverines"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/130/michigan-wolverines"
                  }
                }
              }
            }
          },
          {
            "id": 3209,
            "type": "team",
            "uid": "s:40~l:41~t:194",
            "guid": "d6fdad20-942f-18ec-c5cb-eb8c7cf4e6c3",
            "description": "Ohio State Buckeyes",
            "sportId": 41,
            "teamId": 194,
            "team": {
              "id": 194,
              "description": "Ohio State Buckeyes",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/194/ohio-state-buckeyes"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/194/ohio-state-buckeyes"
                  }
                }
              }
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401825464",
            "guid": "576af194-7d67-3858-b100-455a442e2456",
            "description": "Ohio State Buckeyes @ Michigan Wolverines",
            "eventId": 401825464,
            "event": {
              "id": 401825464,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Ohio State Buckeyes @ Michigan Wolverines",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401825464"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401825464"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "c00151c6-cdd4-5aab-0130-37416052eb2a"
          },
          {
            "type": "guid",
            "guid": "2a530fde-e79b-3772-90a9-df2c1e75cc5e"
          },
          {
            "type": "guid",
            "guid": "d6fdad20-942f-18ec-c5cb-eb8c7cf4e6c3"
          },
          {
            "type": "guid",
            "guid": "576af194-7d67-3858-b100-455a442e2456"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "http://www.espn.com/ncb/recap?gameId=401825464"
          },
          "mobile": {
            "href": "http://m.espn.go.com/ncb/story?storyId=47710909"
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/sports/news/47710909"
            }
          },
          "app": {
            "sportscenter": {
              "href": "sportscenter://x-callback-url/showStory?uid=47710909"
            }
          }
        }
      },
      {
        "id": 47710902,
        "nowId": "1-47710902",
        "contentKey": "47710902-1-21-1",
        "dataSourceIdentifier": "8d89ca557d5f1",
        "type": "Recap",
        "headline": "Johnson's 24 lead Akron past Ohio 86-65",
        "description": "— Tavari Johnson had 24 points in Akron's 86-65 victory against Ohio on Friday.",
        "lastModified": "2026-01-24T04:04:00Z",
        "published": "2026-01-24T04:04:00Z",
        "images": [
          {
            "type": "stitcher",
            "name": "espn.applewatch.awayhome.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.applewatch.awayhome.1"
          },
          {
            "type": "stitcher",
            "name": "espn.applewatch.homeaway.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.applewatch.homeaway.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.awayhome.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.homeaway.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.awayhome.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.homeaway.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.awayhome.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.homeaway.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.awayhome.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.homeaway.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.awayhome.5x2.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401814534.png?templateId=espn.all.homeaway.5x2.2"
          },
          {
            "type": "Media",
            "name": "Akron Zips vs. Ohio Bobcats: Game Highlights",
            "caption": "Akron Zips vs. Ohio Bobcats: Game Highlights",
            "height": 324,
            "width": 576,
            "url": "https://a.espncdn.com/media/motion/wsc/2026/0124/e5b2cd88-5e80-41f1-bc8a-1e44435d83a5/e5b2cd88-5e80-41f1-bc8a-1e44435d83a5.jpg"
          }
        ],
        "categories": [
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 3280,
            "type": "team",
            "uid": "s:40~l:41~t:195",
            "guid": "f5ba8a7f-054a-841d-9066-66f95c5b81cd",
            "description": "Ohio Bobcats",
            "sportId": 41,
            "teamId": 195,
            "team": {
              "id": 195,
              "description": "Ohio Bobcats",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/195/ohio-bobcats"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/195/ohio-bobcats"
                  }
                }
              }
            }
          },
          {
            "id": 3282,
            "type": "team",
            "uid": "s:40~l:41~t:2006",
            "guid": "20bbf700-1b78-afa0-0cd4-241768e00a80",
            "description": "Akron Zips",
            "sportId": 41,
            "teamId": 2006,
            "team": {
              "id": 2006,
              "description": "Akron Zips",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2006/akron-zips"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2006/akron-zips"
                  }
                }
              }
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401814534",
            "guid": "0a72811d-c57c-36c2-bbc7-33650e0a78dd",
            "description": "Akron Zips @ Ohio Bobcats",
            "eventId": 401814534,
            "event": {
              "id": 401814534,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Akron Zips @ Ohio Bobcats",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401814534"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401814534"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "f5ba8a7f-054a-841d-9066-66f95c5b81cd"
          },
          {
            "type": "guid",
            "guid": "f1abe7cc-2c72-322c-a05e-555f5f69477d"
          },
          {
            "type": "guid",
            "guid": "20bbf700-1b78-afa0-0cd4-241768e00a80"
          },
          {
            "type": "guid",
            "guid": "0a72811d-c57c-36c2-bbc7-33650e0a78dd"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "http://www.espn.com/ncb/recap?gameId=401814534"
          },
          "mobile": {
            "href": "http://m.espn.go.com/ncb/story?storyId=47710902"
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/sports/news/47710902"
            }
          },
          "app": {
            "sportscenter": {
              "href": "sportscenter://x-callback-url/showStory?uid=47710902"
            }
          }
        }
      },
      {
        "id": 47710866,
        "nowId": "1-47710866",
        "contentKey": "47710866-1-21-1",
        "dataSourceIdentifier": "fe2eea0b09190",
        "type": "Recap",
        "headline": "Butler defeats Marquette 87-76",
        "description": "— Finley Bizjack had 28 points in Butler's 87-76 win over Marquette on Friday.",
        "lastModified": "2026-01-24T03:59:07Z",
        "published": "2026-01-24T03:59:07Z",
        "images": [
          {
            "type": "stitcher",
            "name": "espn.applewatch.awayhome.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.applewatch.awayhome.1"
          },
          {
            "type": "stitcher",
            "name": "espn.applewatch.homeaway.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.applewatch.homeaway.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.awayhome.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.homeaway.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.awayhome.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.homeaway.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.awayhome.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.homeaway.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.awayhome.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.homeaway.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.awayhome.5x2.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401822912.png?templateId=espn.all.homeaway.5x2.2"
          }
        ],
        "categories": [
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 3452,
            "type": "team",
            "uid": "s:40~l:41~t:2086",
            "guid": "dd75dc4c-5a13-a14e-23eb-e4b37ecd29bc",
            "description": "Butler Bulldogs",
            "sportId": 41,
            "teamId": 2086,
            "team": {
              "id": 2086,
              "description": "Butler Bulldogs",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2086/butler-bulldogs"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2086/butler-bulldogs"
                  }
                }
              }
            }
          },
          {
            "id": 3250,
            "type": "team",
            "uid": "s:40~l:41~t:269",
            "guid": "031f4755-6d7f-61c5-842c-9460a695085b",
            "description": "Marquette Golden Eagles",
            "sportId": 41,
            "teamId": 269,
            "team": {
              "id": 269,
              "description": "Marquette Golden Eagles",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/269/marquette-golden-eagles"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/269/marquette-golden-eagles"
                  }
                }
              }
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401822912",
            "guid": "fbe15515-a43b-3502-b5bd-bdad59600843",
            "description": "Marquette Golden Eagles @ Butler Bulldogs",
            "eventId": 401822912,
            "event": {
              "id": 401822912,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Marquette Golden Eagles @ Butler Bulldogs",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401822912"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401822912"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "dd75dc4c-5a13-a14e-23eb-e4b37ecd29bc"
          },
          {
            "type": "guid",
            "guid": "b52d7d1f-5057-3143-b1ab-3a27253e91c3"
          },
          {
            "type": "guid",
            "guid": "031f4755-6d7f-61c5-842c-9460a695085b"
          },
          {
            "type": "guid",
            "guid": "fbe15515-a43b-3502-b5bd-bdad59600843"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "http://www.espn.com/ncb/recap?gameId=401822912"
          },
          "mobile": {
            "href": "http://m.espn.go.com/ncb/story?storyId=47710866"
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/sports/news/47710866"
            }
          },
          "app": {
            "sportscenter": {
              "href": "sportscenter://x-callback-url/showStory?uid=47710866"
            }
          }
        }
      },
      {
        "id": 47710858,
        "nowId": "1-47710858",
        "contentKey": "47710858-1-21-1",
        "dataSourceIdentifier": "78564705a4d1d",
        "type": "Recap",
        "headline": "Longwood earns 81-79 OT victory against Charleston Southern",
        "description": "— Elijah Tucker scored 21 points and Jaylen Benard made a go-ahead layup with 10.1 seconds left in overtime as Longwood beat Charleston Southern 81-79 on Friday.",
        "lastModified": "2026-01-24T03:57:00Z",
        "published": "2026-01-24T03:57:00Z",
        "images": [
          {
            "type": "stitcher",
            "name": "espn.applewatch.awayhome.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.applewatch.awayhome.1"
          },
          {
            "type": "stitcher",
            "name": "espn.applewatch.homeaway.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.applewatch.homeaway.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.awayhome.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.homeaway.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.awayhome.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.homeaway.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.awayhome.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.homeaway.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.awayhome.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.homeaway.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.awayhome.5x2.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401823922.png?templateId=espn.all.homeaway.5x2.2"
          }
        ],
        "categories": [
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 15925,
            "type": "team",
            "uid": "s:40~l:41~t:2344",
            "guid": "b216cf7b-d484-f505-f9a3-f9abd7d508f7",
            "description": "Longwood Lancers",
            "sportId": 41,
            "teamId": 2344,
            "team": {
              "id": 2344,
              "description": "Longwood Lancers",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2344/longwood-lancers"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2344/longwood-lancers"
                  }
                }
              }
            }
          },
          {
            "id": 3197,
            "type": "team",
            "uid": "s:40~l:41~t:2127",
            "guid": "4e6559a9-194b-208f-f1bf-d3f27cb2c397",
            "description": "Charleston Southern Buccaneers",
            "sportId": 41,
            "teamId": 2127,
            "team": {
              "id": 2127,
              "description": "Charleston Southern Buccaneers",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2127/charleston-southern-buccaneers"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2127/charleston-southern-buccaneers"
                  }
                }
              }
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401823922",
            "guid": "930a8bd3-d8a5-3803-ad54-2a448732445c",
            "description": "Charleston Southern Buccaneers @ Longwood Lancers",
            "eventId": 401823922,
            "event": {
              "id": 401823922,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Charleston Southern Buccaneers @ Longwood Lancers",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401823922"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401823922"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "b216cf7b-d484-f505-f9a3-f9abd7d508f7"
          },
          {
            "type": "guid",
            "guid": "7f62727d-7837-3b7f-963f-496beacd5a28"
          },
          {
            "type": "guid",
            "guid": "4e6559a9-194b-208f-f1bf-d3f27cb2c397"
          },
          {
            "type": "guid",
            "guid": "930a8bd3-d8a5-3803-ad54-2a448732445c"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "http://www.espn.com/ncb/recap?gameId=401823922"
          },
          "mobile": {
            "href": "http://m.espn.go.com/ncb/story?storyId=47710858"
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/sports/news/47710858"
            }
          },
          "app": {
            "sportscenter": {
              "href": "sportscenter://x-callback-url/showStory?uid=47710858"
            }
          }
        }
      },
      {
        "id": 47710847,
        "nowId": "1-47710847",
        "contentKey": "47710847-1-21-1",
        "dataSourceIdentifier": "0f769135edec9",
        "type": "Recap",
        "headline": "Mingo scores 20 as Charlotte knocks off Tulane 73-70",
        "description": "— Dezayne Mingo's 20 points off of the bench helped Charlotte to a 73-70 victory against Tulane on Friday.",
        "lastModified": "2026-01-24T03:54:01Z",
        "published": "2026-01-24T03:54:01Z",
        "images": [
          {
            "type": "stitcher",
            "name": "espn.applewatch.awayhome.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.applewatch.awayhome.1"
          },
          {
            "type": "stitcher",
            "name": "espn.applewatch.homeaway.1",
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.applewatch.homeaway.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.awayhome.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.1",
            "ratio": "16x9",
            "height": 173,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.homeaway.16x9.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.awayhome.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.1x1.1",
            "ratio": "1x1",
            "height": 308,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.homeaway.1x1.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.awayhome.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.1",
            "ratio": "5x2",
            "height": 124,
            "width": 308,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.homeaway.5x2.1"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.awayhome.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.16x9.2",
            "ratio": "16x9",
            "height": 353,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.homeaway.16x9.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.awayhome.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.awayhome.5x2.2"
          },
          {
            "type": "stitcher",
            "name": "espn.all.homeaway.5x2.2",
            "ratio": "5x2",
            "height": 251,
            "width": 628,
            "url": "https://s.espncdn.com/stitcher/sports/basketball/mens-college-basketball/events/401828194.png?templateId=espn.all.homeaway.5x2.2"
          },
          {
            "type": "Media",
            "name": "Tulane Green Wave vs. Charlotte 49ers: Game Highlights",
            "caption": "Tulane Green Wave vs. Charlotte 49ers: Game Highlights",
            "height": 324,
            "width": 576,
            "url": "https://a.espncdn.com/media/motion/wsc/2026/0124/a642dc94-6bbc-4de4-84dc-0030366c447e/a642dc94-6bbc-4de4-84dc-0030366c447e.jpg"
          }
        ],
        "categories": [
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 3253,
            "type": "team",
            "uid": "s:40~l:41~t:2429",
            "guid": "69e7f920-01b0-8812-38a7-68d7dda17111",
            "description": "Charlotte 49ers",
            "sportId": 41,
            "teamId": 2429,
            "team": {
              "id": 2429,
              "description": "Charlotte 49ers",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2429/charlotte-49ers"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2429/charlotte-49ers"
                  }
                }
              }
            }
          },
          {
            "id": 3260,
            "type": "team",
            "uid": "s:40~l:41~t:2655",
            "guid": "fb13f437-f908-d98e-ab58-0afd729d8596",
            "description": "Tulane Green Wave",
            "sportId": 41,
            "teamId": 2655,
            "team": {
              "id": 2655,
              "description": "Tulane Green Wave",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2655/tulane-green-wave"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2655/tulane-green-wave"
                  }
                }
              }
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401828194",
            "guid": "49b78bdc-98c9-3a60-91ed-1569cf387393",
            "description": "Tulane Green Wave @ Charlotte 49ers",
            "eventId": 401828194,
            "event": {
              "id": 401828194,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Tulane Green Wave @ Charlotte 49ers",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401828194"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401828194"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "69e7f920-01b0-8812-38a7-68d7dda17111"
          },
          {
            "type": "guid",
            "guid": "aa7346a7-e0fe-3112-a8ee-5425f0780226"
          },
          {
            "type": "guid",
            "guid": "fb13f437-f908-d98e-ab58-0afd729d8596"
          },
          {
            "type": "guid",
            "guid": "49b78bdc-98c9-3a60-91ed-1569cf387393"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "http://www.espn.com/ncb/recap?gameId=401828194"
          },
          "mobile": {
            "href": "http://m.espn.go.com/ncb/story?storyId=47710847"
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/sports/news/47710847"
            }
          },
          "app": {
            "sportscenter": {
              "href": "sportscenter://x-callback-url/showStory?uid=47710847"
            }
          }
        }
      },
      {
        "id": 47710620,
        "nowId": "1-47710620",
        "contentKey": "47710620-1-293-1",
        "dataSourceIdentifier": "51bccbf73ed81",
        "type": "Media",
        "headline": "Akron Zips vs. Ohio Bobcats: Game Highlights",
        "description": "Akron Zips vs. Ohio Bobcats: Game Highlights",
        "lastModified": "2026-01-24T03:22:31Z",
        "published": "2026-01-24T03:22:31Z",
        "images": [
          {
            "name": "Akron Zips vs. Ohio Bobcats: Game Highlights",
            "caption": "Akron Zips vs. Ohio Bobcats: Game Highlights",
            "alt": "",
            "height": 324,
            "width": 576,
            "url": "https://a.espncdn.com/media/motion/wsc/2026/0124/e5b2cd88-5e80-41f1-bc8a-1e44435d83a5/e5b2cd88-5e80-41f1-bc8a-1e44435d83a5.jpg"
          }
        ],
        "categories": [
          {
            "id": 3280,
            "type": "team",
            "uid": "s:40~l:41~t:195",
            "guid": "f5ba8a7f-054a-841d-9066-66f95c5b81cd",
            "description": "Ohio Bobcats",
            "sportId": 41,
            "teamId": 195,
            "team": {
              "id": 195,
              "description": "Ohio Bobcats",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/195/ohio-bobcats"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/195/ohio-bobcats"
                  }
                }
              }
            }
          },
          {
            "id": 3282,
            "type": "team",
            "uid": "s:40~l:41~t:2006",
            "guid": "20bbf700-1b78-afa0-0cd4-241768e00a80",
            "description": "Akron Zips",
            "sportId": 41,
            "teamId": 2006,
            "team": {
              "id": 2006,
              "description": "Akron Zips",
              "links": {
                "web": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2006/akron-zips"
                  }
                },
                "mobile": {
                  "teams": {
                    "href": "https://www.espn.com/mens-college-basketball/team/_/id/2006/akron-zips"
                  }
                }
              }
            }
          },
          {
            "id": 570939,
            "type": "athlete",
            "uid": "s:40~l:41~a:5108059",
            "guid": "69e4c2d6-4879-3310-8ee9-8751686168e8",
            "description": "Tavari Johnson",
            "sportId": 41,
            "athleteId": 5108059,
            "athlete": {
              "id": 5108059,
              "description": "Tavari Johnson",
              "links": {
                "web": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108059/tavari-johnson"
                  }
                },
                "mobile": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108059/tavari-johnson"
                  }
                }
              }
            }
          },
          {
            "id": 568703,
            "type": "athlete",
            "uid": "s:40~l:41~a:5105840",
            "guid": "8abc6dbc-36b3-3e90-94ee-6e175fc67249",
            "description": "Bowen Hardman",
            "sportId": 41,
            "athleteId": 5105840,
            "athlete": {
              "id": 5105840,
              "description": "Bowen Hardman",
              "links": {
                "web": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5105840/bowen-hardman"
                  }
                },
                "mobile": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5105840/bowen-hardman"
                  }
                }
              }
            }
          },
          {
            "id": 711821,
            "type": "editorialindicator",
            "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
            "description": "SC4U - Full Highlight"
          },
          {
            "id": 9576,
            "type": "league",
            "uid": "s:40~l:41",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
            "description": "NCAA Men's Basketball",
            "sportId": 41,
            "leagueId": 41,
            "league": {
              "id": 41,
              "description": "NCAA Men's Basketball",
              "abbreviation": "NCAAM",
              "links": {
                "web": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                },
                "mobile": {
                  "leagues": {
                    "href": "https://www.espn.com/mens-college-basketball/"
                  }
                }
              }
            }
          },
          {
            "id": 690082,
            "type": "athlete",
            "uid": "s:40~l:41~a:5241470",
            "guid": "f6621645-f1b8-32c0-b4c7-d4b2d64b967d",
            "description": "Sharron Young",
            "sportId": 41,
            "athleteId": 5241470,
            "athlete": {
              "id": 5241470,
              "description": "Sharron Young",
              "links": {
                "web": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5241470/sharron-young"
                  }
                },
                "mobile": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5241470/sharron-young"
                  }
                }
              }
            }
          },
          {
            "id": 570945,
            "type": "athlete",
            "uid": "s:40~l:41~a:5108060",
            "guid": "0f937ab1-3250-3725-bd7d-8a2b802dd114",
            "description": "Amani Lyles",
            "sportId": 41,
            "athleteId": 5108060,
            "athlete": {
              "id": 5108060,
              "description": "Amani Lyles",
              "links": {
                "web": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108060/amani-lyles"
                  }
                },
                "mobile": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108060/amani-lyles"
                  }
                }
              }
            }
          },
          {
            "id": 711827,
            "type": "editorialindicator",
            "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4",
            "description": "3 Star Rating"
          },
          {
            "id": 711824,
            "type": "editorialindicator",
            "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
            "description": "SC4U  - Eligible"
          },
          {
            "id": 570901,
            "type": "athlete",
            "uid": "s:40~l:41~a:5108006",
            "guid": "50222f86-6e77-346a-9b50-77a806e4678e",
            "description": "Javan Simmons",
            "sportId": 41,
            "athleteId": 5108006,
            "athlete": {
              "id": 5108006,
              "description": "Javan Simmons",
              "links": {
                "web": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108006/javan-simmons"
                  }
                },
                "mobile": {
                  "athletes": {
                    "href": "https://www.espn.com/mens-college-basketball/player/_/id/5108006/javan-simmons"
                  }
                }
              }
            }
          },
          {
            "id": 195,
            "type": "team",
            "guid": "d171c740-5a6a-3abf-8538-63692327935f",
            "description": "Ohio University",
            "sportId": 3170,
            "teamId": 195,
            "team": {
              "id": 195,
              "description": "Ohio University"
            }
          },
          {
            "id": 2006,
            "type": "team",
            "guid": "973d0b8c-9059-3f87-a658-97e6e0f8aab4",
            "description": "University of Akron",
            "sportId": 3170,
            "teamId": 2006,
            "team": {
              "id": 2006,
              "description": "University of Akron"
            }
          },
          {
            "type": "event",
            "uid": "s:40~l:41~e:401814534",
            "guid": "0a72811d-c57c-36c2-bbc7-33650e0a78dd",
            "description": "Akron Zips @ Ohio Bobcats",
            "eventId": 401814534,
            "event": {
              "id": 401814534,
              "sport": "basketball",
              "league": "mens-college-basketball",
              "description": "Akron Zips @ Ohio Bobcats",
              "links": {
                "web": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401814534"
                  }
                },
                "mobile": {
                  "event": {
                    "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401814534"
                  }
                }
              }
            }
          },
          {
            "type": "guid",
            "guid": "f5ba8a7f-054a-841d-9066-66f95c5b81cd"
          },
          {
            "type": "guid",
            "guid": "f1abe7cc-2c72-322c-a05e-555f5f69477d"
          },
          {
            "type": "guid",
            "guid": "20bbf700-1b78-afa0-0cd4-241768e00a80"
          },
          {
            "type": "guid",
            "guid": "69e4c2d6-4879-3310-8ee9-8751686168e8"
          },
          {
            "type": "guid",
            "guid": "8abc6dbc-36b3-3e90-94ee-6e175fc67249"
          },
          {
            "type": "guid",
            "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
          },
          {
            "type": "guid",
            "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
          },
          {
            "type": "guid",
            "guid": "f6621645-f1b8-32c0-b4c7-d4b2d64b967d"
          },
          {
            "type": "guid",
            "guid": "0f937ab1-3250-3725-bd7d-8a2b802dd114"
          },
          {
            "type": "guid",
            "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4"
          },
          {
            "type": "guid",
            "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
          },
          {
            "type": "guid",
            "guid": "50222f86-6e77-346a-9b50-77a806e4678e"
          },
          {
            "type": "guid",
            "guid": "d171c740-5a6a-3abf-8538-63692327935f"
          },
          {
            "type": "guid",
            "guid": "973d0b8c-9059-3f87-a658-97e6e0f8aab4"
          },
          {
            "type": "guid",
            "guid": "0a72811d-c57c-36c2-bbc7-33650e0a78dd"
          }
        ],
        "premium": false,
        "links": {
          "web": {
            "href": "https://www.espn.com/video/clip?id=47710620",
            "self": {
              "href": "https://www.espn.com/video/clip?id=47710620",
              "dsi": {
                "href": "https://www.espn.com/video/clip?id=51bccbf73ed81"
              }
            }
          },
          "api": {
            "self": {
              "href": "https://content.core.api.espn.com/v1/video/clips/47710620"
            },
            "artwork": {
              "href": "https://artwork.api.espn.com/artwork/collections/media/378a15f3-2a24-4c56-97c0-7b11cdbf1664"
            }
          },
          "sportscenter": {
            "href": "sportscenter://x-callback-url/showVideo?videoID=47710620&videoDSI=51bccbf73ed81"
          }
        }
      }
    ]
  },
  "ticketsInfo": {
    "tickets": [
      {
        "ticketName": "All MENS-COLLEGE-BASKETBALL Tickets",
        "ticketLink": "https://www.vividseats.com/ncaab/?wsUser=717",
        "type": "league"
      },
      {
        "ticketName": "All Duke Blue Devils Tickets",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets--sports-ncaa-basketball/performer/255?wsUser=717",
        "type": "team"
      },
      {
        "ticketName": "1/24 vs Wake Forest Demon Deacons 107 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-13-2025--sports-ncaa-basketball/production/5845372?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "1/26 vs Louisville Cardinals 208 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-6-2025--sports-ncaa-basketball/production/5844690?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "1/31 @ Virginia Tech Hokies 480 tickets left",
        "ticketLink": "https://www.vividseats.com/virginia-tech-hokies-mens-basketball-tickets-cassell-coliseum-10-9-2025--sports-ncaa-basketball/production/5845865?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/3 vs Boston College Eagles 331 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-7-2025--sports-ncaa-basketball/production/5845358?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/7 @ North Carolina Tar Heels 870 tickets left",
        "ticketLink": "https://www.vividseats.com/north-carolina-tar-heels-mens-basketball-tickets-kenan-stadium-10-5-2025--sports-ncaa-basketball/production/5845882?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/10 @ Pittsburgh Panthers 2203 tickets left",
        "ticketLink": "https://www.vividseats.com/pittsburgh-panthers-mens-basketball-tickets-petersen-events-center-10-7-2025--sports-ncaa-basketball/production/5845803?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/14 vs Clemson Tigers 191 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-8-2025--sports-ncaa-basketball/production/5845360?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/16 vs Syracuse Orange 213 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-11-2025--sports-ncaa-basketball/production/5845368?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/21 vs Michigan Wolverines 2783 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-capital-one-arena-2-21-2026--sports-ncaa-basketball/production/5838127?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/24 @ Notre Dame Fighting Irish 1026 tickets left",
        "ticketLink": "https://www.vividseats.com/notre-dame-fighting-irish-mens-basketball-tickets-purcell-pavilion-at-the-joyce-center-10-8-2025--sports-ncaa-basketball/production/5845819?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "2/28 vs Virginia Cavaliers 121 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-12-2025--sports-ncaa-basketball/production/5845370?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "3/2 @ NC State Wolfpack 1034 tickets left",
        "ticketLink": "https://www.vividseats.com/north-carolina-state-wolfpack-mens-basketball-tickets-lenovo-center-10-7-2025--sports-ncaa-basketball/production/5845894?wsUser=717",
        "type": "event"
      },
      {
        "ticketName": "3/7 vs North Carolina Tar Heels 323 tickets left",
        "ticketLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-5-2025--sports-ncaa-basketball/production/5844688?wsUser=717",
        "type": "event"
      }
    ],
    "seatSituation": {
      "opponentTeamName": "Wake Forest Demon Deacons",
      "currentTeamName": "Duke Blue Devils",
      "venueName": "Cameron Indoor Stadium",
      "summary": "Tickets as low as $110",
      "date": "2026-01-24T17:00Z",
      "dateDay": "Sat",
      "homeAway": "home",
      "eventLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-13-2025--sports-ncaa-basketball/production/5845372?wsUser=717",
      "venueLink": "https://www.vividseats.com/cameron-indoor-stadium-tickets/venue/263?wsUser=717",
      "genericLink": "https://www.vividseats.com/?wsUser=717",
      "teamLink": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets--sports-ncaa-basketball/performer/255?wsUser=717",
      "timeValid": true
    }
  },
  "article": {
    "id": 47702495,
    "nowId": "1-47702495",
    "contentKey": "47702495-1-22-1",
    "dataSourceIdentifier": "2c7d05a62d14a",
    "publishedkey": "ncb401820689",
    "type": "Preview",
    "gameId": "401820689",
    "headline": "No. 5 Duke hosts Wake Forest following Boozer's 30-point game",
    "description": "Wake Forest Demon Deacons (11-8, 2-4 ACC) at Duke Blue Devils (17-1, 6-0 ACC)",
    "title": "No. 5 Duke hosts Wake Forest following Boozer's 30-point game",
    "linkText": "No. 5 Duke hosts Wake Forest following Boozer's 30-point game",
    "categorized": "2026-01-23T09:54:51Z",
    "originallyPosted": "2026-01-23T09:54:49Z",
    "lastModified": "2026-01-23T09:54:51Z",
    "published": "2026-01-23T09:54:49Z",
    "root": "ncb",
    "section": "Men's College Basketball",
    "source": "Data Skrive",
    "images": [],
    "video": [],
    "categories": [
      {
        "id": 9576,
        "type": "league",
        "uid": "s:40~l:41",
        "guid": "11965179-4504-3b99-983e-83ea0e36d5f3",
        "description": "NCAA Men's Basketball",
        "sportId": 41,
        "leagueId": 41,
        "league": {
          "id": 41,
          "description": "NCAA Men's Basketball",
          "abbreviation": "NCAAM",
          "links": {
            "web": {
              "leagues": {
                "href": "https://www.espn.com/mens-college-basketball/"
              }
            },
            "mobile": {
              "leagues": {
                "href": "https://www.espn.com/mens-college-basketball/"
              }
            }
          }
        }
      },
      {
        "id": 3155,
        "type": "team",
        "uid": "s:40~l:41~t:150",
        "guid": "c4430c6c-5998-47d5-7c45-1cdb7ca0befc",
        "description": "Duke Blue Devils",
        "sportId": 41,
        "teamId": 150,
        "team": {
          "id": 150,
          "description": "Duke Blue Devils",
          "links": {
            "web": {
              "teams": {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils"
              }
            },
            "mobile": {
              "teams": {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils"
              }
            }
          }
        }
      },
      {
        "id": 3158,
        "type": "team",
        "uid": "s:40~l:41~t:154",
        "guid": "c52631ea-cc93-df5d-fd15-e4e1c250fbe2",
        "description": "Wake Forest Demon Deacons",
        "sportId": 41,
        "teamId": 154,
        "team": {
          "id": 154,
          "description": "Wake Forest Demon Deacons",
          "links": {
            "web": {
              "teams": {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons"
              }
            },
            "mobile": {
              "teams": {
                "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons"
              }
            }
          }
        }
      },
      {
        "type": "event",
        "uid": "s:40~l:41~e:401820689",
        "guid": "56dc93fe-17fb-300d-9d1a-f11a2c152110",
        "description": "Wake Forest Demon Deacons @ Duke Blue Devils",
        "eventId": 401820689,
        "event": {
          "id": 401820689,
          "sport": "basketball",
          "league": "mens-college-basketball",
          "description": "Wake Forest Demon Deacons @ Duke Blue Devils"
        }
      },
      {
        "type": "guid",
        "guid": "11965179-4504-3b99-983e-83ea0e36d5f3"
      },
      {
        "type": "guid",
        "guid": "c4430c6c-5998-47d5-7c45-1cdb7ca0befc"
      },
      {
        "type": "guid",
        "guid": "1b1b66a7-672b-3451-9bb6-4086e6f00e5d"
      },
      {
        "type": "guid",
        "guid": "c52631ea-cc93-df5d-fd15-e4e1c250fbe2"
      },
      {
        "type": "guid",
        "guid": "56dc93fe-17fb-300d-9d1a-f11a2c152110"
      }
    ],
    "keywords": [
      "NCAA Men's Basketball",
      "Duke Blue Devils",
      "Wake Forest Demon Deacons",
      "Wake Forest Demon Deacons @ Duke Blue Devils"
    ],
    "story": "\u003Ca href=\"http://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons\"\u003EWake Forest Demon Deacons\u003C/a\u003E (11-8, 2-4 ACC) at \u003Ca href=\"http://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils\"\u003EDuke Blue Devils\u003C/a\u003E (17-1, 6-0 ACC)\n\n\r\n              Durham, North Carolina; Saturday, 12 p.m. EST\n\n\r\n              BOTTOM LINE: No. 5 Duke plays Wake Forest after \u003Ca href=\"http://www.espn.com/mens-college-basketball/player/_/id/5041935/cameron-boozer\"\u003ECameron Boozer\u003C/a\u003E scored 30 points in Duke's 80-50 win over the \u003Ca href=\"http://www.espn.com/mens-college-basketball/team/_/id/24/stanford-cardinal\"\u003EStanford Cardinal\u003C/a\u003E.\n\n\r\n              The Blue Devils have gone 8-0 at home. Duke is the top team in the ACC at limiting opponent scoring, giving up 65.1 points while holding opponents to 39.2% shooting.\n\n\r\n              The Demon Deacons are 2-4 against ACC opponents. Wake Forest scores 80.9 points while outscoring opponents by 5.1 points per game.\n\n\r\n              Duke makes 49.8% of its shots from the field this season, which is 5.9 percentage points higher than Wake Forest has allowed to its opponents (43.9%). Wake Forest averages 9.2 made 3-pointers per game this season, 1.4 more made shots on average than the 7.8 per game Duke allows.\n\n\r\n              The matchup Saturday is the first meeting this season between the two teams in conference play.\n\n\r\n              TOP PERFORMERS: Boozer is scoring 23.2 points per game with 9.9 rebounds and 4.0 assists for the Blue Devils. \u003Ca href=\"http://www.espn.com/mens-college-basketball/player/_/id/5061585/isaiah-evans\"\u003EIsaiah Evans\u003C/a\u003E is averaging 16.3 points over the past 10 games.\n\n\r\n              \u003Ca href=\"http://www.espn.com/mens-college-basketball/player/_/id/5142609/juke-harris\"\u003EJuke Harris\u003C/a\u003E is scoring 20.5 points per game and averaging 6.4 rebounds for the Demon Deacons. \u003Ca href=\"http://www.espn.com/mens-college-basketball/player/_/id/5108081/nate-calmese\"\u003ENate Calmese\u003C/a\u003E is averaging 2.1 made 3-pointers over the last 10 games.\n\n\r\n              LAST 10 GAMES: Blue Devils: 9-1, averaging 80.4 points, 34.7 rebounds, 15.3 assists, 9.2 steals and 4.2 blocks per game while shooting 48.0% from the field. Their opponents have averaged 70.1 points per game.\n\n\r\n              Demon Deacons: 5-5, averaging 77.1 points, 27.1 rebounds, 14.1 assists, 9.4 steals and 3.0 blocks per game while shooting 45.3% from the field. Their opponents have averaged 78.0 points.\n\n\r\n              ------\n\n\r\n              The Associated Press created this story using technology provided by \u003Ca href=\"https://www.dataskrive.com/\"\u003EData Skrive\u003C/a\u003E and data from \u003Ca href=\"https://www.sportradar.com\"\u003ESportradar\u003C/a\u003E.",
    "premium": false,
    "isLiveBlog": false,
    "links": {
      "web": {
        "href": "http://www.espn.com/ncb/preview?gameId=401820689"
      },
      "mobile": {
        "href": "http://m.espn.go.com/ncb/story?storyId=47702495"
      },
      "api": {
        "self": {
          "href": "https://content.core.api.espn.com/v1/sports/news/47702495"
        }
      },
      "app": {
        "sportscenter": {
          "href": "sportscenter://x-callback-url/showStory?uid=47702495"
        }
      }
    },
    "allowSearch": true,
    "allowContentReactions": false
  },
  "videos": [],
  "header": {
    "id": "401820689",
    "uid": "s:40~l:41~e:401820689",
    "season": {
      "year": 2026,
      "current": true,
      "type": 2
    },
    "timeValid": true,
    "competitions": [
      {
        "id": "401820689",
        "uid": "s:40~l:41~e:401820689~c:401820689",
        "date": "2026-01-24T17:00Z",
        "neutralSite": false,
        "conferenceCompetition": true,
        "boxscoreAvailable": false,
        "commentaryAvailable": false,
        "liveAvailable": false,
        "onWatchESPN": false,
        "recent": false,
        "wallclockAvailable": false,
        "boxscoreSource": "none",
        "playByPlaySource": "none",
        "competitors": [
          {
            "id": "150",
            "uid": "s:40~l:41~t:150",
            "order": 0,
            "homeAway": "home",
            "team": {
              "id": "150",
              "guid": "c4430c6c-5998-47d5-7c45-1cdb7ca0befc",
              "uid": "s:40~l:41~t:150",
              "location": "Duke",
              "name": "Blue Devils",
              "nickname": "Duke",
              "abbreviation": "DUKE",
              "displayName": "Duke Blue Devils",
              "color": "00539b",
              "alternateColor": "ffffff",
              "logos": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/150.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2026-01-05T20:04Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/primary_logo_on_white_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_white_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/primary_logo_on_black_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_black_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/primary_logo_on_primary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_primary_color"
                  ],
                  "lastUpdated": "2025-12-20T18:48Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/primary_logo_on_secondary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_secondary_color"
                  ],
                  "lastUpdated": "2025-12-20T18:49Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/secondary_logo_on_white_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_white_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/secondary_logo_on_black_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_black_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/secondary_logo_on_primary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_primary_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c4430c6c-5998-47d5-7c45-1cdb7ca0befc/logos/secondary_logo_on_secondary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_secondary_color"
                  ],
                  "lastUpdated": "2024-11-11T00:20Z"
                }
              ],
              "groups": {
                "id": "2",
                "parent": {
                  "id": "50",
                  "name": "NCAA Division I",
                  "slug": "ncaa-division-i"
                },
                "isConference": true,
                "slug": "atlantic-coast-conference"
              },
              "links": [
                {
                  "rel": [
                    "clubhouse",
                    "desktop",
                    "team"
                  ],
                  "href": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils",
                  "text": "Clubhouse"
                }
              ]
            },
            "record": [
              {
                "type": "total",
                "summary": "17-1",
                "displayValue": "17-1"
              },
              {
                "type": "home",
                "summary": "8-0",
                "displayValue": "8-0"
              },
              {
                "type": "vsconf",
                "summary": "6-0",
                "displayValue": "6-0"
              }
            ],
            "possession": false,
            "rank": 5
          },
          {
            "id": "154",
            "uid": "s:40~l:41~t:154",
            "order": 1,
            "homeAway": "away",
            "team": {
              "id": "154",
              "guid": "c52631ea-cc93-df5d-fd15-e4e1c250fbe2",
              "uid": "s:40~l:41~t:154",
              "location": "Wake Forest",
              "name": "Demon Deacons",
              "nickname": "Wake Forest",
              "abbreviation": "WAKE",
              "displayName": "Wake Forest Demon Deacons",
              "color": "ceb888",
              "alternateColor": "2c2a29",
              "logos": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/154.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/primary_logo_on_white_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_white_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/primary_logo_on_black_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_black_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/primary_logo_on_primary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_primary_color"
                  ],
                  "lastUpdated": "2025-12-20T21:21Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/primary_logo_on_secondary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "primary_logo_on_secondary_color"
                  ],
                  "lastUpdated": "2025-12-20T21:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/secondary_logo_on_white_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_white_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/secondary_logo_on_black_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_black_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/secondary_logo_on_primary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_primary_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                },
                {
                  "href": "https://a.espncdn.com/guid/c52631ea-cc93-df5d-fd15-e4e1c250fbe2/logos/secondary_logo_on_secondary_color.png",
                  "width": 4096,
                  "height": 4096,
                  "alt": "",
                  "rel": [
                    "full",
                    "secondary_logo_on_secondary_color"
                  ],
                  "lastUpdated": "2024-11-11T00:22Z"
                }
              ],
              "groups": {
                "id": "2",
                "parent": {
                  "id": "50",
                  "name": "NCAA Division I",
                  "slug": "ncaa-division-i"
                },
                "isConference": true,
                "slug": "atlantic-coast-conference"
              },
              "links": [
                {
                  "rel": [
                    "clubhouse",
                    "desktop",
                    "team"
                  ],
                  "href": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons",
                  "text": "Clubhouse"
                }
              ]
            },
            "record": [
              {
                "type": "total",
                "summary": "11-8",
                "displayValue": "11-8"
              },
              {
                "type": "road",
                "summary": "1-2",
                "displayValue": "1-2"
              },
              {
                "type": "vsconf",
                "summary": "2-4",
                "displayValue": "2-4"
              }
            ],
            "possession": false
          }
        ],
        "status": {
          "type": {
            "id": "1",
            "name": "STATUS_SCHEDULED",
            "state": "pre",
            "completed": false,
            "description": "Scheduled",
            "detail": "Sat, January 24th at 12:00 PM EST",
            "shortDetail": "1/24 - 12:00 PM EST"
          }
        },
        "odds": [
          {
            "awayTeamOdds": {
              "favorite": false,
              "underdog": true,
              "moneyLine": 1100,
              "spreadOdds": -115,
              "open": {
                "favorite": false,
                "pointSpread": {
                  "alternateDisplayValue": "+17.5",
                  "american": "+17.5"
                },
                "spread": {
                  "value": 1.9,
                  "displayValue": "10/11",
                  "alternateDisplayValue": "-110",
                  "decimal": 1.9,
                  "fraction": "10/11",
                  "american": "-110"
                },
                "moneyLine": {
                  "value": 21,
                  "displayValue": "20/1",
                  "alternateDisplayValue": "+2000",
                  "decimal": 21,
                  "fraction": "20/1",
                  "american": "+2000"
                }
              },
              "current": {
                "pointSpread": {
                  "alternateDisplayValue": "+18.5",
                  "american": "+18.5"
                },
                "spread": {
                  "value": 1.86,
                  "displayValue": "20/23",
                  "alternateDisplayValue": "-115",
                  "decimal": 1.86,
                  "fraction": "20/23",
                  "american": "-115"
                },
                "moneyLine": {
                  "value": 12,
                  "displayValue": "11/1",
                  "alternateDisplayValue": "+1100",
                  "decimal": 12,
                  "fraction": "11/1",
                  "american": "+1100"
                }
              },
              "team": {
                "$ref": "http://sports.core.api.espn.pvt/v2/sports/basketball/leagues/mens-college-basketball/seasons/2026/teams/154?lang=en&region=us"
              }
            },
            "homeTeamOdds": {
              "favorite": true,
              "underdog": false,
              "moneyLine": -2100,
              "spreadOdds": -105,
              "open": {
                "favorite": true,
                "pointSpread": {
                  "alternateDisplayValue": "-17.5",
                  "american": "-17.5"
                },
                "spread": {
                  "value": 1.9,
                  "displayValue": "10/11",
                  "alternateDisplayValue": "-110",
                  "decimal": 1.9,
                  "fraction": "10/11",
                  "american": "-110"
                },
                "moneyLine": {
                  "value": 1.01,
                  "displayValue": "1/65",
                  "alternateDisplayValue": "-6500",
                  "decimal": 1.01,
                  "fraction": "1/65",
                  "american": "-6500"
                }
              },
              "current": {
                "pointSpread": {
                  "alternateDisplayValue": "-18.5",
                  "american": "-18.5"
                },
                "spread": {
                  "value": 1.95,
                  "displayValue": "20/21",
                  "alternateDisplayValue": "-105",
                  "decimal": 1.95,
                  "fraction": "20/21",
                  "american": "-105"
                },
                "moneyLine": {
                  "value": 1.04,
                  "displayValue": "1/21",
                  "alternateDisplayValue": "-2100",
                  "decimal": 1.04,
                  "fraction": "1/21",
                  "american": "-2100"
                }
              },
              "team": {
                "$ref": "http://sports.core.api.espn.pvt/v2/sports/basketball/leagues/mens-college-basketball/seasons/2026/teams/150?lang=en&region=us"
              }
            },
            "current": {
              "over": {
                "value": 1.86,
                "displayValue": "20/23",
                "alternateDisplayValue": "-115",
                "decimal": 1.86,
                "fraction": "20/23",
                "american": "-115"
              },
              "under": {
                "value": 1.95,
                "displayValue": "20/21",
                "alternateDisplayValue": "-105",
                "decimal": 1.95,
                "fraction": "20/21",
                "american": "-105"
              },
              "total": {
                "alternateDisplayValue": "150.5",
                "american": "150.5"
              }
            }
          }
        ],
        "broadcasts": [
          {
            "type": {
              "id": "1",
              "shortName": "TV"
            },
            "market": {
              "id": "1",
              "type": "National"
            },
            "media": {
              "shortName": "The CW Network"
            },
            "lang": "en",
            "region": "us",
            "isNational": true
          }
        ],
        "groups": {
          "id": "2",
          "name": "Atlantic Coast Conference",
          "abbreviation": "acc",
          "shortName": "ACC",
          "midsizeName": "ACC"
        },
        "boxscoreMinutes": false
      }
    ],
    "links": [
      {
        "rel": [
          "summary",
          "desktop",
          "event"
        ],
        "href": "https://www.espn.com/mens-college-basketball/game/_/gameId/401820689/wake-forest-duke",
        "text": "Gamecast",
        "shortText": "Summary",
        "isExternal": false,
        "isPremium": false
      },
      {
        "rel": [
          "preview",
          "desktop",
          "event"
        ],
        "href": "https://www.espn.com/mens-college-basketball/preview/_/gameId/401820689",
        "text": "Preview",
        "shortText": "Preview",
        "isExternal": false,
        "isPremium": false
      },
      {
        "rel": [
          "tickets",
          "desktop"
        ],
        "href": "https://www.vividseats.com/duke-blue-devils-mens-basketball-tickets-cameron-indoor-stadium-10-13-2025--sports-ncaa-basketball/production/5845372?wsUser=717",
        "text": "Tickets",
        "shortText": "Tickets",
        "isExternal": true,
        "isPremium": false
      }
    ],
    "week": 12,
    "league": {
      "id": "41",
      "uid": "s:40~l:41",
      "name": "NCAA Men's Basketball",
      "abbreviation": "NCAAM",
      "midsizeName": "NCAAM Basketball",
      "slug": "mens-college-basketball",
      "isTournament": false,
      "links": [
        {
          "rel": [
            "index",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/",
          "text": "Index"
        },
        {
          "rel": [
            "index",
            "sportscenter",
            "app",
            "league"
          ],
          "href": "sportscenter://x-callback-url/showClubhouse?uid=s:40~l:41",
          "text": "Index"
        },
        {
          "rel": [
            "schedule",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/schedule",
          "text": "Schedule"
        },
        {
          "rel": [
            "schedule",
            "sportscenter",
            "app",
            "league"
          ],
          "href": "sportscenter://x-callback-url/showClubhouse?uid=s:40~l:41&section=scores",
          "text": "Schedule"
        },
        {
          "rel": [
            "standings",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/standings",
          "text": "Standings"
        },
        {
          "rel": [
            "standings",
            "sportscenter",
            "app",
            "league"
          ],
          "href": "sportscenter://x-callback-url/showClubhouse?uid=s:40~l:41&section=standings",
          "text": "Standings"
        },
        {
          "rel": [
            "rankings",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/rankings",
          "text": "Rankings"
        },
        {
          "rel": [
            "scores",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/scoreboard",
          "text": "Scores"
        },
        {
          "rel": [
            "scores",
            "sportscenter",
            "app",
            "league"
          ],
          "href": "sportscenter://x-callback-url/showClubhouse?uid=s:40~l:41&section=scores",
          "text": "Scores"
        },
        {
          "rel": [
            "stats",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/stats",
          "text": "Stats"
        },
        {
          "rel": [
            "teams",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/teams",
          "text": "Teams"
        },
        {
          "rel": [
            "injuries",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/injuries",
          "text": "Injuries"
        },
        {
          "rel": [
            "odds",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/odds",
          "text": "Odds"
        },
        {
          "rel": [
            "odds",
            "sportscenter",
            "app",
            "league"
          ],
          "href": "sportscenter://x-callback-url/showClubhouse?uid=s:40~l:41&section=odds",
          "text": "Odds"
        },
        {
          "rel": [
            "bpi_overview",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi",
          "text": "Overview"
        },
        {
          "rel": [
            "bpi_bpi",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi/_/view/bpi",
          "text": "BPI"
        },
        {
          "rel": [
            "bpi_resume",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi/_/view/resume",
          "text": "Resume"
        },
        {
          "rel": [
            "bpi_projections",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi/_/view/projections",
          "text": "Projections"
        },
        {
          "rel": [
            "bpi_predictions",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi/_/view/predictions",
          "text": "Daily Predictions"
        },
        {
          "rel": [
            "bpi_tournament",
            "desktop",
            "league"
          ],
          "href": "https://www.espn.com/mens-college-basketball/bpi/_/view/tournament",
          "text": "Tournament"
        }
      ],
      "logos": [
        {
          "href": "https://a.espncdn.com/redesign/assets/img/icons/ESPN-icon-basketball.png",
          "rel": [
            "full",
            "default"
          ]
        },
        {
          "href": "https://a.espncdn.com/redesign/assets/img/icons/ESPN-icon-basketball.png",
          "rel": [
            "full",
            "dark"
          ]
        }
      ]
    }
  },
  "wallclockAvailable": false,
  "meta": {
    "gp_topic": "gp-basketball-mens-college-basketball-401820689",
    "gameSwitcherEnabled": true,
    "picker_topic": "picker-basketball-mens-college-basketball",
    "gameState": "pre"
  },
  "standings": {
    "fullViewLink": {
      "text": "Full Standings",
      "href": "https://www.espn.com/mens-college-basketball/standings"
    },
    "header": "2025-26 Standings",
    "groups": [
      {
        "standings": {
          "entries": [
            {
              "team": "Duke",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/150/duke-blue-devils",
              "id": "150",
              "uid": "s:40~l:41~t:150",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "17-1",
                  "displayValue": "17-1"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 0,
                  "displayValue": "-"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "6-0",
                  "displayValue": "6-0"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/150.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/150.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2026-01-05T20:04Z"
                }
              ]
            },
            {
              "team": "Clemson",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/228/clemson-tigers",
              "id": "228",
              "uid": "s:40~l:41~t:228",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "16-4",
                  "displayValue": "16-4"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 0.5,
                  "displayValue": "0.5"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "6-1",
                  "displayValue": "6-1"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/228.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/228.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2026-01-05T20:04Z"
                }
              ]
            },
            {
              "team": "Virginia",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/258/virginia-cavaliers",
              "id": "258",
              "uid": "s:40~l:41~t:258",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "16-2",
                  "displayValue": "16-2"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 1,
                  "displayValue": "1"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "5-1",
                  "displayValue": "5-1"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/258.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/258.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Miami",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/2390/miami-hurricanes",
              "id": "2390",
              "uid": "s:40~l:41~t:2390",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "15-4",
                  "displayValue": "15-4"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 2,
                  "displayValue": "2"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "4-2",
                  "displayValue": "4-2"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/2390.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "NC State",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/152/nc-state-wolfpack",
              "id": "152",
              "uid": "s:40~l:41~t:152",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "13-6",
                  "displayValue": "13-6"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 2,
                  "displayValue": "2"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "4-2",
                  "displayValue": "4-2"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/152.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/152.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Virginia Tech",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/259/virginia-tech-hokies",
              "id": "259",
              "uid": "s:40~l:41~t:259",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "15-5",
                  "displayValue": "15-5"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 2.5,
                  "displayValue": "2.5"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "4-3",
                  "displayValue": "4-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/259.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/259.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "North Carolina",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/153/north-carolina-tar-heels",
              "id": "153",
              "uid": "s:40~l:41~t:153",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "15-4",
                  "displayValue": "15-4"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 3,
                  "displayValue": "3"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "3-3",
                  "displayValue": "3-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/153.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/153.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2026-01-05T20:06Z"
                }
              ]
            },
            {
              "team": "Stanford",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/24/stanford-cardinal",
              "id": "24",
              "uid": "s:40~l:41~t:24",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "14-5",
                  "displayValue": "14-5"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 3,
                  "displayValue": "3"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "3-3",
                  "displayValue": "3-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/24.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/24.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "SMU",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/2567/smu-mustangs",
              "id": "2567",
              "uid": "s:40~l:41~t:2567",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "14-5",
                  "displayValue": "14-5"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 3,
                  "displayValue": "3"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "3-3",
                  "displayValue": "3-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/2567.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Louisville",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/97/louisville-cardinals",
              "id": "97",
              "uid": "s:40~l:41~t:97",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "13-5",
                  "displayValue": "13-5"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 3,
                  "displayValue": "3"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "3-3",
                  "displayValue": "3-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/97.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/97.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Syracuse",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/183/syracuse-orange",
              "id": "183",
              "uid": "s:40~l:41~t:183",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "12-7",
                  "displayValue": "12-7"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 3,
                  "displayValue": "3"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "3-3",
                  "displayValue": "3-3"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/183.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/183.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "California",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/25/california-golden-bears",
              "id": "25",
              "uid": "s:40~l:41~t:25",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "14-5",
                  "displayValue": "14-5"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 4,
                  "displayValue": "4"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "2-4",
                  "displayValue": "2-4"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/25.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/25.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Georgia Tech",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/59/georgia-tech-yellow-jackets",
              "id": "59",
              "uid": "s:40~l:41~t:59",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "11-8",
                  "displayValue": "11-8"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 4,
                  "displayValue": "4"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "2-4",
                  "displayValue": "2-4"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/59.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/59.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Wake Forest",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/154/wake-forest-demon-deacons",
              "id": "154",
              "uid": "s:40~l:41~t:154",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "11-8",
                  "displayValue": "11-8"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 4,
                  "displayValue": "4"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "2-4",
                  "displayValue": "2-4"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/154.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/154.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Boston College",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/103/boston-college-eagles",
              "id": "103",
              "uid": "s:40~l:41~t:103",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "9-10",
                  "displayValue": "9-10"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 4,
                  "displayValue": "4"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "2-4",
                  "displayValue": "2-4"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/103.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/103.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Notre Dame",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/87/notre-dame-fighting-irish",
              "id": "87",
              "uid": "s:40~l:41~t:87",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "10-9",
                  "displayValue": "10-9"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 5,
                  "displayValue": "5"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "1-5",
                  "displayValue": "1-5"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/87.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/87.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Florida State",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/52/florida-state-seminoles",
              "id": "52",
              "uid": "s:40~l:41~t:52",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "8-11",
                  "displayValue": "8-11"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 5,
                  "displayValue": "5"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "1-5",
                  "displayValue": "1-5"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/52.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            },
            {
              "team": "Pittsburgh",
              "link": "https://www.espn.com/mens-college-basketball/team/_/id/221/pittsburgh-panthers",
              "id": "221",
              "uid": "s:40~l:41~t:221",
              "stats": [
                {
                  "id": "0",
                  "name": "overall",
                  "abbreviation": "Season",
                  "displayName": "Team Season Record",
                  "shortDisplayName": "Season",
                  "description": "Overall Record",
                  "type": "total",
                  "summary": "8-11",
                  "displayValue": "8-11"
                },
                {
                  "name": "gamesBehind",
                  "displayName": "Games Back",
                  "shortDisplayName": "GB",
                  "description": "Games Back",
                  "abbreviation": "GB",
                  "type": "vsconf_gamesbehind",
                  "value": 5,
                  "displayValue": "5"
                },
                {
                  "id": "9",
                  "name": "vs. Conf.",
                  "abbreviation": "VS CONF",
                  "displayName": "CONF",
                  "shortDisplayName": "CONF",
                  "description": "Conference Record",
                  "type": "vsconf",
                  "summary": "1-5",
                  "displayValue": "1-5"
                }
              ],
              "logo": [
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500/221.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "default"
                  ],
                  "lastUpdated": "2025-12-19T22:33Z"
                },
                {
                  "href": "https://a.espncdn.com/i/teamlogos/ncaa/500-dark/221.png",
                  "width": 500,
                  "height": 500,
                  "alt": "",
                  "rel": [
                    "full",
                    "dark"
                  ],
                  "lastUpdated": "2025-12-19T22:35Z"
                }
              ]
            }
          ]
        },
        "header": "2025-26 Atlantic Coast Conference Standings",
        "href": "https://www.espn.com/mens-college-basketball/standings/_/group/2",
        "conferenceHeader": "NCAA Division I",
        "divisionHeader": "Atlantic Coast Conference",
        "shortDivisionHeader": "ACC"
      }
    ],
    "isSameConference": true
  }
}
```