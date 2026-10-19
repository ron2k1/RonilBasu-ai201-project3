# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

> **Who wrote these.** Claude Code drafted all five at my direction, from the
> taxonomy and the planned label mix, and they were committed before
> `labels.csv` existed and before any training run. Nobody had seen a model
> number when the targets were set. The disclosure is repeated in the README's
> How I Used AI.

**What the targets are measured on.** The held-out test split the notebook
makes (15% of `labels.csv`), scored by the `results.json` fields named in each
criterion. Unit 6 retrains on seeds 42, 7 and 2024, and a criterion is met only
if it holds on all three. The plan going in is about 240 labelled posts, so the
test split is about 36 posts, and one post is worth roughly 3 points of
accuracy.

**The label mix these numbers assume.** Reading 80 comments for Milestones 1
and 2 put a random r/nba comment at roughly 40% `take`, 40% `banter` and 10-15%
`analysis`. The plan is to label the pool in order and then top up `analysis`
from the rest of the pool until it is about a fifth of the file. That leaves
`analysis` with about 8 posts in each test split.

---

## 1. Overall accuracy is at least 0.62 on every seed

`accuracy` in `results.json` is 0.62 or higher on seeds 42, 7 and 2024.

**Why this target:** a model that always answers `take` would score about
0.40 on this mix, and a coin-flip over three labels about 0.33. 0.62 is twenty
points clear of the always-`take` guess, which is about the point where a
moderator could use it to pre-sort a thread and fix fewer than four posts in
ten. It also has to survive three splits of only ~36 posts, where one unlucky
post costs 3 points, so it sits below the 0.70 that sounds nice and isn't
defensible on 165 training posts and about 30 gradient steps.

---

## 2. Every label clears an F1 floor, with a looser one for `analysis`

On every seed, `per_label.take.f1` and `per_label.banter.f1` are at least
0.55, and `per_label.analysis.f1` is at least 0.40.

**Why this target:** `take` and `banter` will each have about 14 posts in the
test split, so their F1 is reasonably steady and 0.55 asks them to be right
more often than wrong on both precision and recall. `analysis` is the smallest
label, with about 8 test posts, so one miss moves its recall by about 12
points; a 0.55 floor there would be decided by luck. 0.40 is still not free:
it can't be met by a model that never predicts `analysis`, which is the most
likely way a three-epoch run on a fifth-of-the-file label fails.

---

## 3. The model doesn't collapse onto one label

On every seed, for each of the three labels, the share of test posts the model
*predicts* as that label is within 15 percentage points of the share that
truly *is* that label. Read off `confusion` in `results.json`: column totals
against row totals, each divided by `n_test`.

**Why this target:** the failure the brief warns about, a model that learns to
guess the big label, can hide inside a decent accuracy here, because `take`
and `banter` are both large. This criterion catches it directly. 15 points is
about 5 of ~36 posts. A model that predicts `analysis` once when 8 posts are
`analysis` (about 3% predicted against 22% true) misses it, while ordinary
mistakes spread across the labels don't.

---

## 4. The labelling agrees with staff on at least 24 of 30 posts

In unit 6, my labels on the 30 staff posts, applied under the staff taxonomy in
`data/staff_taxonomy.md`, match `data/staff_labels.csv` on at least 24 of 30
(0.80), as `agreement.py` reports it.

**Why this target:** this is the one check where somebody else labelled the
same posts, so it is the only evidence that my rules get applied the way a
second reader would apply them. Staff say a rate in the 70s is normal. 0.80
asks for a little better than normal, for a taxonomy-specific reason: the staff
set's hardest rule ("the fact has to be load-bearing") is the same test as my
delete-the-fact rule for `analysis` vs `take`, which the stress test already
drilled. Their `reaction` vs `hot_take` rule is the analogue of my `banter` vs
`take` rule. If the rate falls below 24, the boundary I think I apply cleanly
isn't clean.

---

## 5. Confident predictions are right more often than unsure ones

On every seed, `confidence.accuracy_most_confident_third` is at least 0.20
higher than `confidence.accuracy_least_confident_third`.

**Why this target:** the only use this model's confidence could have is
deciding which posts a person double-checks: hand the least-sure third to a
human. That is worth doing only if the sure third really is better. Each third
is about 12 posts, so a 0.20 gap is two or three posts' difference; anything
smaller is one lucky post, and a gap of zero would mean the confidence number
is decoration. The hard cases on the `take`/`banter` line (sarcasm, furious
reactions with a claim inside) are exactly the posts that should come back
unsure, which is why I expect a gap to exist at all.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
