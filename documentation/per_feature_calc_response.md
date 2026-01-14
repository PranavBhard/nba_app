Yeah, there are definitely some landmines here, and your doc already catches the two biggest ones. Let me walk through what *I* see from a modeling / code-flow perspective.

### 0. Big picture: math is the same, **player set is not**

From your description, **once you have a set of players**, both training and prediction call the *same* function:

> `per_calculator.compute_team_per_features(...)`
> → `_get_team_players_before_date_cached()`
> → season-long aggregates → PER → team PER features

So the PER math itself is consistent.

The discrepancies are almost entirely about **which players go into that function** and **how the filters behave when missing / empty / using different IDs**. That’s exactly the kind of thing that will make player features feel like “they do nothing.”

---

## 1. The two big discrepancies you already found (and yes, they’re serious)

### 1.1 Training: “only who played” vs Prediction: “everyone who ever played”

**Training:**

* For each game, you build `player_filters` from `stats_nba_players` with:

  * `playing`: players with `stats.min > 0` for that `game_id`
  * `starters`: players with `starter=True` for that `game_id`
* So training PER for that game = **season-long stats of only the guys who actually played in that game**.

**Prediction (when no player_filters from UI):**

* You call `get_team_players_before_date(...)`, then:

  * `home_playing = [p['_id'] for p in home_players ...]`
* That is **all players who have played for the team before the date** (minus excluded), not the specific 8–10 that will play tonight.

**Impact:**

* Training learns:
  “PER features reflect the active lineup’s talent”
* Prediction computes:
  “PER features reflect the entire season’s roster, including guys not playing tonight”

So even if you mark players injured in the UI but don’t pass filters correctly, the prediction path can still behave like “everyone is available,” and the model never sees the kind of variation it was trained on.

This is absolutely a **HIGH-severity mismatch**.

---

### 1.2 Default prediction behavior ≠ training default

You nailed this too:

* Training **always** constructs `player_filters` from the actual game box score → never falls back to “all players.”
* Prediction:

  * If `player_filters` is missing or `{}`, it invents one from all historical team players.

So:

* Training’s “default” = “only who played”
* Prediction’s “default” = “everyone who ever played”

This can 100% explain “PER features do nothing”:

* In training, the model sees PER shift when lineups differ.
* In prediction, if most calls skip explicit `player_filters`, the PER features are nearly **constant** for a team on a given date (same pool of players), so:

  * LR / tree sees very little variation ⇒ tiny/zero weights.

---

## 2. Extra discrepancies I see that you didn’t explicitly call out

### 2.1 Possible ID mismatch: `player_id` vs `_id`

From your doc:

* Training `player_filters['playing']` is built from `stats_nba_players`:

  ```python
  {'player_id': 1, 'starter': 1}
  # → playing list = [doc['player_id'], ...]
  ```

* Prediction (no filters) uses:

  ```python
  home_playing = [p['_id'] for p in home_players ...]
  ```

* `_get_team_players_before_date_cached()` likely returns docs from `players_nba` where `_id` is the Mongo ObjectId.

* `stats_nba_players` has `player_id` (probably ESPN / external ID).

**If** `compute_team_per_features` expects one ID type (say `player_id`) but prediction is passing the other (`_id`), then:

* Training filters **match** (correct players used)
* Prediction filters might **never match**, so it falls back to:

  * “no filter” → use all players
  * or “empty result” → weird defaults

This would perfectly explain:

* Why your UI “injury toggles” and player configs don’t move the PER features.
* Why prediction seems insensitive to changes in `player_filters`.

👉 I would explicitly confirm in code:

* What ID field `compute_team_per_features` uses to intersect with `player_filters['playing']`.
* That both training and prediction are passing the same ID namespace (either always `player_id` or always `_id`, not mixed).

This is a **sneaky but very plausible bug**.

---

### 2.2 Starter logic drift = noisy starter features

You already called out:

* Training: starters = `starter` flag in that game’s `stats_nba_players`.
* Prediction:

  * If `player_filters['starters']` provided: use that.
  * Else: derive starters from historical pattern (`starter_games > games/2`).

Implications:

