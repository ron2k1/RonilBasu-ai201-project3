# Milestone 4: how `labels.csv` was labelled

> Every pass below was run by Claude Code, the coding agent I ran this unit
> with, or by subagents it launched. None of the 416 rows was labelled by me.
> The `note` column in `labels.csv` says which pass each row came from.

## The passes, in order

1. **Cold, 20 rows (`p0001`–`p0021`).** Claude Code labelled the first 21
   pool rows in a single pass from the README definitions alone, before any
   pre-label existed. `p0019` was skipped as a redact.dev placeholder, which
   leaves 20. Reading these rows is also what produced the basketball-scope line
   in the taxonomy (commit `6799c04`). No row had been labelled under the
   unscoped wording, so nothing needed relabelling. Result: 11 `banter`,
   6 `take`, 3 `analysis`.
2. **Blind pre-label, two batches.** Two Claude subagents worked from the
   README's Label Taxonomy section, `label_definitions.txt`, and their own
   batch file. Neither saw the cold labels or the other batch.
   - **Batch A, in pool order:** `p0022`–`p0300`, 279 rows. This is the
     community's natural mix.
   - **Batch B, the analysis top-up:** every comment from `p0301` onward that
     contains a digit, 120 rows. `p0401`–`p0460` were left out because that's
     the Milestone 1 reading range and where the README's examples come from.
     The batch was picked to add `analysis`, but every row in it was labelled as
     whatever it is. Most of the 120 came out `take` or `banter`.
3. **Review of every pre-labelled row.** Claude Code read each of the 399
   pre-labelled rows next to its text and the subagent's one-line reason, and
   either kept the label or corrected it. 10 of 399 were corrected (2.5%).

## The split that changed a rule

The two batches disagreed about one kind of post: a basketball fact with no
opinion attached. Batch A called `p0150` ("John Hollinger has us 40-42, 9th in
the East") `banter`. Batch B called bare stat lines such as `p0681` ("9 ppg in
27 mins at 43% shooting") `analysis`. Both readings fit the rules as written,
so the gap was in the rules. The README now has a bare-fact rule
(commit `a7473af`): a stat line, record, result, contract figure or projection
is evidence for a side and counts as `analysis`. Trivia or a quote passed along
for fun is `banter`. The rows on both sides were re-checked against the rule.

## Every correction

| Row | Pre-label | Final | Why |
|---|---|---|---|
| `p0029` | skip (question) | `take` | A rhetorical question pushing a position: there are too many posts because he's a Laker |
| `p0085` | `banter` | `take` | A sarcastic headline ("2027: Rudy Gobert helps Wolves become greatest offensive team in NBA history") still predicts the opposite. This is the sarcasm rule |
| `p0131` | skip (question) | `take` | A rhetorical challenge ("How have the Bulls and Pelicans been bent over by the 2nd apron?"), not a request for information |
| `p0150` | `banter` | `analysis` | A bare projection is evidence for a side, under the bare-fact rule |
| `p0172` | `banter` | `take` | "As a Sonics fan, I've seen this movie before" predicts a relocation a reply could dispute |
| `p0242` | `take` | `banter` | "OKC trade gave him trust issues" is a quip. The only thing left to answer is the joke |
| `p0517` | `take` | `analysis` | Delete the 7-game series format and the low-variance claim has nothing behind it |
| `p0653` | `take` | `analysis` | The "not 1, not 2..." quote is the reason 2011 was worse. Delete it and nothing is left |
| `p0718` | `analysis` | `banter` | Top 50 / Top 75 trivia passed along, with nothing it is evidence for |
| `p0727` | `banter` | `take` | Opinions about a fan's sentiment-analysis project. Fans and the media that cover the league are in scope |

## Skipped rows (not in `labels.csv`)

| Reason | Rows |
|---|---|
| Only asks for information | `p0201`, `p0498` |
| Wonders aloud and asks the poster for more ("We need more insight, OP!"). Skipped as a question. Under the decision rule it could have been `banter` | `p0080` |
| Text wiped by redact.dev | `p0019` |

## What the low correction rate does and doesn't mean

2.5% sounds like strong agreement, but every pass here was the same model
family reading the same rules. Two Claude passes share their priors, so they
agree with each other more easily than two people would. The batch-to-batch
split above is the one place the agreement was tested from outside a single
pass. The real outside check is unit 6's agreement report against the staff
set.
