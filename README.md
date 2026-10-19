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

**The decision rule I used every time:** strip the tone and ask what a reply
could disagree with. If the post commits to a position about players, teams or
the league that someone could answer with "no, you're wrong", it's `take`,
even when it's sarcastic, joking or furious. If the only things left to answer
are the joke or the feeling itself, it's `banter`. Under this rule `p0454` is
a `take`.

**Two more rules, for the other boundaries:**

- **`analysis` vs `take`: delete the fact.** If the claim is left with no
  reason, the fact was carrying it, so it's `analysis`. If the post still makes
  the same point just as hard (the fact only set the scene, or set up a joke),
  it's `take`. Whether the fact is a *good* reason doesn't matter. The label
  records what the post does, not whether it's right.
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

**Where the posts came from:**

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
| **Total** |  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**2.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**3.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

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
