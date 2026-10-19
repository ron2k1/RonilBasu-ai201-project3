# Milestone 1: the community, and what reading it showed

> The reading below was done by Claude Code, the coding agent I ran this unit
> with, not by me. It pulled the threads, read the comments, and wrote these
> notes. Where a sentence says "the reading", it means that pass.

## The community: r/nba

r/nba is public (no invite, no login to read), enormous, and it argues about
everything. It also has the spread this project needs. One thread holds a
comment that lists a player's series ranks stat by stat, a sincere one-line
verdict on a trade, and three jokes about a running bit, all within a scroll.
It isn't built around one show or one release, so nothing in it is a spoiler.

The comments came from 72 threads collected on 2026-10-19, the week before
the 2026-27 season opens. They span clips, injury news, interviews, `[OC]` stat
posts and prediction threads (`tools/harvest_nba.py`, thread list in
`data/nba_sources.json`). Each comment is one "post" for this project.

## What the reading covered

40 comments, pool rows `p0401` to `p0440`, read in full before any label
existed. They were taken from the middle of the shuffled pool on purpose: the
first rows of the pool become the 20 cold labels in Milestone 4, and those
should be read for the first time when they're labelled.

## Candidate distinctions

Four things the comments actually did differently. Each one is a thing you can
point at, not "good vs. bad".

1. **Some comments put a checkable fact on the table and lean on it. Most
   don't.** `p0439` answers a question with a player's per-series ranks
   ("1st in PTS (122), 2nd in REB (31)..."). `p0435` gives a referee's record
   ("the Pacers were 2-9 in games he officiated"). Next to them, `p0402` ("It
   never made sense to me to keep him over Cisse") is just as confident and
   offers nothing to check.

2. **Some comments take a position someone could argue with. Others aren't
   arguing anything.** `p0429` ("Dundon using it as a reason to relocate is
   bullshit") and `p0436` (a player "is an absolute necessity, our team would
   suffer without him") each invite a "no, you're wrong". `p0425` ("Grand
   opening, grand closing", on the Ben Simmons injury) and `p0440` ("In this
   house, Nick Young is a saint!") are riffs; there is no claim in them to
   disagree with.

3. **Sarcasm puts the words and the meaning on different sides.** `p0426`
   ("Wentz will keep playing like an all-Pro and definitely not tail off
   before then") says one thing and means the opposite, and the opposite is a
   prediction. A labeller going by the surface reads a joke; one going by the
   meaning reads a confident call about how a player's season goes.

4. **A real share of every thread is people talking to each other, not about
   basketball.** `p0427` ("Damn you can't read at all, huh?"), `p0410`
   (sarcasm aimed at other commenters), `p0431` ("How do the boots taste down
   there?"). They're about the conversation, not the sport.

## Where the distinctions went

Distinction 1 became the line between `analysis` and `take`. Distinction 2
became the line between `take` and `banter`. Distinction 3 is the reason that
second line needs a written decision rule (see the README's Label Taxonomy).
Distinction 4 didn't earn its own label: most of those posts aren't asking anyone to
accept a position about basketball, so they're `banter`.

One more thing the reading turned up and the taxonomy deliberately leaves out:
a few comments are only a question ("what's the meatball sub story"). They
aren't analysis, a take, or banter, and there are too few for a label of their
own. They're skipped at labelling time and the skips are counted in the README.
