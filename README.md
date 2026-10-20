# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads an r/nba comment and says whether it is arguing with
evidence, arguing without it, or not arguing at all. Each comment gets one of
three labels:

- `analysis`: a basketball argument resting on a checkable fact, such as a
  stat, a record or a contract figure.
- `take`: a basketball opinion, judgment or prediction with nothing checkable
  behind it.
- `banter`: jokes, jabs, quick feelings and off-topic talk.

The classifier is `distilbert-base-uncased`, fine-tuned on 416 real comments
from 72 r/nba threads and labelled under the rules in the Label Taxonomy
below.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Three labels, and two questions that sort every post into one of them:

1. **Does the post commit to a basketball position someone could argue with?** No: `banter`.
2. **If it does, does it offer a checkable fact as the reason?** Yes: `analysis`. No: `take`.

The examples below are real r/nba comments from the reading in Milestone 1
(pool ids in brackets, text exactly as collected).

### `analysis`

**Definition:** a basketball argument that offers a specific, checkable fact
as its reason: a stat, a record, a date, a named game or play, a contract
figure, or a quote.

**Example 1** `[p0439]`:
> Closest I can find is 2022 1st round vs ATL where he was 1st in PTS (122), 2nd in REB (31), 2nd in AST (21), 1st in STL (11), 3rd in BLK (2). His other closest series was ironically against LeBron, in the 2020 Finals: 2nd in PTS (157), 3rd in REB (50), 1st in AST (59), 1st in STL (13), 2nd in BLK (5).

**Example 2** `[p0451]`:
> No it hasn't. When he's out there he's still very good defensively, not the elite defender he was in his prime but extremely effective both on and off ball. 1.7 steals a game, 98th percentile in both steals and deflections per 100 possessions. Good article where I pulled those stats from goes more in depth. He's still a good/great defender. [link: sports.yahoo.com]

### `take`

**Definition:** an opinion, judgment or prediction about basketball that
someone could argue with, offered without a checkable fact as its reason.

**Example 1** `[p0402]`:
> It never made sense to me to keep him over Cisse

**Example 2** `[p0460]`:
> Braun is really the guy they overpaid. They should keeo Watson and find away to dump Braun

### `banter`

**Definition:** a joke, a bit, a jab, a quick feeling, or talk about
something other than basketball: anything that doesn't commit to a basketball
position someone could argue with.

**Example 1** `[p0425]`, on the Ben Simmons injury thread:
> Grand opening , grand closing

**Example 2** `[p0440]`:
> In this house, Nick Young is a saint! A saint!

### The hardest boundary

**Which two labels:** `take` and `banter`. r/nba says most of its opinions as
jokes, sarcasm or swearing, so the tone of a post and its content point at
different labels all the time. This is the post that showed it `[p0454]`, from
the Ben Simmons Achilles thread:

> Which is fucking insane man. Something isn't right. Idk if it's the shoes or that basketball has become way too demanding from a very young age, but these guys simply can't keep up anymore. Their bodies are literally ripping

It reads as a reaction. It also blames the injury wave on how hard players are
worked from a young age, which is something you could argue against.

**The decision rule, applied to every row:** strip the tone and ask what a reply
could disagree with. If the post commits to a position about players, teams or
the league that someone could answer with "no, you're wrong", it's `take`,
even when it's sarcastic, joking or furious. If the only things left to answer
are the joke or the feeling itself, it's `banter`. Under this rule `p0454` is
a `take`.

**Three more rules, for the other boundaries:**

- **`analysis` vs `take`: delete the fact.** If the claim is left with no
  reason, the fact was carrying it, so it's `analysis`. If the post still makes
  the same point just as hard (the fact only set the scene, or set up a joke),
  it's `take`. Whether the fact is a *good* reason doesn't matter. The label
  records what the post does, not whether it's right.
- **A post that is only a basketball fact** (a stat line, a record, a result,
  a contract figure, a projection) and argues nothing out loud is `analysis`.
  Posted into a thread, a bare number is evidence for one side even when the
  side isn't named. The `analysis` example `p0439` is exactly that: a list of
  stats answering a question. Trivia or a quote passed along for fun, with
  nothing it could be evidence for, is `banter`. This rule was added while the
  pre-labels were being reviewed, because the two blind pre-label passes split
  on it (see The Dataset).
- **A post doing two things** gets the label for the one it spends most of its
  words on. This is a tie-break, used only after the rules above.

**What counts as basketball:** players, teams, coaches, refs, front offices,
contracts, the league and its business, and the media and fans that cover it.
An opinion about shawarma in a Raptors thread is `banter`. This scope line was
added after the first cold rows were read and before any were labelled: rows
`p0006` and `p0007` argue about which city has better shawarma, and `p0018`
corrects someone about hammerhead sharks with a fact. Under the unscoped
definitions those were a `take` and an `analysis`, which would have taught the
model that trivia corrections are basketball analysis.

**What sits outside the taxonomy:** a post that only asks for information
("what's the meatball sub story") is none of the three, and neither is a
comment whose text was wiped by a privacy tool (`p0019` is a redact.dev
placeholder followed by random words). Both are skipped at labelling time and
counted under The Dataset.

