# Stress test: eight posts built to sit on the boundaries

A separate Claude agent (a fresh context with no access to the pool) got the
three draft definitions and this instruction: write eight short r/nba-style
comments that deliberately sit on the boundaries between the labels, spread
across all three boundaries, with no labels and no commentary. These are
generated posts. They are **not** in `labels.csv` and never will be; they only
tested the definitions.

The calls below were made by Claude Code (the agent running this project)
against the draft definitions first, then against the rules as revised.

**Draft definitions tested**

- `analysis`: an argument whose main support is a specific, checkable fact.
- `take`: a sincere opinion, judgment or prediction, offered without a
  checkable fact doing the work.
- `banter`: a joke, a bit, a sarcastic jab or a quick feeling that isn't asking
  anyone to accept a position.

| # | Post | Clean under the draft? | Call after revision |
|---|---|---|---|
| 1 | sga is the best player on the planet and it's not even a debate anymore. scoring title, mvp, finals mvp all in the same season. what else do yall want from the man | Yes. The three awards are the whole argument | `analysis` |
| 2 | ant has been ass in the biggest games of his career. back to back wcf exits in 24 and 25 and both times he disappeared when it mattered. at some point that's just who he is | **No.** The exits are offered as the reason, but they're team results and don't show he played badly. Is that "doing the work"? | `analysis`: delete the exits and "both times he disappeared" has nothing behind it. A weak reason is still the reason |
| 3 | jokic put up 29/12/10 in 24-25 and finished second in mvp voting lmao. guy needs to average a quadruple double and drive the team bus to get one apparently | Mostly. Sarcastic, but the stat line is the reason he was robbed | `analysis` |
| 4 | wemby is gonna win dpoy every single year until he retires and then they're renaming the trophy after him. not even joking | Yes | `take` |
| 5 | jaylen brown signed for 304 million and still dribbles with his left hand like it's gonna explode. celtics really paid for that | **No.** A contract figure, then a jab. Is the figure the reason, or the set-up? | `take`: delete the figure and the jab lands the same. The position (his handle isn't worth it) rests on nothing checkable |
| 6 | nico harrison should be legally barred from making phone calls. luka in purple and gold still feels like a fever dream | Wobbly. Written as a joke and a feeling | `take`: a reply could say "the trade was fine". The joke carries a position |
| 7 | kd shot like 53% from the field at 36 on a dogshit suns team. houston didn't trade for a washed guy, they got the second best scorer in the league | Yes. 53% at 36 is the reason he isn't washed | `analysis` |
| 8 | knicks fired thibs right after their first ecf trip in 25 years and replaced him with mike brown. yeah this is gonna go great | **No.** Is the point that firing a winning coach was dumb (the fact carries it) or that Mike Brown is bad (nothing carries it)? | `analysis`, but only by the tie-break: most of the words are the ECF fact |

**What changed because of it**

- The `analysis` rule got its delete-the-fact test (posts 2, 5 and 8).
- "Whether the fact is a good reason doesn't matter" was added after post 2.
  Without it, labelling `analysis` would mean judging whether the argument is
  right, and two labellers would disagree about basketball instead of about
  the post.
- `take` lost the word "sincere". Post 6 isn't sincere in tone and still
  commits to a position, so "sincere" pointed the wrong way.

**What it didn't test.** None of the eight came back as plain `banter`. Asked
for boundary posts, the agent wrote opinions dressed as jokes, not jokes that
hold no opinion. So the `banter` side of the hardest boundary got its test
from the real reading (`p0425`, `p0440`, `p0454`), not from this.
