# Market vs Model Doctrine (Critical Foundation)

This is the foundational framing for the entire matchup network. Every agent must internalize these concepts.

## The Market is the Voice of Authority on Favorites/Underdogs

**"Favorite" and "underdog" are market-defined terms.**

- Vegas, Kalshi, and public betting markets establish who is the favorite (lower payout, expected to win) and who is the underdog (higher payout, expected to lose).
- When a user says "underdog" without qualification, they mean **market underdog** — the team priced below 50% by Vegas/Kalshi.
- When a user says "favorite" without qualification, they mean **market favorite** — the team priced above 50% by Vegas/Kalshi.
- The market represents **public consensus** — it's what "everyone" thinks.

## The Model is a Private, Proprietary Signal

**Our model is separate from the market. It's our edge.**

- The model's prediction (`p_home`) is our **private, novel, proprietary** win probability.
- No one else has access to this model. It's not public information.
- The model may **agree or disagree** with the market — and that disagreement is where value lives.
- Never conflate "model favorite" with "market favorite" — they can point opposite directions.

## The Value Proposition: Disagreement

**The most important insight is when model and market disagree.**

Example scenario:
- Market (Vegas/Kalshi): Team A at 45% (underdog)
- Model: Team A at 53% (model's pick)

In this case:
- Team A is the **market underdog** (priced at 45%)
- Team A is the **model favorite** (our model gives them 53%)
- The user saying "Team A makes sense to me as underdog" likely means: "I like that the market is underpricing Team A, and the model agrees with me."

This disagreement is the entire point. Users come to us to find where the model sees something the market doesn't.

## p_home Interpretation (CRITICAL)

`p_home` is the model's probability that the **home team** wins.

- If `p_home > 0.50`: Model favors the **home team**
- If `p_home < 0.50`: Model favors the **away team**
- If `p_home = 0.53` for a game where Team A is home: Model gives Team A a 53% chance to win

**Before writing any narrative about "what the model predicts", verify your interpretation of p_home.**

Example:
- Game: DET @ GS (Detroit away, Golden State home)
- `p_home = 0.47` (47%)
- This means: Model gives GS (home) 47%, so model gives DET (away) 53%
- **Model favors Detroit.**

## Attribution Rules (Hard Rules)

1. **Never say a team is "favored" or "underdog" without attribution.**
   - WRONG: "The Pistons are underdogs here"
   - RIGHT: "The Pistons are **market underdogs** (Vegas: 45%)"
   - RIGHT: "The **model** favors the Pistons at 53%"

2. **Always distinguish model vs market when discussing probabilities/odds.**
   - Model probability comes from `ensemble_model.p_home`
   - Market probability comes from `market_snapshot` (Kalshi, Vegas)

3. **When user says "underdog" or "favorite", assume they mean market-defined unless they explicitly say "model."**

## Common User Patterns to Recognize

| User says | They likely mean |
|-----------|------------------|
| "X makes sense as underdog" | "I like X, who is a market underdog — does the model agree?" |
| "Why is X underdog?" | "Why does the market have X below 50%?" |
| "Model likes X as underdog" | "Model favors X even though market has them as underdog" |
| "Who wins?" | "What does our model say, and how does it compare to market?" |

## Checklist Before Writing Output

Before finalizing any narrative about the prediction:

1. What is `p_home`? ___
2. Who is the home team? ___
3. Therefore, model favors: ___ (home if p_home > 0.50, away if < 0.50)
4. What does the market say? (Check `market_snapshot`)
5. Is there disagreement between model and market?
6. If user mentioned "underdog/favorite", did I correctly interpret this as market-defined?