**The stress test.** Before labelling, a separate Claude agent was given these
definitions and asked for eight r/nba-style comments built to sit on the
boundaries. Three of the eight (a player "disappeared" in two named playoff
exits, a contract figure in front of a jab about his dribbling, and a coach
fired "right after their first ECF trip in 25 years") couldn't be called
cleanly under the first draft of the `analysis` rule, which only said the fact
had to "do the work". The delete-the-fact test and the "good reason doesn't
matter" clause were added because of them. The eight posts and the call on
each are in [`docs/stress_test.md`](docs/stress_test.md).


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/nba, through the safereddit.com Redlib
mirror, because reddit.com refused direct requests from this machine with a
403. `tools/harvest_nba.py` collected 72 threads on 2026-10-19:
- ten each from the week's top, the month's top and hot
- ten each from title searches for "predictions", "MVP" and "overrated"
- nine from a search for "OC" and three from "unpopular opinion"

The searches pull threads where people argue instead of react. The thread
list is in `data/nba_sources.json`.

The harvester first dropped bots, deleted comments, anything under 25 or over
1,200 characters, anything scored below 2, and anything containing a slur.
From what was left it kept up to 12 random comments per thread. Usernames
became `u/[user]`, links `[link: domain]` and gifs `[gif]`. That left a
shuffled pool of 827 candidates. `labels.csv` holds 416 of them:
- 297 from the first 300 in pool order (three skipped)
- 119 from 120 later comments that contain a digit (one skipped), added to
  thicken `analysis`

**How I labelled them:** Claude Code, the coding agent I ran this unit with,
did all of the labelling. I didn't label any rows myself.

- **Cold, 20 rows.** `p0001`–`p0021`, one skipped. Claude Code labelled them
  from the definitions alone, before anything was pre-labelled. Their `note`
  says `cold`.
- **Pre-labelled with AI, then reviewed, 396 rows.**
  - Two Claude subagents pre-labelled 399 rows blind: 279 in pool order, plus
    the 120-row digit top-up. Neither saw the cold labels or the other batch.
  - Claude Code then read every pre-labelled row next to the subagent's
    one-line reason, and kept or corrected it. 10 were corrected.
  - Four rows were skipped, which leaves 396. The note says `pre-labelled,
    reviewed, kept` or `pre-labelled X, corrected to Y` with the reason.
- **Skipped, 4 rows.** Three only asked for information. One was a
  redact.dev placeholder.
- The two subagents split on bare facts with no opinion attached. That split
  is why the Label Taxonomy has a bare-fact rule.
- Every correction and the split are recorded in
  [`docs/labelling_log.md`](docs/labelling_log.md).

**The top-up and the shortcut it could teach.** The top-up rows were picked
because they contain a digit, but each was labelled as whatever it is. Only 39
of its 119 rows are `analysis`. Across the whole file, 81% of `analysis` rows
contain a digit, but so do 48% of `take` rows and 35% of `banter` rows. A
number alone doesn't give the label away. It's still the likeliest shortcut
for the model to learn, and the first thing to look for in unit 6's errors.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 74 | 17.8% |
| `take` | 155 | 37.3% |
| `banter` | 187 | 45.0% |
| **Total** | 416 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

The three calls below were made by Claude Code during the review, so the
template's "I chose" reads "Chosen" here. There's one case for each boundary.

**1. `take` vs `banter` (the hardest boundary)**
> *The post* `[p0085]`: 2027: Rudy Gobert helps Wolves become greatest offensive team in NBA history
>
> *Could have been:* `banter` or `take`. It's a fake headline, and the
> subagent pre-labelled it `banter` as a sarcastic bit.
>
> *Chosen:* `take`, because of the strip-the-tone rule. Under the joke is a
> claim about how Minnesota's offense goes with Gobert in it, and a reply could
> answer "no, you're wrong". The words are a joke and the meaning is a
> prediction, which is the reason the rule exists.

**2. `analysis` vs `take`**
> *The post* `[p0696]`: a reply to a post that compared this season's
> win-total lines with last season's results and concluded the league will
> have more parity. It argues that's a bad inference: "Let's say I have 30
> coins, and I flip each of them 10 times per day. Every day, at least one of
> them ends up with more than 6 heads [...] But, when I set the odds for
> tomorrow, none of the individual coins are expected to end up with more than
> 5 or less than 5 heads. Does that mean that we're expected to get flatter
> results tomorrow? No, of course not."
>
> *Could have been:* `analysis`. It's the most careful argument in the file,
> and it's full of numbers.
>
> *Chosen:* `take`. The numbers are invented to illustrate the logic, and the
> logic is the reason. Delete-the-fact finds no checkable fact carrying the
> claim. The rule labels what a post rests on, not how rigorous it is. A model
> that learned "long, careful and numeric means `analysis`" would be learning
> the wrong thing.