* For any game where tonight’s lineup ≠ “usual” lineup:

  * Training sees “true starters for this game”.
  * Prediction sees “most frequent starters historically”.

That gives you:

* Noisy `startersPerAvg` and `startersPerDiff` at inference.
* Those features get downweighted or ignored by the model (they look unreliable out-of-distribution).

This alone won’t make PER block useless, but it makes the **starter-specific** PER features particularly fragile.

---

### 2.3 Injury metadata vs UI flags

Right now:

* Training: implicitly excludes injured guys by virtue of querying only those who logged minutes in that game.
* Prediction:

  * Uses UI’s `is_injured` to build `player_filters`, **and**
  * Also filters by `players_nba.injured == True`.

Two potential problems:

1. If UI flags and DB metadata disagree → you get inconsistent filters.
2. If metadata is stale (often the case), your prediction-time player set might be wrong even when UI is correct.

This again could lead to situations where:

* The player set used for PER is not what you think it is,
* So flipping “injured” in the UI appears to do nothing.

---

## 3. How this explains “player-level features don’t matter”

Putting it together:

1. **Training**:

   * PER features change meaningfully from game to game:

     * different lineups,
     * different combinations of star/non-star,
     * injured guys auto-excluded.
   * Model *can* learn: “Rosters with higher PER_avg/weighted win more often.”

2. **Prediction (current behavior)**:

   * If `player_filters` is missing or mis-shaped, you end up with:

     * same or very similar set of players for every prediction,
     * broken ID matching → filter silently ignored,
     * constant-ish team PER values.
   * Model sees **almost no variation** in PER at inference time.
   * So:

     * Changing “who’s playing” in the UI doesn’t change features, so doesn’t change predictions.
     * Feature importance appears tiny for player_talent block.
     * In CV experiments, any noise/mismatch from PER is just extra variance → “player_talent hurts performance”.

On top of that, you also have the **structural overshadowing** problem:

* Team-level stats (outcome_strength, shooting, ratings) already encode a **lot** of player talent signal.
* If PER is noisy or mismatched at inference, the model logically concludes “I can ignore this; team stats are cleaner.”

---

## 4. Concrete things I’d do next

### 4.1 Add hard logging / asserts around the PER player set

For both training and prediction, log for a few games:

* Which player IDs are used in PER calculation.
* How many players per team are used.
* The resulting PER features.

Specifically:

1. Pick a historical game.
2. Run the **training path** PER computation for that game.
3. Run the **prediction path** for the same date/teams, with:

   * no `player_filters`
   * correctly constructed `player_filters` based on that game’s box score.
4. Compare PER feature vectors.

Those should match (within floating-point error) when you feed the same `playing` list. If they don’t, you’ve found the discrepancy.

### 4.2 Make `player_filters` mandatory in prediction

Instead of:

* “If no filters, use all players,”

do:

* “If no filters, either:

  * use last-actual-game lineup, or
  * raise an error / warning and don’t compute PER.”

You want the default prediction behavior to mirror training’s assumption:

> PER = talent of the *actual* lineup in this game.

### 4.3 Normalize ID usage

Pick one canonical ID:

* Either always `player_id` (ESPN/integration ID), or
* Always `players_nba._id`

Then enforce:

* `player_filters['playing']` is always that ID type.
* `_get_team_players_before_date_cached()` returns docs keyed by that same ID.
* `compute_team_per_features` only matches on that ID.

And log a warning if:

* `len(player_filters['playing'])` > 0 but **no players** are matched.

---

## 5. Answering your core question directly

> **Do you see any discrepancies in calculations for training and predicting that may be the cause of this?**

Yes:

1. **Training only uses actual game participants; prediction often uses “everyone who’s ever played.”** That’s a big mismatch.

2. **Prediction’s construction of `player_filters` can easily be using a different ID field (`_id` vs `player_id`) than training**, which would effectively nullify your filters and make PER features insensitive to UI changes.

3. **Starter logic and injury logic are not symmetric** between training and prediction, which makes the starter-based and availability-based PER features noisy out-of-distribution.

Those three together are more than enough to explain why:

* Player features don’t move the model,
* And even seem to “hurt performance” in your ablation tests.
