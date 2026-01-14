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
            "2025-11-01T07:00Z",
            "2025-11-02T07:00Z",
            "2025-11-03T08:00Z"
          ],
          "events": [
            {
              "id": "401810003",
              "uid": "s:40~l:46~e:401810003~c:401810003",
              "guid": "a5f1bada-c1e9-3e5d-ba11-6344c1028a2e",
              "date": "2025-11-02T20:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "New Orleans Pelicans at Oklahoma City Thunder",
              "shortName": "NO @ OKC",
              "seriesSummary": "OKC leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810003/pelicans-thunder",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810003",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810003",
              "location": "Chesapeake Energy Arena",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810003/pelicans-thunder",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 3,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
                }
              },
              "competitors": [
                {
                  "id": "3",
                  "guid": "9461f397-7882-94c0-c18c-e89bdc9e570e",
                  "uid": "s:40~l:46~t:3",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "New Orleans Pelicans",
                  "name": "Pelicans",
                  "abbreviation": "NO",
                  "location": "New Orleans",
                  "color": "0a2240",
                  "alternateColor": "b4975a",
                  "score": "106",
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
                  "record": "0-6",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 0
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
                      "value": -3
                    },
                    "pointsFor": {
                      "value": 106
                    },
                    "pointsAgainst": {
                      "value": 137
                    },
                    "avgPointsFor": {
                      "value": 17.6666660308838
                    },
                    "avgPointsAgainst": {
                      "value": 22.8333339691162
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 2
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": -6
                    },
                    "playoffSeed": {
                      "value": 15
                    },
                    "gamesBehind": {
                      "value": 6.5
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 0
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 4
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/no.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/no.png"
                },
                {
                  "id": "25",
                  "guid": "bd458c44-2d33-47eb-cebc-35d3d4ac595c",
                  "uid": "s:40~l:46~t:25",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Oklahoma City Thunder",
                  "name": "Thunder",
                  "abbreviation": "OKC",
                  "location": "Oklahoma City",
                  "color": "007ac1",
                  "alternateColor": "ef3b24",
                  "score": "137",
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
                  "record": "7-0",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 7
                    },
                    "losses": {
                      "value": 0
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
                      "value": 137
                    },
                    "pointsAgainst": {
                      "value": 106
                    },
                    "avgPointsFor": {
                      "value": 19.5714282989502
                    },
                    "avgPointsAgainst": {
                      "value": 15.1428575515747
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 1
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 0
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": 7
                    },
                    "playoffSeed": {
                      "value": 1
                    },
                    "gamesBehind": {
                      "value": 0
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 4
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 3
                    },
                    "roadLosses": {
                      "value": 0
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/okc.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/okc.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810003",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810003",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810003",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46823172,
                "dataSourceIdentifier": "231511a6024e7",
                "cerebroId": "6907e3d9a421b770c0833d38",
                "pccId": "8d07ff14-9952-4fc8-a752-021411b70cfa",
                "source": "espn",
                "headline": "New Orleans Pelicans vs. Oklahoma City Thunder: Game Highlights",
                "caption": "New Orleans Pelicans vs. Oklahoma City Thunder: Game Highlights",
                "title": "New Orleans Pelicans vs. Oklahoma City Thunder: Game Highlights",
                "description": "New Orleans Pelicans vs. Oklahoma City Thunder: Game Highlights",
                "lastModified": "2025-11-02T23:12:29Z",
                "originalPublishDate": "2025-11-02T23:05:50Z",
                "premium": false,
                "syndicatable": true,
                "duration": 74,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-02T23:05:50Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "FJ",
                    "LS",
                    "BJ",
                    "GQ",
                    "BS",
                    "UY",
                    "VG",
                    "GT",
                    "BR",
                    "AS",
                    "HN",
                    "CF",
                    "PE",
                    "MX",
                    "LR",
                    "US",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "ZW",
                    "NI",
                    "ST",
                    "TZ",
                    "MG",
                    "GP",
                    "NG",
                    "TC",
                    "AR",
                    "KE",
                    "MS",
                    "CG",
                    "ER",
                    "CI",
                    "MW",
                    "GM",
                    "SV",
                    "LC",
                    "BZ",
                    "CM",
                    "GH",
                    "KM",
                    "KY",
                    "DO",
                    "PY",
                    "VC",
                    "JM",
                    "GF",
                    "RW",
                    "CD",
                    "ZM",
                    "SN",
                    "GY",
                    "GB",
                    "UK",
                    "BF",
                    "CL",
                    "MH",
                    "PW",
                    "AU",
                    "CV",
                    "UG",
                    "BM",
                    "CO",
                    "AI",
                    "GN",
                    "BQ",
                    "GW",
                    "GA",
                    "ML",
                    "PA",
                    "BB",
                    "ZA",
                    "FM",
                    "MZ",
                    "SX",
                    "EC",
                    "BW",
                    "BI",
                    "NZ",
                    "AW",
                    "KN",
                    "ET",
                    "HT",
                    "NE",
                    "SC",
                    "AO",
                    "TG",
                    "CU",
                    "GD",
                    "SL",
                    "TT",
                    "NA",
                    "VE",
                    "CR",
                    "RE",
                    "BO",
                    "SR",
                    "AM",
                    "MF",
                    "MQ",
                    "MU",
                    "AG",
                    "SZ",
                    "SS"
                  ]
                },
                "gameId": 401810003,
                "plays": [
                  {
                    "id": 40181000352
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46823172",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46823172"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46823172"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46823172"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/8d07ff14-9952-4fc8-a752-021411b70cfa/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46823172"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/8d07ff14-9952-4fc8-a752-021411b70cfa/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46823172"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46823172"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/8d07ff14-9952-4fc8-a752-021411b70cfa"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/8d07ff14-9952-4fc8-a752-021411b70cfa/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1102/02505020-46d4-4d2f-95ce-db305364f5df/02505020-46d4-4d2f-95ce-db305364f5df_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46823172&videoDSI=231511a6024e7"
                  }
                },
                "categories": [
                  {
                    "id": 168949,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4222252",
                    "guid": "1b8bb909-9b5c-2498-030f-1e5140c6eec8",
                    "description": "Isaiah Hartenstein",
                    "sportId": 46,
                    "athleteId": 4222252,
                    "athlete": {
                      "id": 4222252,
                      "description": "Isaiah Hartenstein",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4222252/isaiah-hartenstein"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4222252/isaiah-hartenstein"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 187309,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4278073",
                    "guid": "4dcec409-3ff9-2881-2bc3-b4289ce6c36d",
                    "description": "Shai Gilgeous-Alexander",
                    "sportId": 46,
                    "athleteId": 4278073,
                    "athlete": {
                      "id": 4278073,
                      "description": "Shai Gilgeous-Alexander",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4278073/shai-gilgeous-alexander"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4278073/shai-gilgeous-alexander"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810003",
                    "guid": "a5f1bada-c1e9-3e5d-ba11-6344c1028a2e",
                    "description": "New Orleans Pelicans @ Oklahoma City Thunder",
                    "eventId": 401810003,
                    "event": {
                      "id": 401810003,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "New Orleans Pelicans @ Oklahoma City Thunder",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810003"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810003"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 114922,
                    "type": "team",
                    "uid": "s:40~l:46~t:3",
                    "guid": "9461f397-7882-94c0-c18c-e89bdc9e570e",
                    "description": "New Orleans Pelicans",
                    "sportId": 46,
                    "teamId": 3,
                    "team": {
                      "id": 3,
                      "description": "New Orleans Pelicans",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/no/new-orleans-pelicans"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/no/new-orleans-pelicans"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 384265,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4395628",
                    "guid": "34e5ec5d-10b3-ba59-2ba1-3a3be9a1be22",
                    "description": "Zion Williamson",
                    "sportId": 46,
                    "athleteId": 4395628,
                    "athlete": {
                      "id": 4395628,
                      "description": "Zion Williamson",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395628/zion-williamson"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395628/zion-williamson"
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
                    "id": 4695,
                    "type": "team",
                    "uid": "s:40~l:46~t:25",
                    "guid": "bd458c44-2d33-47eb-cebc-35d3d4ac595c",
                    "description": "Oklahoma City Thunder",
                    "sportId": 46,
                    "teamId": 25,
                    "team": {
                      "id": 25,
                      "description": "Oklahoma City Thunder",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/okc/oklahoma-city-thunder"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/okc/oklahoma-city-thunder"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "1b8bb909-9b5c-2498-030f-1e5140c6eec8"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "4dcec409-3ff9-2881-2bc3-b4289ce6c36d"
                  },
                  {
                    "type": "guid",
                    "guid": "a5f1bada-c1e9-3e5d-ba11-6344c1028a2e"
                  },
                  {
                    "type": "guid",
                    "guid": "9461f397-7882-94c0-c18c-e89bdc9e570e"
                  },
                  {
                    "type": "guid",
                    "guid": "34e5ec5d-10b3-ba59-2ba1-3a3be9a1be22"
                  },
                  {
                    "type": "guid",
                    "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4"
                  },
                  {
                    "type": "guid",
                    "guid": "bd458c44-2d33-47eb-cebc-35d3d4ac595c"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (New Orleans Pelicans vs. Oklahoma City Thunder: Game Highlights) 2025/11/02 ESHEET",
                  "trackingId": "dm_20251102_NBA_new_orleans_pelicans_vs_oklahoma_city_thunder_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810004",
              "uid": "s:40~l:46~e:401810004~c:401810004",
              "guid": "66fb1fab-673b-3502-aeb3-944895e78f36",
              "date": "2025-11-02T23:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Philadelphia 76ers at Brooklyn Nets",
              "shortName": "PHI @ BKN",
              "seriesSummary": "PHI leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810004/76ers-nets",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810004",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810004",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810004/76ers-nets",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
                }
              },
              "competitors": [
                {
                  "id": "20",
                  "guid": "ca1685ed-b799-53e4-7924-e58ea6eb8f3a",
                  "uid": "s:40~l:46~t:20",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": true,
                  "displayName": "Philadelphia 76ers",
                  "name": "76ers",
                  "abbreviation": "PHI",
                  "location": "Philadelphia",
                  "color": "1d428a",
                  "alternateColor": "e01234",
                  "score": "129",
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
                  "record": "5-1",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 5
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
                      "value": 2
                    },
                    "pointsFor": {
                      "value": 129
                    },
                    "pointsAgainst": {
                      "value": 105
                    },
                    "avgPointsFor": {
                      "value": 21.5
                    },
                    "avgPointsAgainst": {
                      "value": 17.5
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.833333313465118
                    },
                    "leagueWinPercent": {
                      "value": 0
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
                      "value": 2
                    },
                    "gamesBehind": {
                      "value": 0.5
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
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
                      "value": 0
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phi.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/phi.png"
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
                  "score": "105",
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
                  "record": "0-6",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 0
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
                      "value": -3
                    },
                    "pointsFor": {
                      "value": 105
                    },
                    "pointsAgainst": {
                      "value": 129
                    },
                    "avgPointsFor": {
                      "value": 17.5
                    },
                    "avgPointsAgainst": {
                      "value": 21.5
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": -6
                    },
                    "playoffSeed": {
                      "value": 15
                    },
                    "gamesBehind": {
                      "value": 5.5
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 0
                    },
                    "homeLosses": {
                      "value": 3
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 3
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810004",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810004",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810004",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46825295,
                "dataSourceIdentifier": "df91f49cc6f95",
                "cerebroId": "6908083ca421b770c08356e8",
                "pccId": "feee3005-a3db-4db0-9839-e0ab207caa25",
                "source": "espn",
                "headline": "Philadelphia 76ers vs. Brooklyn Nets: Game Highlights",
                "caption": "Philadelphia 76ers vs. Brooklyn Nets: Game Highlights",
                "title": "Philadelphia 76ers vs. Brooklyn Nets: Game Highlights",
                "description": "Philadelphia 76ers vs. Brooklyn Nets: Game Highlights",
                "lastModified": "2025-11-03T02:22:29Z",
                "originalPublishDate": "2025-11-03T01:41:07Z",
                "premium": false,
                "syndicatable": true,
                "duration": 74,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T01:41:07Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "FJ",
                    "LS",
                    "BJ",
                    "GQ",
                    "BS",
                    "UY",
                    "VG",
                    "GT",
                    "BR",
                    "AS",
                    "HN",
                    "CF",
                    "PE",
                    "MX",
                    "LR",
                    "US",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "ZW",
                    "NI",
                    "ST",
                    "TZ",
                    "MG",
                    "GP",
                    "NG",
                    "TC",
                    "AR",
                    "KE",
                    "MS",
                    "CG",
                    "ER",
                    "CI",
                    "MW",
                    "GM",
                    "SV",
                    "LC",
                    "BZ",
                    "CM",
                    "GH",
                    "KM",
                    "KY",
                    "DO",
                    "PY",
                    "VC",
                    "JM",
                    "GF",
                    "RW",
                    "CD",
                    "ZM",
                    "SN",
                    "GY",
                    "GB",
                    "UK",
                    "BF",
                    "CL",
                    "MH",
                    "PW",
                    "AU",
                    "CV",
                    "UG",
                    "BM",
                    "CO",
                    "AI",
                    "GN",
                    "BQ",
                    "GW",
                    "GA",
                    "ML",
                    "PA",
                    "BB",
                    "ZA",
                    "FM",
                    "MZ",
                    "SX",
                    "EC",
                    "BW",
                    "BI",
                    "NZ",
                    "AW",
                    "KN",
                    "ET",
                    "HT",
                    "NE",
                    "SC",
                    "AO",
                    "TG",
                    "CU",
                    "GD",
                    "SL",
                    "TT",
                    "NA",
                    "VE",
                    "CR",
                    "RE",
                    "BO",
                    "SR",
                    "AM",
                    "MF",
                    "MQ",
                    "MU",
                    "AG",
                    "SZ",
                    "SS"
                  ]
                },
                "gameId": 401810004,
                "plays": [
                  {
                    "id": 40181000426
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46825295",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46825295",
                      "dsi": {
                        "href": "https://www.espn.com/video/clip?id=df91f49cc6f95"
                      }
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46825295"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46825295"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/feee3005-a3db-4db0-9839-e0ab207caa25/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825295"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/feee3005-a3db-4db0-9839-e0ab207caa25/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825295"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46825295"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/feee3005-a3db-4db0-9839-e0ab207caa25"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/feee3005-a3db-4db0-9839-e0ab207caa25/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/14eb6aab-95b7-4b40-9544-43ff007c4213/14eb6aab-95b7-4b40-9544-43ff007c4213_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46825295&videoDSI=df91f49cc6f95"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 492136,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4397014",
                    "guid": "dbe4d07d-9166-07d7-19f0-52cc771d179d",
                    "description": "Quentin Grimes",
                    "sportId": 46,
                    "athleteId": 4397014,
                    "athlete": {
                      "id": 4397014,
                      "description": "Quentin Grimes",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4397014/quentin-grimes"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4397014/quentin-grimes"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 140920,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3133603",
                    "guid": "9e672c74-a038-60b0-a85c-9b8a6ff4b8fa",
                    "description": "Kelly Oubre Jr",
                    "sportId": 46,
                    "athleteId": 3133603,
                    "athlete": {
                      "id": 3133603,
                      "description": "Kelly Oubre Jr",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3133603/kelly-oubre-jr"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3133603/kelly-oubre-jr"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810004",
                    "guid": "66fb1fab-673b-3502-aeb3-944895e78f36",
                    "description": "Philadelphia 76ers @ Brooklyn Nets",
                    "eventId": 401810004,
                    "event": {
                      "id": 401810004,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Philadelphia 76ers @ Brooklyn Nets",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810004"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810004"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4323,
                    "type": "team",
                    "uid": "s:40~l:46~t:20",
                    "guid": "ca1685ed-b799-53e4-7924-e58ea6eb8f3a",
                    "description": "Philadelphia 76ers",
                    "sportId": 46,
                    "teamId": 20,
                    "team": {
                      "id": 20,
                      "description": "Philadelphia 76ers",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/phi/philadelphia-76ers"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/phi/philadelphia-76ers"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 492486,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4432174",
                    "guid": "55617f6a-a1fb-326e-8c71-31211dcad955",
                    "description": "Cam Thomas",
                    "sportId": 46,
                    "athleteId": 4432174,
                    "athlete": {
                      "id": 4432174,
                      "description": "Cam Thomas",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4432174/cam-thomas"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4432174/cam-thomas"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 104965,
                    "type": "team",
                    "uid": "s:40~l:46~t:17",
                    "guid": "926db769-d35e-e282-9d7e-a05001d774ab",
                    "description": "Brooklyn Nets",
                    "sportId": 46,
                    "teamId": 17,
                    "team": {
                      "id": 17,
                      "description": "Brooklyn Nets",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/bkn/brooklyn-nets"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/bkn/brooklyn-nets"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711828,
                    "type": "editorialindicator",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7",
                    "description": "4 Star Rating"
                  },
                  {
                    "id": 688339,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:5124612",
                    "guid": "d5a0355a-95f4-38ed-b96d-ea0302ebbd0b",
                    "description": "VJ Edgecombe",
                    "sportId": 46,
                    "athleteId": 5124612,
                    "athlete": {
                      "id": 5124612,
                      "description": "VJ Edgecombe",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/5124612/vj-edgecombe"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/5124612/vj-edgecombe"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "dbe4d07d-9166-07d7-19f0-52cc771d179d"
                  },
                  {
                    "type": "guid",
                    "guid": "9e672c74-a038-60b0-a85c-9b8a6ff4b8fa"
                  },
                  {
                    "type": "guid",
                    "guid": "66fb1fab-673b-3502-aeb3-944895e78f36"
                  },
                  {
                    "type": "guid",
                    "guid": "ca1685ed-b799-53e4-7924-e58ea6eb8f3a"
                  },
                  {
                    "type": "guid",
                    "guid": "55617f6a-a1fb-326e-8c71-31211dcad955"
                  },
                  {
                    "type": "guid",
                    "guid": "926db769-d35e-e282-9d7e-a05001d774ab"
                  },
                  {
                    "type": "guid",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7"
                  },
                  {
                    "type": "guid",
                    "guid": "d5a0355a-95f4-38ed-b96d-ea0302ebbd0b"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Philadelphia 76ers vs. Brooklyn Nets: Game Highlights) 2025/11/02 ESHEET",
                  "trackingId": "dm_20251102_NBA_philadelphia_76ers_vs_brooklyn_nets_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810005",
              "uid": "s:40~l:46~e:401810005~c:401810005",
              "guid": "72c15c44-fc43-3e87-b0ec-c14e2ec57f1a",
              "date": "2025-11-02T23:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Utah Jazz at Charlotte Hornets",
              "shortName": "UTAH @ CHA",
              "seriesSummary": "CHA leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810005/jazz-hornets",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810005",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810005",
              "location": "Spectrum Center",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810005/jazz-hornets",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
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
                  "typeId": 1,
                  "priority": 4,
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
                  "typeId": 4,
                  "priority": 2,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
                }
              },
              "competitors": [
                {
                  "id": "26",
                  "guid": "77cea2fb-1388-b7c8-d171-2e72b3aecbfb",
                  "uid": "s:40~l:46~t:26",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Utah Jazz",
                  "name": "Jazz",
                  "abbreviation": "UTAH",
                  "location": "Utah",
                  "color": "4e008e",
                  "alternateColor": "79a3dc",
                  "score": "103",
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
                  "record": "2-4",
                  "records": [],
                  "group": "11",
                  "recordStats": {
                    "wins": {
                      "value": 2
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
                      "value": -1
                    },
                    "pointsFor": {
                      "value": 103
                    },
                    "pointsAgainst": {
                      "value": 126
                    },
                    "avgPointsFor": {
                      "value": 17.1666660308838
                    },
                    "avgPointsAgainst": {
                      "value": 21
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.333333343267441
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": -3
                    },
                    "playoffSeed": {
                      "value": 13
                    },
                    "gamesBehind": {
                      "value": 4.5
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 1
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 3
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/utah.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/utah.png"
                },
                {
                  "id": "30",
                  "guid": "377633c2-0dd1-91a1-83c0-9ed2d0c00ea1",
                  "uid": "s:40~l:46~t:30",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Charlotte Hornets",
                  "name": "Hornets",
                  "abbreviation": "CHA",
                  "location": "Charlotte",
                  "color": "008ca8",
                  "alternateColor": "1d1060",
                  "score": "126",
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
                  "record": "3-4",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 3
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 126
                    },
                    "pointsAgainst": {
                      "value": 103
                    },
                    "avgPointsFor": {
                      "value": 18
                    },
                    "avgPointsAgainst": {
                      "value": 14.7142858505249
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0
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
                      "value": 11
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/cha.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/cha.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810005",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810005",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810005",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46825335,
                "dataSourceIdentifier": "5451a00167f1c",
                "cerebroId": "690808e6c66a8438e7af6984",
                "pccId": "3dc2f5bc-6824-41f8-9640-3d82fdd7fbef",
                "source": "espn",
                "headline": "Utah Jazz vs. Charlotte Hornets: Game Highlights",
                "caption": "Utah Jazz vs. Charlotte Hornets: Game Highlights",
                "title": "Utah Jazz vs. Charlotte Hornets: Game Highlights",
                "description": "Utah Jazz vs. Charlotte Hornets: Game Highlights",
                "lastModified": "2025-11-03T01:47:42Z",
                "originalPublishDate": "2025-11-03T01:43:56Z",
                "premium": false,
                "syndicatable": true,
                "duration": 71,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T01:43:56Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "BF",
                    "ZW",
                    "PA",
                    "ML",
                    "GD",
                    "MU",
                    "BQ",
                    "US",
                    "AS",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "NG",
                    "SS",
                    "KE",
                    "BR",
                    "UG",
                    "MH",
                    "GH",
                    "RW",
                    "ET",
                    "CO",
                    "AO",
                    "HT",
                    "MW",
                    "CM",
                    "KY",
                    "HN",
                    "CR",
                    "BM",
                    "GW",
                    "MX",
                    "BS",
                    "NA",
                    "KM",
                    "SZ",
                    "BO",
                    "SX",
                    "GN",
                    "VC",
                    "BJ",
                    "GB",
                    "UK",
                    "MQ",
                    "TC",
                    "BW",
                    "JM",
                    "MS",
                    "NE",
                    "PE",
                    "AM",
                    "AR",
                    "CF",
                    "GM",
                    "NZ",
                    "GT",
                    "GP",
                    "LC",
                    "SV",
                    "ER",
                    "KN",
                    "CL",
                    "CD",
                    "MZ",
                    "PW",
                    "AI",
                    "AW",
                    "PY",
                    "CI",
                    "SC",
                    "CU",
                    "GF",
                    "GA",
                    "RE",
                    "NI",
                    "FM",
                    "FJ",
                    "VE",
                    "DO",
                    "ZM",
                    "LR",
                    "GQ",
                    "SR",
                    "MF",
                    "ST",
                    "AG",
                    "GY",
                    "ZA",
                    "MG",
                    "SN",
                    "BZ",
                    "CV",
                    "VG",
                    "BB",
                    "SL",
                    "TG",
                    "TZ",
                    "LS",
                    "EC",
                    "UY",
                    "BI",
                    "TT",
                    "AU",
                    "CG"
                  ]
                },
                "gameId": 401810005,
                "plays": [
                  {
                    "id": 40181000528
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46825335",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46825335"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46825335"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46825335"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/3dc2f5bc-6824-41f8-9640-3d82fdd7fbef/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825335"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/3dc2f5bc-6824-41f8-9640-3d82fdd7fbef/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825335"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46825335"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/3dc2f5bc-6824-41f8-9640-3d82fdd7fbef"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/3dc2f5bc-6824-41f8-9640-3d82fdd7fbef/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/a6831ef1-25dd-4d8a-bb53-3cece5344e9b/a6831ef1-25dd-4d8a-bb53-3cece5344e9b_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46825335&videoDSI=5451a00167f1c"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810005",
                    "guid": "72c15c44-fc43-3e87-b0ec-c14e2ec57f1a",
                    "description": "Utah Jazz @ Charlotte Hornets",
                    "eventId": 401810005,
                    "event": {
                      "id": 401810005,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Utah Jazz @ Charlotte Hornets",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810005"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810005"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 4564,
                    "type": "team",
                    "uid": "s:40~l:46~t:26",
                    "guid": "77cea2fb-1388-b7c8-d171-2e72b3aecbfb",
                    "description": "Utah Jazz",
                    "sportId": 46,
                    "teamId": 26,
                    "team": {
                      "id": 26,
                      "description": "Utah Jazz",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/utah/utah-jazz"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/utah/utah-jazz"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 187284,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4277811",
                    "guid": "2a6515dd-6770-7eac-2141-de08448a6905",
                    "description": "Collin Sexton",
                    "sportId": 46,
                    "athleteId": 4277811,
                    "athlete": {
                      "id": 4277811,
                      "description": "Collin Sexton",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4277811/collin-sexton"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4277811/collin-sexton"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 127884,
                    "type": "team",
                    "uid": "s:40~l:46~t:30",
                    "guid": "377633c2-0dd1-91a1-83c0-9ed2d0c00ea1",
                    "description": "Charlotte Hornets",
                    "sportId": 46,
                    "teamId": 30,
                    "team": {
                      "id": 30,
                      "description": "Charlotte Hornets",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/cha/charlotte-hornets"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/cha/charlotte-hornets"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 533657,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4433249",
                    "guid": "9005f423-8ebb-3459-acf9-31eb0eaaf801",
                    "description": "Moussa Diabate",
                    "sportId": 46,
                    "athleteId": 4433249,
                    "athlete": {
                      "id": 4433249,
                      "description": "Moussa Diabate",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4433249/moussa-diabate"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4433249/moussa-diabate"
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
                    "id": 187361,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4066383",
                    "guid": "f288347b-fa90-b31d-965a-98e20e1a8294",
                    "description": "Miles Bridges",
                    "sportId": 46,
                    "athleteId": 4066383,
                    "athlete": {
                      "id": 4066383,
                      "description": "Miles Bridges",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4066383/miles-bridges"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4066383/miles-bridges"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 168881,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4066336",
                    "guid": "87ff7f1b-e52a-b236-308c-878d12df8446",
                    "description": "Lauri Markkanen",
                    "sportId": 46,
                    "athleteId": 4066336,
                    "athlete": {
                      "id": 4066336,
                      "description": "Lauri Markkanen",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4066336/lauri-markkanen"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4066336/lauri-markkanen"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "72c15c44-fc43-3e87-b0ec-c14e2ec57f1a"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "77cea2fb-1388-b7c8-d171-2e72b3aecbfb"
                  },
                  {
                    "type": "guid",
                    "guid": "2a6515dd-6770-7eac-2141-de08448a6905"
                  },
                  {
                    "type": "guid",
                    "guid": "377633c2-0dd1-91a1-83c0-9ed2d0c00ea1"
                  },
                  {
                    "type": "guid",
                    "guid": "9005f423-8ebb-3459-acf9-31eb0eaaf801"
                  },
                  {
                    "type": "guid",
                    "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4"
                  },
                  {
                    "type": "guid",
                    "guid": "f288347b-fa90-b31d-965a-98e20e1a8294"
                  },
                  {
                    "type": "guid",
                    "guid": "87ff7f1b-e52a-b236-308c-878d12df8446"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Utah Jazz vs. Charlotte Hornets: Game Highlights) 2025/11/02 ESHEET",
                  "trackingId": "dm_20251102_NBA_utah_jazz_vs_charlotte_hornets_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810006",
              "uid": "s:40~l:46~e:401810006~c:401810006",
              "guid": "ef4d02a4-d978-302e-8c0f-6507584ba7a2",
              "date": "2025-11-02T23:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Atlanta Hawks at Cleveland Cavaliers",
              "shortName": "ATL @ CLE",
              "seriesSummary": "CLE leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810006/hawks-cavaliers",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810006",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810006",
              "location": "Rocket Mortgage FieldHouse",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810006/hawks-cavaliers",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 3,
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
                  "typeId": 6,
                  "priority": 2,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
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
                  "score": "109",
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
                  "record": "3-4",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 3
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 109
                    },
                    "pointsAgainst": {
                      "value": 117
                    },
                    "avgPointsFor": {
                      "value": 15.5714282989502
                    },
                    "avgPointsAgainst": {
                      "value": 16.7142848968506
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
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
                      "value": 8
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 0
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
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/atl.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/atl.png"
                },
                {
                  "id": "5",
                  "guid": "ec79ad1f-e6d2-7762-a2db-7fe97d35126b",
                  "uid": "s:40~l:46~t:5",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Cleveland Cavaliers",
                  "name": "Cavaliers",
                  "abbreviation": "CLE",
                  "location": "Cleveland",
                  "color": "860038",
                  "alternateColor": "bc945c",
                  "score": "117",
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
                  "record": "4-3",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 4
                    },
                    "losses": {
                      "value": 3
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
                      "value": 117
                    },
                    "pointsAgainst": {
                      "value": 109
                    },
                    "avgPointsFor": {
                      "value": 16.7142848968506
                    },
                    "avgPointsAgainst": {
                      "value": 15.5714282989502
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.571428596973419
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 2
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
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 6
                    },
                    "gamesBehind": {
                      "value": 2
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 1
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 2
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/cle.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/cle.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810006",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810006",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810006",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46825459,
                "dataSourceIdentifier": "aaa4e82ec53c1",
                "cerebroId": "69080ab1a421b770c08357c8",
                "pccId": "f932df2d-f064-4e95-9932-08e5e558d5c1",
                "source": "espn",
                "headline": "Atlanta Hawks vs. Cleveland Cavaliers: Game Highlights",
                "caption": "Atlanta Hawks vs. Cleveland Cavaliers: Game Highlights",
                "title": "Atlanta Hawks vs. Cleveland Cavaliers: Game Highlights",
                "description": "Atlanta Hawks vs. Cleveland Cavaliers: Game Highlights",
                "lastModified": "2025-11-03T01:58:03Z",
                "originalPublishDate": "2025-11-03T01:51:33Z",
                "premium": false,
                "syndicatable": true,
                "duration": 74,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T01:51:33Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "FJ",
                    "LS",
                    "BJ",
                    "GQ",
                    "BS",
                    "UY",
                    "VG",
                    "GT",
                    "BR",
                    "AS",
                    "HN",
                    "CF",
                    "PE",
                    "MX",
                    "LR",
                    "US",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "ZW",
                    "NI",
                    "ST",
                    "TZ",
                    "MG",
                    "GP",
                    "NG",
                    "TC",
                    "AR",
                    "KE",
                    "MS",
                    "CG",
                    "ER",
                    "CI",
                    "MW",
                    "GM",
                    "SV",
                    "LC",
                    "BZ",
                    "CM",
                    "GH",
                    "KM",
                    "KY",
                    "DO",
                    "PY",
                    "VC",
                    "JM",
                    "GF",
                    "RW",
                    "CD",
                    "ZM",
                    "SN",
                    "GY",
                    "GB",
                    "UK",
                    "BF",
                    "CL",
                    "MH",
                    "PW",
                    "AU",
                    "CV",
                    "UG",
                    "BM",
                    "CO",
                    "AI",
                    "GN",
                    "BQ",
                    "GW",
                    "GA",
                    "ML",
                    "PA",
                    "BB",
                    "ZA",
                    "FM",
                    "MZ",
                    "SX",
                    "EC",
                    "BW",
                    "BI",
                    "NZ",
                    "AW",
                    "KN",
                    "ET",
                    "HT",
                    "NE",
                    "SC",
                    "AO",
                    "TG",
                    "CU",
                    "GD",
                    "SL",
                    "TT",
                    "NA",
                    "VE",
                    "CR",
                    "RE",
                    "BO",
                    "SR",
                    "AM",
                    "MF",
                    "MQ",
                    "MU",
                    "AG",
                    "SZ",
                    "SS"
                  ]
                },
                "gameId": 401810006,
                "plays": [
                  {
                    "id": 40181000618
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46825459",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46825459"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46825459"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46825459"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/f932df2d-f064-4e95-9932-08e5e558d5c1/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825459"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/f932df2d-f064-4e95-9932-08e5e558d5c1/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825459"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46825459"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/f932df2d-f064-4e95-9932-08e5e558d5c1"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/f932df2d-f064-4e95-9932-08e5e558d5c1/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/c876fb1a-4731-48a1-af1b-f1401b5183d2/c876fb1a-4731-48a1-af1b-f1401b5183d2_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46825459&videoDSI=aaa4e82ec53c1"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810006",
                    "guid": "ef4d02a4-d978-302e-8c0f-6507584ba7a2",
                    "description": "Atlanta Hawks @ Cleveland Cavaliers",
                    "eventId": 401810006,
                    "event": {
                      "id": 401810006,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Atlanta Hawks @ Cleveland Cavaliers",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810006"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810006"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4358,
                    "type": "team",
                    "uid": "s:40~l:46~t:1",
                    "guid": "15096a54-f015-c987-5ec8-55afedf6272f",
                    "description": "Atlanta Hawks",
                    "sportId": 46,
                    "teamId": 1,
                    "team": {
                      "id": 1,
                      "description": "Atlanta Hawks",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/atl/atlanta-hawks"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/atl/atlanta-hawks"
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
                    "id": 168848,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3908809",
                    "guid": "6482ece5-f903-92e2-ffdd-13901fdd3a49",
                    "description": "Donovan Mitchell",
                    "sportId": 46,
                    "athleteId": 3908809,
                    "athlete": {
                      "id": 3908809,
                      "description": "Donovan Mitchell",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3908809/donovan-mitchell"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3908809/donovan-mitchell"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 492294,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4701230",
                    "guid": "a3bb4b30-41a4-3cb0-abea-2e1746695cb8",
                    "description": "Jalen Johnson",
                    "sportId": 46,
                    "athleteId": 4701230,
                    "athlete": {
                      "id": 4701230,
                      "description": "Jalen Johnson",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4701230/jalen-johnson"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4701230/jalen-johnson"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4408,
                    "type": "team",
                    "uid": "s:40~l:46~t:5",
                    "guid": "ec79ad1f-e6d2-7762-a2db-7fe97d35126b",
                    "description": "Cleveland Cavaliers",
                    "sportId": 46,
                    "teamId": 5,
                    "team": {
                      "id": 5,
                      "description": "Cleveland Cavaliers",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "id": 533656,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4869342",
                    "guid": "7b066993-61be-35fd-9070-c1b9a57c7b31",
                    "description": "Dyson Daniels",
                    "sportId": 46,
                    "athleteId": 4869342,
                    "athlete": {
                      "id": 4869342,
                      "description": "Dyson Daniels",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4869342/dyson-daniels"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4869342/dyson-daniels"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "ef4d02a4-d978-302e-8c0f-6507584ba7a2"
                  },
                  {
                    "type": "guid",
                    "guid": "15096a54-f015-c987-5ec8-55afedf6272f"
                  },
                  {
                    "type": "guid",
                    "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4"
                  },
                  {
                    "type": "guid",
                    "guid": "6482ece5-f903-92e2-ffdd-13901fdd3a49"
                  },
                  {
                    "type": "guid",
                    "guid": "a3bb4b30-41a4-3cb0-abea-2e1746695cb8"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "ec79ad1f-e6d2-7762-a2db-7fe97d35126b"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  },
                  {
                    "type": "guid",
                    "guid": "7b066993-61be-35fd-9070-c1b9a57c7b31"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Atlanta Hawks vs. Cleveland Cavaliers: Game Highlights) 2025/11/02 ESHEET",
                  "trackingId": "dm_20251102_NBA_atlanta_hawks_vs_cleveland_cavaliers_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810007",
              "uid": "s:40~l:46~e:401810007~c:401810007",
              "guid": "861248e3-cc8d-3028-8eba-d69ee6b850e7",
              "date": "2025-11-02T23:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Memphis Grizzlies at Toronto Raptors",
              "shortName": "MEM @ TOR",
              "seriesSummary": "TOR leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810007/grizzlies-raptors",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810007",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810007",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810007/grizzlies-raptors",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 722,
                  "broadcastId": 722,
                  "name": "Sportsnet",
                  "shortName": "Sportsnet",
                  "callLetters": "Sportsnet",
                  "station": "Sportsnet",
                  "lang": "en",
                  "region": "us",
                  "slug": "sportsnet"
                },
                {
                  "typeId": 1,
                  "priority": 3,
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
                  "priority": 2,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
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
                  "score": "104",
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
                  "record": "3-4",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 3
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 104
                    },
                    "pointsAgainst": {
                      "value": 117
                    },
                    "avgPointsFor": {
                      "value": 14.8571424484253
                    },
                    "avgPointsAgainst": {
                      "value": 16.7142848968506
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
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
                      "value": -2
                    },
                    "playoffSeed": {
                      "value": 10
                    },
                    "gamesBehind": {
                      "value": 4
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 2
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mem.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/mem.png"
                },
                {
                  "id": "28",
                  "guid": "5a9c33b8-63fd-ff34-a833-925fe89320a6",
                  "uid": "s:40~l:46~t:28",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Toronto Raptors",
                  "name": "Raptors",
                  "abbreviation": "TOR",
                  "location": "Toronto",
                  "color": "d91244",
                  "alternateColor": "000000",
                  "score": "117",
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
                  "record": "3-4",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 3
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 117
                    },
                    "pointsAgainst": {
                      "value": 104
                    },
                    "avgPointsFor": {
                      "value": 16.7142848968506
                    },
                    "avgPointsAgainst": {
                      "value": 14.8571424484253
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 0
                    },
                    "divisionLosses": {
                      "value": 0
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0
                    },
                    "streak": {
                      "value": 2
                    },
                    "playoffSeed": {
                      "value": 8
                    },
                    "gamesBehind": {
                      "value": 3
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 1
                    },
                    "homeLosses": {
                      "value": 2
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 2
                    },
                    "roadLosses": {
                      "value": 2
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810007",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810007",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810007",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46825254,
                "dataSourceIdentifier": "9acc62055d26a",
                "cerebroId": "690806c9c66a8438e7af668a",
                "pccId": "df490c2e-a063-4a8c-8eed-02b839b52587",
                "source": "espn",
                "headline": "Memphis Grizzlies vs. Toronto Raptors: Game Highlights",
                "caption": "Memphis Grizzlies vs. Toronto Raptors: Game Highlights",
                "title": "Memphis Grizzlies vs. Toronto Raptors: Game Highlights",
                "description": "Memphis Grizzlies vs. Toronto Raptors: Game Highlights",
                "lastModified": "2025-11-03T01:43:40Z",
                "originalPublishDate": "2025-11-03T01:34:57Z",
                "premium": false,
                "syndicatable": true,
                "duration": 73,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T01:34:57Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "BF",
                    "ZW",
                    "PA",
                    "ML",
                    "GD",
                    "MU",
                    "BQ",
                    "US",
                    "AS",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "NG",
                    "SS",
                    "KE",
                    "BR",
                    "UG",
                    "MH",
                    "GH",
                    "RW",
                    "ET",
                    "CO",
                    "AO",
                    "HT",
                    "MW",
                    "CM",
                    "KY",
                    "HN",
                    "CR",
                    "BM",
                    "GW",
                    "MX",
                    "BS",
                    "NA",
                    "KM",
                    "SZ",
                    "BO",
                    "SX",
                    "GN",
                    "VC",
                    "BJ",
                    "GB",
                    "UK",
                    "MQ",
                    "TC",
                    "BW",
                    "JM",
                    "MS",
                    "NE",
                    "PE",
                    "AM",
                    "AR",
                    "CF",
                    "GM",
                    "NZ",
                    "GT",
                    "GP",
                    "LC",
                    "SV",
                    "ER",
                    "KN",
                    "CL",
                    "CD",
                    "MZ",
                    "PW",
                    "AI",
                    "AW",
                    "PY",
                    "CI",
                    "SC",
                    "CU",
                    "GF",
                    "GA",
                    "RE",
                    "NI",
                    "FM",
                    "FJ",
                    "VE",
                    "DO",
                    "ZM",
                    "LR",
                    "GQ",
                    "SR",
                    "MF",
                    "ST",
                    "AG",
                    "GY",
                    "ZA",
                    "MG",
                    "SN",
                    "BZ",
                    "CV",
                    "VG",
                    "BB",
                    "SL",
                    "TG",
                    "TZ",
                    "LS",
                    "EC",
                    "UY",
                    "BI",
                    "TT",
                    "AU",
                    "CG"
                  ]
                },
                "gameId": 401810007,
                "plays": [
                  {
                    "id": 401810007134
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46825254",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46825254"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46825254"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46825254"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/df490c2e-a063-4a8c-8eed-02b839b52587/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825254"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/df490c2e-a063-4a8c-8eed-02b839b52587/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825254"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46825254"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/df490c2e-a063-4a8c-8eed-02b839b52587"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/df490c2e-a063-4a8c-8eed-02b839b52587/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/42ead2da-81a3-4653-8aa3-03725df7bacb/42ead2da-81a3-4653-8aa3-03725df7bacb_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46825254&videoDSI=9acc62055d26a"
                  }
                },
                "categories": [
                  {
                    "id": 384275,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4395625",
                    "guid": "92d6ee44-1fcc-f058-5b21-9c8dc7d2efde",
                    "description": "RJ Barrett",
                    "sportId": 46,
                    "athleteId": 4395625,
                    "athlete": {
                      "id": 4395625,
                      "description": "RJ Barrett",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395625/rj-barrett"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395625/rj-barrett"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810007",
                    "guid": "861248e3-cc8d-3028-8eba-d69ee6b850e7",
                    "description": "Memphis Grizzlies @ Toronto Raptors",
                    "eventId": 401810007,
                    "event": {
                      "id": 401810007,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Memphis Grizzlies @ Toronto Raptors",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810007"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810007"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 187408,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4277961",
                    "guid": "dbe0e9e5-0046-c414-000b-f4e629b08f5d",
                    "description": "Jaren Jackson Jr",
                    "sportId": 46,
                    "athleteId": 4277961,
                    "athlete": {
                      "id": 4277961,
                      "description": "Jaren Jackson Jr",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4277961/jaren-jackson-jr"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4277961/jaren-jackson-jr"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4584,
                    "type": "team",
                    "uid": "s:40~l:46~t:29",
                    "guid": "af5d4942-aeb5-2d07-2a8a-f70b54617e51",
                    "description": "Memphis Grizzlies",
                    "sportId": 46,
                    "teamId": 29,
                    "team": {
                      "id": 29,
                      "description": "Memphis Grizzlies",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/mem/memphis-grizzlies"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/mem/memphis-grizzlies"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4469,
                    "type": "team",
                    "uid": "s:40~l:46~t:28",
                    "guid": "5a9c33b8-63fd-ff34-a833-925fe89320a6",
                    "description": "Toronto Raptors",
                    "sportId": 46,
                    "teamId": 28,
                    "team": {
                      "id": 28,
                      "description": "Toronto Raptors",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/tor/toronto-raptors"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/tor/toronto-raptors"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711828,
                    "type": "editorialindicator",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7",
                    "description": "4 Star Rating"
                  },
                  {
                    "id": 533680,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4397227",
                    "guid": "1de2239e-92a3-8e4e-4320-cc5143dd91ed",
                    "description": "Vince Williams Jr",
                    "sportId": 46,
                    "athleteId": 4397227,
                    "athlete": {
                      "id": 4397227,
                      "description": "Vince Williams Jr",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4397227/vince-williams-jr"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4397227/vince-williams-jr"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "92d6ee44-1fcc-f058-5b21-9c8dc7d2efde"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "861248e3-cc8d-3028-8eba-d69ee6b850e7"
                  },
                  {
                    "type": "guid",
                    "guid": "dbe0e9e5-0046-c414-000b-f4e629b08f5d"
                  },
                  {
                    "type": "guid",
                    "guid": "af5d4942-aeb5-2d07-2a8a-f70b54617e51"
                  },
                  {
                    "type": "guid",
                    "guid": "5a9c33b8-63fd-ff34-a833-925fe89320a6"
                  },
                  {
                    "type": "guid",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7"
                  },
                  {
                    "type": "guid",
                    "guid": "1de2239e-92a3-8e4e-4320-cc5143dd91ed"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Memphis Grizzlies vs. Toronto Raptors: Game Highlights) 2025/11/02 ESHEET",
                  "trackingId": "dm_20251102_NBA_memphis_grizzlies_vs_toronto_raptors_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810008",
              "uid": "s:40~l:46~e:401810008~c:401810008",
              "guid": "72c782b2-3908-339a-91af-ab5590555cac",
              "date": "2025-11-03T00:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Chicago Bulls at New York Knicks",
              "shortName": "CHI @ NY",
              "seriesSummary": "Series tied 1-1",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810008/bulls-knicks",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810008",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810008",
              "location": "Madison Square Garde",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810008/bulls-knicks",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "12:00",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 1125,
                  "broadcastId": 1125,
                  "name": "Chicago Sports Network",
                  "shortName": "CHSN",
                  "callLetters": "CHSN",
                  "station": "CHSN",
                  "lang": "en",
                  "region": "us",
                  "slug": "chsn"
                },
                {
                  "typeId": 1,
                  "priority": 2,
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
              "fullStatus": {
                "clock": 720,
                "displayClock": "12:00",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
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
                  "score": "116",
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
                  "record": "5-1",
                  "records": [],
                  "group": "2",
                  "recordStats": {
                    "wins": {
                      "value": 5
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
                      "value": 2
                    },
                    "pointsFor": {
                      "value": 116
                    },
                    "pointsAgainst": {
                      "value": 128
                    },
                    "avgPointsFor": {
                      "value": 19.3333339691162
                    },
                    "avgPointsAgainst": {
                      "value": 21.3333339691162
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.833333313465118
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
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
                      "value": 2
                    },
                    "gamesBehind": {
                      "value": 0
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 4
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 1
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/chi.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/chi.png"
                },
                {
                  "id": "18",
                  "guid": "61719eb2-11c3-4e3d-90c3-0a1319fd850b",
                  "uid": "s:40~l:46~t:18",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "New York Knicks",
                  "name": "Knicks",
                  "abbreviation": "NY",
                  "location": "New York",
                  "color": "1d428a",
                  "alternateColor": "f58426",
                  "score": "128",
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
                  "record": "3-3",
                  "records": [],
                  "group": "1",
                  "recordStats": {
                    "wins": {
                      "value": 3
                    },
                    "losses": {
                      "value": 3
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
                      "value": 0
                    },
                    "pointsFor": {
                      "value": 128
                    },
                    "pointsAgainst": {
                      "value": 116
                    },
                    "avgPointsFor": {
                      "value": 21.3333339691162
                    },
                    "avgPointsAgainst": {
                      "value": 19.3333339691162
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.5
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
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
                      "value": 1
                    },
                    "playoffSeed": {
                      "value": 7
                    },
                    "gamesBehind": {
                      "value": 2
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 3
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 3
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/ny.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/ny.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810008",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810008",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810008",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46825900,
                "dataSourceIdentifier": "df62590200022",
                "cerebroId": "6908150f4e62f67fb8df84d2",
                "pccId": "2a07b722-9fcd-4d86-8cd2-b5ca0dac46fe",
                "source": "espn",
                "headline": "Chicago Bulls vs. New York Knicks: Game Highlights",
                "caption": "Chicago Bulls vs. New York Knicks: Game Highlights",
                "title": "Chicago Bulls vs. New York Knicks: Game Highlights",
                "description": "Chicago Bulls vs. New York Knicks: Game Highlights",
                "lastModified": "2025-11-03T02:42:34Z",
                "originalPublishDate": "2025-11-03T02:35:51Z",
                "premium": false,
                "syndicatable": true,
                "duration": 74,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T02:35:51Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "UM",
                    "BR",
                    "GW",
                    "MG",
                    "CM",
                    "GP",
                    "TG",
                    "CR",
                    "CU",
                    "PA",
                    "GT",
                    "PE",
                    "LR",
                    "ST",
                    "LS",
                    "GA",
                    "MF",
                    "BZ",
                    "PW",
                    "SZ",
                    "VG",
                    "TT",
                    "KM",
                    "MH",
                    "SN",
                    "MU",
                    "SL",
                    "BO",
                    "GF",
                    "MS",
                    "HN",
                    "CG",
                    "GU",
                    "JM",
                    "GY",
                    "CD",
                    "BI",
                    "MW",
                    "MP",
                    "SR",
                    "GM",
                    "ZM",
                    "AO",
                    "BF",
                    "SX",
                    "AI",
                    "GN",
                    "GD",
                    "AR",
                    "CI",
                    "AS",
                    "TC",
                    "NZ",
                    "HT",
                    "CF",
                    "VE",
                    "AM",
                    "ZW",
                    "AW",
                    "KE",
                    "CV",
                    "ER",
                    "TZ",
                    "ZA",
                    "ET",
                    "EC",
                    "BM",
                    "KY",
                    "BW",
                    "GB",
                    "UK",
                    "FM",
                    "AU",
                    "NE",
                    "NG",
                    "US",
                    "PR",
                    "VI",
                    "UG",
                    "BB",
                    "BQ",
                    "UY",
                    "FJ",
                    "GH",
                    "SS",
                    "SV",
                    "MQ",
                    "VC",
                    "NI",
                    "GQ",
                    "MX",
                    "KN",
                    "AG",
                    "RW",
                    "ML",
                    "CO",
                    "RE",
                    "PY",
                    "DO",
                    "CL",
                    "BS",
                    "SC",
                    "NA",
                    "BJ",
                    "LC",
                    "MZ"
                  ]
                },
                "gameId": 401810008,
                "plays": [
                  {
                    "id": 40181000837
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46825900",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46825900"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46825900"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46825900"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/2a07b722-9fcd-4d86-8cd2-b5ca0dac46fe/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825900"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/2a07b722-9fcd-4d86-8cd2-b5ca0dac46fe/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46825900"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46825900"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/2a07b722-9fcd-4d86-8cd2-b5ca0dac46fe"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/2a07b722-9fcd-4d86-8cd2-b5ca0dac46fe/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/b2a42765-2b62-4b47-b426-1c99c2f54fbe/b2a42765-2b62-4b47-b426-1c99c2f54fbe_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46825900&videoDSI=df62590200022"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 168962,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3934719",
                    "guid": "31ec117d-6e14-d4f0-9414-9d2467197179",
                    "description": "OG Anunoby",
                    "sportId": 46,
                    "athleteId": 3934719,
                    "athlete": {
                      "id": 3934719,
                      "description": "OG Anunoby",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3934719/og-anunoby"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3934719/og-anunoby"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4293,
                    "type": "team",
                    "uid": "s:40~l:46~t:18",
                    "guid": "61719eb2-11c3-4e3d-90c3-0a1319fd850b",
                    "description": "New York Knicks",
                    "sportId": 46,
                    "teamId": 18,
                    "team": {
                      "id": 18,
                      "description": "New York Knicks",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/ny/new-york-knicks"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/ny/new-york-knicks"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 187348,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3934672",
                    "guid": "89519c75-cf8a-38e7-1151-b6247a2d4535",
                    "description": "Jalen Brunson",
                    "sportId": 46,
                    "athleteId": 3934672,
                    "athlete": {
                      "id": 3934672,
                      "description": "Jalen Brunson",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3934672/jalen-brunson"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3934672/jalen-brunson"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4392,
                    "type": "team",
                    "uid": "s:40~l:46~t:4",
                    "guid": "e588ccf1-ba03-ea43-c34c-9a9c8d1895ca",
                    "description": "Chicago Bulls",
                    "sportId": 46,
                    "teamId": 4,
                    "team": {
                      "id": 4,
                      "description": "Chicago Bulls",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/chi/chicago-bulls"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/chi/chicago-bulls"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810008",
                    "guid": "72c782b2-3908-339a-91af-ab5590555cac",
                    "description": "Chicago Bulls @ New York Knicks",
                    "eventId": 401810008,
                    "event": {
                      "id": 401810008,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Chicago Bulls @ New York Knicks",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810008"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810008"
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
                    "id": 492186,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4871145",
                    "guid": "501894e4-c167-38d3-8dda-8412203e3fcf",
                    "description": "Josh Giddey",
                    "sportId": 46,
                    "athleteId": 4871145,
                    "athlete": {
                      "id": 4871145,
                      "description": "Josh Giddey",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4871145/josh-giddey"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4871145/josh-giddey"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "31ec117d-6e14-d4f0-9414-9d2467197179"
                  },
                  {
                    "type": "guid",
                    "guid": "61719eb2-11c3-4e3d-90c3-0a1319fd850b"
                  },
                  {
                    "type": "guid",
                    "guid": "89519c75-cf8a-38e7-1151-b6247a2d4535"
                  },
                  {
                    "type": "guid",
                    "guid": "e588ccf1-ba03-ea43-c34c-9a9c8d1895ca"
                  },
                  {
                    "type": "guid",
                    "guid": "72c782b2-3908-339a-91af-ab5590555cac"
                  },
                  {
                    "type": "guid",
                    "guid": "26380a67-7938-32a0-9c82-33abab9f7ad4"
                  },
                  {
                    "type": "guid",
                    "guid": "501894e4-c167-38d3-8dda-8412203e3fcf"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Chicago Bulls vs. New York Knicks: Game Highlights) 2025/11/03 ESHEET",
                  "trackingId": "dm_20251103_NBA_chicago_bulls_vs_new_york_knicks_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810009",
              "uid": "s:40~l:46~e:401810009~c:401810009",
              "guid": "257fba67-7a5c-31b5-800a-50260fe2c636",
              "date": "2025-11-03T01:00:00Z",
              "timeValid": true,
              "recent": false,
              "name": "San Antonio Spurs at Phoenix Suns",
              "shortName": "SA @ PHX",
              "seriesSummary": "PHX leads series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810009/spurs-suns",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810009",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810009",
              "location": "Talking Stick Resort Arena",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810009/spurs-suns",
              "status": "post",
              "summary": "Final",
              "period": 4,
              "clock": "0.0",
              "broadcasts": [
                {
                  "typeId": 1,
                  "priority": 1,
                  "type": "TV",
                  "isNational": false,
                  "broadcasterId": 966,
                  "broadcastId": 966,
                  "name": "Arizona's Family 3TV",
                  "shortName": "Arizona's Family 3TV",
                  "callLetters": "Arizona's Family 3TV",
                  "station": "Arizona's Family 3TV",
                  "lang": "en",
                  "region": "us",
                  "slug": "arizonas-family-3tv"
                },
                {
                  "typeId": 1,
                  "priority": 4,
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
                  "typeId": 4,
                  "priority": 2,
                  "type": "Streaming",
                  "isNational": false,
                  "broadcasterId": 1193,
                  "broadcastId": 1193,
                  "name": "Suns Live",
                  "shortName": "Suns Live",
                  "callLetters": "Suns Live",
                  "station": "Suns Live",
                  "lang": "en",
                  "region": "us",
                  "slug": "suns-live"
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
                }
              },
              "competitors": [
                {
                  "id": "24",
                  "guid": "8aef8547-32f5-0943-a1de-e734567674cc",
                  "uid": "s:40~l:46~t:24",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "San Antonio Spurs",
                  "name": "Spurs",
                  "abbreviation": "SA",
                  "location": "San Antonio",
                  "color": "000000",
                  "alternateColor": "c4ced4",
                  "score": "118",
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
                  "record": "5-1",
                  "records": [],
                  "group": "10",
                  "recordStats": {
                    "wins": {
                      "value": 5
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
                      "value": 2
                    },
                    "pointsFor": {
                      "value": 118
                    },
                    "pointsAgainst": {
                      "value": 130
                    },
                    "avgPointsFor": {
                      "value": 19.6666660308838
                    },
                    "avgPointsAgainst": {
                      "value": 21.6666660308838
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.833333313465118
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 2
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
                      "value": 2
                    },
                    "gamesBehind": {
                      "value": 1.5
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 3
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 2
                    },
                    "roadLosses": {
                      "value": 1
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/sa.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/sa.png"
                },
                {
                  "id": "21",
                  "guid": "c6eade89-5971-0e84-8ccb-cd91482b2b50",
                  "uid": "s:40~l:46~t:21",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Phoenix Suns",
                  "name": "Suns",
                  "abbreviation": "PHX",
                  "location": "Phoenix",
                  "color": "29127a",
                  "alternateColor": "e56020",
                  "score": "130",
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
                  "record": "3-4",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 3
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
                      "value": -0.5
                    },
                    "pointsFor": {
                      "value": 130
                    },
                    "pointsAgainst": {
                      "value": 118
                    },
                    "avgPointsFor": {
                      "value": 18.5714282989502
                    },
                    "avgPointsAgainst": {
                      "value": 16.8571434020996
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.428571432828903
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 1
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
                      "value": 11
                    },
                    "gamesBehind": {
                      "value": 4
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 3
                    },
                    "homeLosses": {
                      "value": 1
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 0
                    },
                    "roadLosses": {
                      "value": 3
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phx.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/phx.png"
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810009",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810009",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810009",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46826539,
                "dataSourceIdentifier": "4c01afd76cc3b",
                "cerebroId": "690823d0c66a8438e7af849f",
                "pccId": "4915615a-b4ea-4a0f-80fd-ee08e51147f5",
                "source": "espn",
                "headline": "San Antonio Spurs vs. Phoenix Suns: Game Highlights",
                "caption": "San Antonio Spurs vs. Phoenix Suns: Game Highlights",
                "title": "San Antonio Spurs vs. Phoenix Suns: Game Highlights",
                "description": "San Antonio Spurs vs. Phoenix Suns: Game Highlights",
                "lastModified": "2025-11-03T04:32:29Z",
                "originalPublishDate": "2025-11-03T03:38:47Z",
                "premium": false,
                "syndicatable": true,
                "duration": 71,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T03:38:47Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "BF",
                    "ZW",
                    "PA",
                    "ML",
                    "GD",
                    "MU",
                    "BQ",
                    "US",
                    "AS",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "NG",
                    "SS",
                    "KE",
                    "BR",
                    "UG",
                    "MH",
                    "GH",
                    "RW",
                    "ET",
                    "CO",
                    "AO",
                    "HT",
                    "MW",
                    "CM",
                    "KY",
                    "HN",
                    "CR",
                    "BM",
                    "GW",
                    "MX",
                    "BS",
                    "NA",
                    "KM",
                    "SZ",
                    "BO",
                    "SX",
                    "GN",
                    "VC",
                    "BJ",
                    "GB",
                    "UK",
                    "MQ",
                    "TC",
                    "BW",
                    "JM",
                    "MS",
                    "NE",
                    "PE",
                    "AM",
                    "AR",
                    "CF",
                    "GM",
                    "NZ",
                    "GT",
                    "GP",
                    "LC",
                    "SV",
                    "ER",
                    "KN",
                    "CL",
                    "CD",
                    "MZ",
                    "PW",
                    "AI",
                    "AW",
                    "PY",
                    "CI",
                    "SC",
                    "CU",
                    "GF",
                    "GA",
                    "RE",
                    "NI",
                    "FM",
                    "FJ",
                    "VE",
                    "DO",
                    "ZM",
                    "LR",
                    "GQ",
                    "SR",
                    "MF",
                    "ST",
                    "AG",
                    "GY",
                    "ZA",
                    "MG",
                    "SN",
                    "BZ",
                    "CV",
                    "VG",
                    "BB",
                    "SL",
                    "TG",
                    "TZ",
                    "LS",
                    "EC",
                    "UY",
                    "BI",
                    "TT",
                    "AU",
                    "CG"
                  ]
                },
                "gameId": 401810009,
                "plays": [
                  {
                    "id": 40181000924
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46826539",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46826539"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46826539"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46826539"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/4915615a-b4ea-4a0f-80fd-ee08e51147f5/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46826539"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/4915615a-b4ea-4a0f-80fd-ee08e51147f5/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46826539"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46826539"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/4915615a-b4ea-4a0f-80fd-ee08e51147f5"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/4915615a-b4ea-4a0f-80fd-ee08e51147f5/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d/d17a6e54-c61d-4ccd-800e-c08ddf8e8c2d_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46826539&videoDSI=4c01afd76cc3b"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 140940,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3136193",
                    "guid": "493046d7-fa60-d8a1-1397-b9a6dca8dedf",
                    "description": "Devin Booker",
                    "sportId": 46,
                    "athleteId": 3136193,
                    "athlete": {
                      "id": 3136193,
                      "description": "Devin Booker",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3136193/devin-booker"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3136193/devin-booker"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 187341,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3135045",
                    "guid": "fedd8adf-a9cc-d643-0130-ff502fc58389",
                    "description": "Grayson Allen",
                    "sportId": 46,
                    "athleteId": 3135045,
                    "athlete": {
                      "id": 3135045,
                      "description": "Grayson Allen",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3135045/grayson-allen"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3135045/grayson-allen"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 384252,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4395723",
                    "guid": "691dfac0-35e1-b597-c503-f0211c8f7f6f",
                    "description": "Keldon Johnson",
                    "sportId": 46,
                    "athleteId": 4395723,
                    "athlete": {
                      "id": 4395723,
                      "description": "Keldon Johnson",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395723/keldon-johnson"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4395723/keldon-johnson"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711828,
                    "type": "editorialindicator",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7",
                    "description": "4 Star Rating"
                  },
                  {
                    "id": 4548,
                    "type": "team",
                    "uid": "s:40~l:46~t:24",
                    "guid": "8aef8547-32f5-0943-a1de-e734567674cc",
                    "description": "San Antonio Spurs",
                    "sportId": 46,
                    "teamId": 24,
                    "team": {
                      "id": 24,
                      "description": "San Antonio Spurs",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/sa/san-antonio-spurs"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/sa/san-antonio-spurs"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 633090,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4845367",
                    "guid": "26c7892b-12d0-3b1d-9645-f881921a1a20",
                    "description": "Stephon Castle",
                    "sportId": 46,
                    "athleteId": 4845367,
                    "athlete": {
                      "id": 4845367,
                      "description": "Stephon Castle",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4845367/stephon-castle"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4845367/stephon-castle"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810009",
                    "guid": "257fba67-7a5c-31b5-800a-50260fe2c636",
                    "description": "San Antonio Spurs @ Phoenix Suns",
                    "eventId": 401810009,
                    "event": {
                      "id": 401810009,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "San Antonio Spurs @ Phoenix Suns",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810009"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810009"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4644,
                    "type": "team",
                    "uid": "s:40~l:46~t:21",
                    "guid": "c6eade89-5971-0e84-8ccb-cd91482b2b50",
                    "description": "Phoenix Suns",
                    "sportId": 46,
                    "teamId": 21,
                    "team": {
                      "id": 21,
                      "description": "Phoenix Suns",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/phx/phoenix-suns"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/phx/phoenix-suns"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "493046d7-fa60-d8a1-1397-b9a6dca8dedf"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "fedd8adf-a9cc-d643-0130-ff502fc58389"
                  },
                  {
                    "type": "guid",
                    "guid": "691dfac0-35e1-b597-c503-f0211c8f7f6f"
                  },
                  {
                    "type": "guid",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7"
                  },
                  {
                    "type": "guid",
                    "guid": "8aef8547-32f5-0943-a1de-e734567674cc"
                  },
                  {
                    "type": "guid",
                    "guid": "26c7892b-12d0-3b1d-9645-f881921a1a20"
                  },
                  {
                    "type": "guid",
                    "guid": "257fba67-7a5c-31b5-800a-50260fe2c636"
                  },
                  {
                    "type": "guid",
                    "guid": "c6eade89-5971-0e84-8ccb-cd91482b2b50"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (San Antonio Spurs vs. Phoenix Suns: Game Highlights) 2025/11/03 ESHEET",
                  "trackingId": "dm_20251103_NBA_san_antonio_spurs_vs_phoenix_suns_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            },
            {
              "id": "401810010",
              "uid": "s:40~l:46~e:401810010~c:401810010",
              "guid": "2e57a569-466b-3f16-9cdf-10048211efdf",
              "date": "2025-11-03T02:30:00Z",
              "timeValid": true,
              "recent": false,
              "name": "Miami Heat at Los Angeles Lakers",
              "shortName": "MIA @ LAL",
              "seriesSummary": "LAL lead series 1-0",
              "links": [
                {
                  "rel": [
                    "summary",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/game/_/gameId/401810010/heat-lakers",
                  "text": "Gamecast"
                },
                {
                  "rel": [
                    "boxscore",
                    "desktop",
                    "event"
                  ],
                  "href": "https://www.espn.com/nba/boxscore/_/gameId/401810010",
                  "text": "Box Score"
                }
              ],
              "gamecastAvailable": true,
              "playByPlayAvailable": true,
              "commentaryAvailable": false,
              "wallclockAvailable": true,
              "fauxcastAvailable": true,
              "onWatch": false,
              "competitionId": "401810010",
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
              "week": 2,
              "weekText": "Week 2",
              "link": "https://www.espn.com/nba/game/_/gameId/401810010/heat-lakers",
              "status": "post",
              "summary": "Final",
              "period": 4,
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
              "fullStatus": {
                "clock": 0,
                "displayClock": "0.0",
                "period": 4,
                "displayPeriod": "4th",
                "type": {
                  "id": "3",
                  "name": "STATUS_FINAL",
                  "state": "post",
                  "completed": true,
                  "description": "Final",
                  "detail": "Final",
                  "shortDetail": "Final"
                }
              },
              "competitors": [
                {
                  "id": "14",
                  "guid": "81e3212c-30ef-9b1b-5edb-453b13ff265a",
                  "uid": "s:40~l:46~t:14",
                  "type": "team",
                  "order": 1,
                  "homeAway": "away",
                  "winner": false,
                  "displayName": "Miami Heat",
                  "name": "Heat",
                  "abbreviation": "MIA",
                  "location": "Miami",
                  "color": "98002e",
                  "alternateColor": "000000",
                  "score": "120",
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
                  "record": "3-3",
                  "records": [],
                  "group": "9",
                  "recordStats": {
                    "wins": {
                      "value": 3
                    },
                    "losses": {
                      "value": 3
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
                      "value": 0
                    },
                    "pointsFor": {
                      "value": 120
                    },
                    "pointsAgainst": {
                      "value": 130
                    },
                    "avgPointsFor": {
                      "value": 20
                    },
                    "avgPointsAgainst": {
                      "value": 21.6666660308838
                    },
                    "gamesPlayed": {
                      "value": 6
                    },
                    "winPercent": {
                      "value": 0.5
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 1
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
                      "value": 6
                    },
                    "gamesBehind": {
                      "value": 2
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
                    },
                    "homeLosses": {
                      "value": 0
                    },
                    "homeTies": {
                      "value": 0
                    },
                    "roadWins": {
                      "value": 1
                    },
                    "roadLosses": {
                      "value": 3
                    },
                    "roadTies": {
                      "value": 0
                    }
                  },
                  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mia.png",
                  "logoDark": "https://a.espncdn.com/i/teamlogos/nba/500-dark/scoreboard/mia.png"
                },
                {
                  "id": "13",
                  "guid": "2876e98b-b9bc-2920-4319-46e6943f8be4",
                  "uid": "s:40~l:46~t:13",
                  "type": "team",
                  "order": 0,
                  "homeAway": "home",
                  "winner": true,
                  "displayName": "Los Angeles Lakers",
                  "name": "Lakers",
                  "abbreviation": "LAL",
                  "location": "Los Angeles",
                  "color": "552583",
                  "alternateColor": "fdb927",
                  "score": "130",
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
                  "record": "5-2",
                  "records": [],
                  "group": "4",
                  "recordStats": {
                    "wins": {
                      "value": 5
                    },
                    "losses": {
                      "value": 2
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
                      "value": 130
                    },
                    "pointsAgainst": {
                      "value": 120
                    },
                    "avgPointsFor": {
                      "value": 18.5714282989502
                    },
                    "avgPointsAgainst": {
                      "value": 17.1428565979004
                    },
                    "gamesPlayed": {
                      "value": 7
                    },
                    "winPercent": {
                      "value": 0.714285731315613
                    },
                    "leagueWinPercent": {
                      "value": 0
                    },
                    "divisionWins": {
                      "value": 1
                    },
                    "divisionLosses": {
                      "value": 1
                    },
                    "divisionTies": {
                      "value": 0
                    },
                    "divisionWinPercent": {
                      "value": 0.5
                    },
                    "streak": {
                      "value": 3
                    },
                    "playoffSeed": {
                      "value": 3
                    },
                    "gamesBehind": {
                      "value": 2
                    },
                    "conferenceWins": {
                      "value": 0
                    },
                    "conferenceLosses": {
                      "value": 0
                    },
                    "conferenceTies": {
                      "value": 0
                    },
                    "homeWins": {
                      "value": 2
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
                      "value": 0
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
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810010",
                  "text": "Gamecast",
                  "shortText": "Summary"
                },
                {
                  "rel": [
                    "boxscore",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810010",
                  "text": "Box Score",
                  "shortText": "Box Score"
                },
                {
                  "rel": [
                    "gamecast",
                    "sportscenter",
                    "app",
                    "event"
                  ],
                  "href": "sportscenter://x-callback-url/showGame?sportName=basketball&leagueAbbrev=nba&gameId=401810010",
                  "text": "Gamecast",
                  "shortText": "Gamecast"
                }
              ],
              "video": {
                "id": 46827452,
                "dataSourceIdentifier": "548399a7885ac",
                "cerebroId": "69083c76a421b770c0837b02",
                "pccId": "3476f2db-bbca-405b-a8b2-16ddd86ed416",
                "source": "espn",
                "headline": "Miami Heat vs. Los Angeles Lakers: Game Highlights",
                "caption": "Miami Heat vs. Los Angeles Lakers: Game Highlights",
                "title": "Miami Heat vs. Los Angeles Lakers: Game Highlights",
                "description": "Miami Heat vs. Los Angeles Lakers: Game Highlights",
                "lastModified": "2025-11-03T05:25:13Z",
                "originalPublishDate": "2025-11-03T05:23:57Z",
                "premium": false,
                "syndicatable": true,
                "duration": 68,
                "videoRatio": "16:9,9:16",
                "timeRestrictions": {
                  "embargoDate": "2025-11-03T05:23:57Z",
                  "expirationDate": "2026-07-31T04:00:00Z"
                },
                "deviceRestrictions": {
                  "type": "whitelist",
                  "devices": [
                    "desktop",
                    "ipad",
                    "settop",
                    "handset",
                    "tablet"
                  ]
                },
                "geoRestrictions": {
                  "type": "whitelist",
                  "countries": [
                    "FJ",
                    "LS",
                    "BJ",
                    "GQ",
                    "BS",
                    "UY",
                    "VG",
                    "GT",
                    "BR",
                    "AS",
                    "HN",
                    "CF",
                    "PE",
                    "MX",
                    "LR",
                    "US",
                    "GU",
                    "MP",
                    "PR",
                    "VI",
                    "UM",
                    "ZW",
                    "NI",
                    "ST",
                    "TZ",
                    "MG",
                    "GP",
                    "NG",
                    "TC",
                    "AR",
                    "KE",
                    "MS",
                    "CG",
                    "ER",
                    "CI",
                    "MW",
                    "GM",
                    "SV",
                    "LC",
                    "BZ",
                    "CM",
                    "GH",
                    "KM",
                    "KY",
                    "DO",
                    "PY",
                    "VC",
                    "JM",
                    "GF",
                    "RW",
                    "CD",
                    "ZM",
                    "SN",
                    "GY",
                    "GB",
                    "UK",
                    "BF",
                    "CL",
                    "MH",
                    "PW",
                    "AU",
                    "CV",
                    "UG",
                    "BM",
                    "CO",
                    "AI",
                    "GN",
                    "BQ",
                    "GW",
                    "GA",
                    "ML",
                    "PA",
                    "BB",
                    "ZA",
                    "FM",
                    "MZ",
                    "SX",
                    "EC",
                    "BW",
                    "BI",
                    "NZ",
                    "AW",
                    "KN",
                    "ET",
                    "HT",
                    "NE",
                    "SC",
                    "AO",
                    "TG",
                    "CU",
                    "GD",
                    "SL",
                    "TT",
                    "NA",
                    "VE",
                    "CR",
                    "RE",
                    "BO",
                    "SR",
                    "AM",
                    "MF",
                    "MQ",
                    "MU",
                    "AG",
                    "SZ",
                    "SS"
                  ]
                },
                "gameId": 401810010,
                "plays": [
                  {
                    "id": 40181001015
                  }
                ],
                "thumbnail": "https://a.espncdn.com/media/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.jpg",
                "images": [
                  {
                    "name": "Poster Image",
                    "caption": "",
                    "alt": "",
                    "credit": "",
                    "height": 324,
                    "width": 576,
                    "url": "https://media.video-cdn.espn.com/images/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.jpg"
                  }
                ],
                "posterImages": {
                  "default": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_default.jpg",
                    "width": 576,
                    "height": 324
                  },
                  "full": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.jpg"
                  },
                  "wide": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_5x2.jpg"
                  },
                  "square": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_1x1.jpg"
                  },
                  "vertical": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_9x16.jpg"
                  },
                  "verticalFirstFrame": {
                    "href": "https://service-pkgespn.akamaized.net/opp/img/espn/9x16/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/thumb-1-w406-h720-f4.jpg"
                  }
                },
                "links": {
                  "web": {
                    "href": "https://www.espn.com/video/clip?id=46827452",
                    "self": {
                      "href": "https://www.espn.com/video/clip?id=46827452"
                    },
                    "seo": {
                      "href": "https://www.espn.com/video/clip/_/id/46827452"
                    }
                  },
                  "mobile": {
                    "source": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.mp4"
                    },
                    "alert": {
                      "href": "https://m.espn.com/general/video/videoAlert?vid=46827452"
                    },
                    "streaming": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/3476f2db-bbca-405b-a8b2-16ddd86ed416/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46827452"
                    },
                    "progressiveDownload": {
                      "href": "https://watch.auth.api.espn.com/video/auth/brightcove/3476f2db-bbca-405b-a8b2-16ddd86ed416/asset?UMADPARAMreferer=https://www.espn.com/video/clip?id=46827452"
                    }
                  },
                  "api": {
                    "self": {
                      "href": "https://content.core.api.espn.com/v1/video/clips/46827452"
                    },
                    "artwork": {
                      "href": "https://artwork.api.espn.com/artwork/collections/media/3476f2db-bbca-405b-a8b2-16ddd86ed416"
                    }
                  },
                  "source": {
                    "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_360p30_1464k.mp4",
                    "mezzanine": {
                      "href": "https://media.video-origin.espn.com/espnvideo/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.mp4"
                    },
                    "flash": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20.smil"
                    },
                    "hds": {
                      "href": "https://hds.video-cdn.espn.com/z/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_rel.smil/manifest.f4m"
                    },
                    "HLS": {
                      "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/playlist.m3u8",
                      "HD": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/playlist.m3u8"
                      },
                      "cmaf": {
                        "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/playlist.m3u8",
                        "9x16": {
                          "href": "https://service-pkgespn.akamaized.net/opp/cmaf/espn/9x16/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/playlist.m3u8"
                        }
                      },
                      "9x16": {
                        "href": "https://service-pkgespn.akamaized.net/opp/hls/espn/9x16/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20/playlist.m3u8"
                      },
                      "shield": {
                        "href": "https://watch.auth.api.espn.com/video/auth/media/3476f2db-bbca-405b-a8b2-16ddd86ed416/asset"
                      }
                    },
                    "HD": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_720p30_2896k.mp4"
                    },
                    "full": {
                      "href": "https://media.video-cdn.espn.com/motion/wsc/2025/1103/cd3e5a31-3518-48d7-8ac9-e33b1072db20/cd3e5a31-3518-48d7-8ac9-e33b1072db20_360p30_1464k.mp4"
                    }
                  },
                  "sportscenter": {
                    "href": "sportscenter://x-callback-url/showVideo?videoID=46827452&videoDSI=548399a7885ac"
                  }
                },
                "categories": [
                  {
                    "id": 191422,
                    "type": "topic",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae",
                    "description": "nba highlight",
                    "sportId": 0,
                    "topicId": 707
                  },
                  {
                    "id": 12025,
                    "type": "league",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34",
                    "description": "Fantasy NBA",
                    "sportId": 0,
                    "leagueId": 3090,
                    "league": {
                      "id": 3090,
                      "description": "Fantasy NBA",
                      "links": {
                        "web": {

                        },
                        "mobile": {

                        }
                      }
                    }
                  },
                  {
                    "id": 4630,
                    "type": "team",
                    "uid": "s:40~l:46~t:13",
                    "guid": "2876e98b-b9bc-2920-4319-46e6943f8be4",
                    "description": "Los Angeles Lakers",
                    "sportId": 46,
                    "teamId": 13,
                    "team": {
                      "id": 13,
                      "description": "Los Angeles Lakers",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/lal/los-angeles-lakers"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/lal/los-angeles-lakers"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "event",
                    "uid": "s:40~l:46~e:401810010",
                    "guid": "2e57a569-466b-3f16-9cdf-10048211efdf",
                    "description": "Miami Heat @ Los Angeles Lakers",
                    "eventId": 401810010,
                    "event": {
                      "id": 401810010,
                      "sport": "basketball",
                      "league": "nba",
                      "description": "Miami Heat @ Los Angeles Lakers",
                      "links": {
                        "web": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810010"
                          }
                        },
                        "mobile": {
                          "event": {
                            "href": "https://www.espn.com/nba/game/_/gameId/401810010"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 4259,
                    "type": "team",
                    "uid": "s:40~l:46~t:14",
                    "guid": "81e3212c-30ef-9b1b-5edb-453b13ff265a",
                    "description": "Miami Heat",
                    "sportId": 46,
                    "teamId": 14,
                    "team": {
                      "id": 14,
                      "description": "Miami Heat",
                      "links": {
                        "web": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/mia/miami-heat"
                          }
                        },
                        "mobile": {
                          "teams": {
                            "href": "https://www.espn.com/nba/team/_/name/mia/miami-heat"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 128809,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:2990992",
                    "guid": "f5096a5b-cbc5-1d7f-d406-56c623c434e5",
                    "description": "Marcus Smart",
                    "sportId": 46,
                    "athleteId": 2990992,
                    "athlete": {
                      "id": 2990992,
                      "description": "Marcus Smart",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/2990992/marcus-smart"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/2990992/marcus-smart"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711828,
                    "type": "editorialindicator",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7",
                    "description": "4 Star Rating"
                  },
                  {
                    "id": 159574,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:3945274",
                    "guid": "583794eb-0f38-9bbd-3e25-9dd33b7f83b8",
                    "description": "Luka Doncic",
                    "sportId": 46,
                    "athleteId": 3945274,
                    "athlete": {
                      "id": 3945274,
                      "description": "Luka Doncic",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3945274/luka-doncic"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/3945274/luka-doncic"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 9577,
                    "type": "league",
                    "uid": "s:40~l:46",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154",
                    "description": "NBA",
                    "sportId": 46,
                    "leagueId": 46,
                    "league": {
                      "id": 46,
                      "description": "NBA",
                      "abbreviation": "NBA",
                      "links": {
                        "web": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        },
                        "mobile": {
                          "leagues": {
                            "href": "https://www.espn.com/nba/"
                          }
                        }
                      }
                    }
                  },
                  {
                    "id": 711824,
                    "type": "editorialindicator",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26",
                    "description": "SC4U  - Eligible"
                  },
                  {
                    "id": 711821,
                    "type": "editorialindicator",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2",
                    "description": "SC4U - Full Highlight"
                  },
                  {
                    "id": 409391,
                    "type": "athlete",
                    "uid": "s:40~l:46~a:4432848",
                    "guid": "f5252401-4e07-3fef-88b1-7d4f652ead74",
                    "description": "Jaime Jaquez Jr",
                    "sportId": 46,
                    "athleteId": 4432848,
                    "athlete": {
                      "id": 4432848,
                      "description": "Jaime Jaquez Jr",
                      "links": {
                        "web": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4432848/jaime-jaquez-jr"
                          }
                        },
                        "mobile": {
                          "athletes": {
                            "href": "https://www.espn.com/nba/player/_/id/4432848/jaime-jaquez-jr"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": "guid",
                    "guid": "9660cd01-90a5-2726-f826-03bcf57d32ae"
                  },
                  {
                    "type": "guid",
                    "guid": "12c6e39f-b760-49b1-8e4c-b3eb90814c34"
                  },
                  {
                    "type": "guid",
                    "guid": "2876e98b-b9bc-2920-4319-46e6943f8be4"
                  },
                  {
                    "type": "guid",
                    "guid": "2e57a569-466b-3f16-9cdf-10048211efdf"
                  },
                  {
                    "type": "guid",
                    "guid": "81e3212c-30ef-9b1b-5edb-453b13ff265a"
                  },
                  {
                    "type": "guid",
                    "guid": "f5096a5b-cbc5-1d7f-d406-56c623c434e5"
                  },
                  {
                    "type": "guid",
                    "guid": "b14f9e1f-2d2c-3b10-b39d-d781f4c4aba7"
                  },
                  {
                    "type": "guid",
                    "guid": "583794eb-0f38-9bbd-3e25-9dd33b7f83b8"
                  },
                  {
                    "type": "guid",
                    "guid": "7b3729c9-7f69-308a-bf8a-ee15a6aba154"
                  },
                  {
                    "type": "guid",
                    "guid": "d348c764-47d9-3e31-bd75-d39dfde52c26"
                  },
                  {
                    "type": "guid",
                    "guid": "f3e05446-8d07-3064-a239-c10c32884ea2"
                  },
                  {
                    "type": "guid",
                    "guid": "f5252401-4e07-3fef-88b1-7d4f652ead74"
                  }
                ],
                "ad": {
                  "sport": "nba",
                  "bundle": "sportscenter"
                },
                "tracking": {
                  "sportName": "basketball",
                  "leagueName": "NBA",
                  "coverageType": "Final Game Highlight",
                  "trackingName": "NBA_One-Play (Miami Heat vs. Los Angeles Lakers: Game Highlights) 2025/11/03 ESHEET",
                  "trackingId": "dm_20251103_NBA_miami_heat_vs_los_angeles_lakers_game_highlights"
                },
                "contributingPartner": "wsc",
                "contributingSystem": "wsc"
              }
            }
          ]
        }
      ]
    }
  ]
}
```