**3. `banter` vs `analysis` (the one that changed a rule)**
> *The post* `[p0150]`: John Hollinger has us 40-42, 9th in the East
>
> *Could have been:* `banter`, because it states no opinion of its own, and
> that's how the in-order subagent labelled it. Or `analysis`, because it's a
> checkable projection; the top-up subagent labelled posts like it (bare stat
> lines such as `p0681`, "9 ppg in 27 mins at 43% shooting") that way.
>
> *Chosen:* `analysis`, under the bare-fact rule this split led to. Posted
> into a thread about a team's season, a projection is evidence for a side,
> even when the side isn't named. The README's own `analysis` example `p0439`
> is the same shape: stats answering a question, no opinion attached. Trivia
> passed along for fun (`p0718`, on how many Top 50 players had died) went to
> `banter` under the same rule.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, the notebook's default, with a
three-label classification head (`analysis`, `take`, `banter`).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42,
`MAX_LENGTH` 128.

**Device:** `cpu` (torch 2.14.1+cpu). The laptop has an RTX 4060, but
`requirements.txt` asks for plain `torch`, and the default PyPI build on
Windows is CPU-only. The notebook's device check found no GPU it could use.
Sections 1 to 5 ran in about three minutes.

**Anything I changed from the defaults, and why:** Nothing. Every setting
above is the notebook default.
- `MAX_LENGTH` was the one worth checking. 20 of the 416 posts run past 128
  DistilBERT tokens and get cut: 11 `take`, 5 `banter`, 4 `analysis`. The
  median post is 28 tokens and the longest is 237. Doubling the limit to save
  5% of posts would roughly double the cost, because every post is padded up
  to the limit, not only the long ones.
- The rest stay at their defaults so that unit 6's three seeds measure this
  setup. Any change belongs in The Improvement, after the baseline comparison.

**Split sizes:** stratified 70/15/15 on seed 42.

| Label | Train | Val | Test |
|---|---|---|---|
| `analysis` | 52 | 11 | 11 |
| `take` | 107 | 24 | 24 |
| `banter` | 131 | 28 | 28 |
| **Total** | 290 | 63 | 63 |

No label fell under 8 in the test split, so the notebook printed no `[note]`.
`analysis` comes closest with 11: one post changing sides moves its recall by
9 points, so expect its F1 to swing between seeds.

The run's metrics are in `results.json`. They're read in unit 6, against
the criteria filed before the run.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**The biggest use first.** I gave this unit's brief to Claude Code, the
coding agent, and it did the work:
- scraping the threads and reading the comments
- drafting the taxonomy and the five criteria
- labelling (cold, then reviewing every pre-label)
- the training run
- drafting this README

The two moments below happened inside that. The bullet labels say "was asked"
rather than "I asked", because the agent ran them.

**Moment 1: the stress test**

- *What was asked for:* a fresh Claude agent got the three draft definitions
  and was asked for eight r/nba-style comments built to sit on the label
  boundaries, with no labels attached.
- *What came back:* three of the eight couldn't be called cleanly under the
  draft `analysis` rule, which only said the fact had to "do the work". They
  were a player who "disappeared" in two named playoff exits, a contract
  figure in front of a jab about his dribbling, and a coach fired "right after
  their first ECF trip in 25 years". None of the eight was plain `banter`. The
  agent wrote opinions dressed as jokes, never jokes with no opinion.
- *What changed:*
  - `analysis` got the delete-the-fact test and the "a weak reason is still
    the reason" clause.
  - `take` lost the word "sincere", because a joking post can still commit to
    a position.
  - The `banter` side of the hardest boundary was tested on real posts
    instead (`p0425`, `p0440`, `p0454`).
  - All eight posts and the calls are in
    [`docs/stress_test.md`](docs/stress_test.md).

**Moment 2: the pre-label passes disagreeing**

- *What was asked for:* two Claude subagents pre-labelled 399 rows blind from
  the README rules. Each gave a label, a one-line reason and a "hard" flag per
  row. One took 279 rows in pool order, the other the 120-row digit top-up.
- *What came back:*
  - 399 labels, 192 of them flagged hard.
  - The two batches split on bare facts. The in-order pass called a bare
    projection (`p0150`) `banter`. The top-up pass called bare stat lines
    `analysis`, citing the README's own note that the shark-fact correction
    would have been `analysis` if it were about basketball.
  - Separately, the subagents tended to call sarcasm and rhetorical
    questions `banter` or skips when they carried a position.
- *What changed:*
  - The bare-fact rule went into the taxonomy.
  - The review corrected 10 of 399 rows. Four of them (`p0085`, `p0172`,
    `p0029`, `p0131`) were that sarcasm and rhetorical-question pattern.
  - The labelling log records that two passes by the same model family agree
    more easily than two people would, so the 2.5% correction rate isn't
    evidence that the labels are right.

**Pre-labelling disclosure:** yes.
- 396 of the 416 rows in `labels.csv` were pre-labelled by Claude subagents.
  Claude Code read every one of them and kept or corrected it.
- The other 20 are the cold rows, which Claude Code also labelled. I didn't
  label any rows myself.
- Every row's `note` says which pass it came from, and corrected rows say what
  changed and why.
- `criteria.md` was also drafted by Claude Code, and committed before any
  label or run existed.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
