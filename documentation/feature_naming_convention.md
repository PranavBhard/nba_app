## 1) `stat_name` options

These are your core “what does this measure” identifiers. (You can expand over time, but keep them stable.)

### Team outcome / scoring

* `points`
* `wins`
* `ppg`
* `margin`

### Shooting / efficiency

* `efg`
* `ts`
* `three_made`
* `three_pct`
* `fg_pct` *(optional if you add later)*

### Team performance

* `off_rtg`
* `def_rtg`
* `assists_ratio`
* `pace`

### Box-score / possession-ish

* `reb_total`
* `off_total`
* `def_total`
* `blocks`
* `turnovers`

### Rating / strength

* `elo`

### Player-aggregate PER family

* `player_per`
* `player_per_1`
* `player_per_2`
* `player_per_3`
* `player_team_per`
* `player_starters_per`
* `player_per_available`

### Injury family

* `inj_per`
* `inj_min_lost`
* `inj_severity`
* `inj_rotation_per`

*(Note: “inj_per_value” usually collapses into `inj_per` + a reducer like `weighted_MIN`.)*

---

## 2) `time_period` options

Exactly one of:

* `season`
* `months_<N>` where `<N>` is any positive int (e.g. `months_1`, `months_3`)
* `games_<N>` where `<N>` is any positive int (e.g. `games_10`, `games_25`)
* `days_<N>` where `<N>` is any positive int (e.g. `days_3`, `days_14`)
* `none` (instantaneous / current / already-windowed)

---

## 3) `calc_weight` options

Choose one reducer / computation method:

### Non-parameterized

* `raw`
* `avg`
* `sum`
* `std`
* `min`
* `max`
* `top<N>_sum` *(e.g. `top3_sum`, `top5_sum`)*
* `top<N>_avg` *(optional, e.g. `top3_avg`)*
* `rel` *(league-relative / normalized)*

### Parameterized weighted form

* `weighted_<BY>`

Where `<BY>` is one of your controlled vocabulary values, e.g.

* `MIN` (minutes)
* `MPG` (minutes per game)
* `REC` (recency)
* `GAMES` (games-played weighting)
* `POSS` (possessions, if you ever use it)

You can also allow compound weight keys if you want:

* `weighted_MIN_REC`
* `weighted_MPG_REC`

---

## 4) `home/away/diff` options

Exactly one of:

* `home`
* `away`
* `diff`

---

## 5) Optional side flag

If and only if it is side-split, append:

* `|side`

Otherwise the name ends at `<home/away/diff>`.

---

## Full feature format (final)

* Non-side:

  * `stat_name|time_period|calc_weight|home/away/diff`
* Side-split:

  * `stat_name|time_period|calc_weight|home/away/diff|side`

