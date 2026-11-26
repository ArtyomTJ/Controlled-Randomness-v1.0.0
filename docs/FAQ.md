# FAQ

### Is this pseudoscience?

The project becomes science when its claims are operationalized, measured,
and falsifiable. v1.0 separates two claims: H1 (the selection rule biases
the source) is falsified for the reference architecture; H2 (a conscious
observer biases a live source) is stated as a testable hypothesis with a
preregistered protocol. The repository does not assume H2 is true. It
builds the experiment that would make a "yes" credible.

### Why does the original program fail?

Because the selection rule only updates the auxiliary pair $(x,y)$. The
generator and the stopping predicate never read $(x,y)$. For a fixed seed,
both arms are the same experiment. See [`MATH.md`](MATH.md).

### If the effect is real, why use a quantum RNG?

A classical PRNG is a deterministic program seeded by the clock. There is no
physical process for an observer to influence. A live quantum source is the
cleanest physical source with documented randomness; it is also the
standard choice in the experimental literature on intention and randomness.
A hardware noise source can be used as a secondary condition, but it must
be live and characterized.

### Why human-chosen targets instead of human selection on every draw?

The original rule's per-draw selection is causally isolated from the
stopping predicate. A human pressing "keep" cannot change $T$ through the
program. The observer's intention can still be encoded in the choice of
target, which is scalable and easy to blind. A per-draw selection arm is
included as an exploratory condition for a smaller alphabet.

### What about my experience in Warframe?

Game rolls are server-side and the client's choice of which mod to keep is
not an input to the next roll. The feeling that "similar stats come faster"
is consistent with well-known effects: clustering in random sequences,
confirmation bias, selective memory, and small samples. If you want to test
it, log every roll, not only the successes, and compare the frequencies with
the published drop tables.

### What would convince skeptics?

A preregistered, adequately powered experiment on a live source, with a
positive effect, a confidence interval, and an independent replication.
A single laboratory result — especially a single run — will not.

### Can I run this at home?

Yes, for the null experiment: [`../experiments/run_v1.py`](../experiments/run_v1.py)
and the C++ program require no special hardware. For H2 you need a live
physical source and a human participant; a prerecorded file is not enough.

### Why publish a null result?

Because it is a real result. It falsifies H1, it identifies the missing
ingredient in the original experiment, and it prevents the next researcher
from repeating the same design error. A project that reports only positive
results is not a research program.

### What is the "observer" in the protocol?

A human participant who chooses the target before the trial. The protocol
does not require the participant to watch every draw; it requires the
intention to be fixed and timestamped before the source runs. The
exploratory arm adds per-draw selection for a smaller alphabet.

### What are the main failure modes?

- Optional stopping without a sequential boundary.
- Post hoc target changes.
- Source drift or a faulty health check.
- Unblinding before the dataset is frozen.
- Pooling exploratory and confirmatory endpoints.
- Publication bias: only positive results get written up.

The protocol in [`PROTOCOL.md`](PROTOCOL.md) addresses each of these.
