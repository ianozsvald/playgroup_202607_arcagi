# Playgroup 2026-07: ARC AGI

> [!NOTE]
> During 2026-07 I'm running another [Playgroup](https://playgroup.org.uk/), this time on the wonderful ARC AGI 2026 benchmark.

## Getting Started

The more you do, the more you'll get from the day. The first two bullets are a great starting point.

- [Try some challenges](https://arcprize.org/tasks?v=3) and think about 'how you figure out how to solve them'
- [Set up your local machine and get an ARC key](https://docs.arcprize.org/) (see below)
- Check the `EXPERIMENTS.md` file by this `README.md` to see notes on the agents that have been provided
- Join `#arc-agi` in the playgroup Slack
- Overview paper: [ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence](https://arxiv.org/abs/2603.24621)
    - [paper summary on Emergent Mind](https://www.emergentmind.com/papers/2603.24621)
- See the Kaggle competition leaderboard note below. There are 3 benchmark solutions; finding these and reading about them is a good clue for how to get going.
- [30-day write-up from the pre-v3 competition](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings) has useful background (includes links to public solutions)
- [GPT 5.5 & Opus 4.7 analysis](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis) via https://arcprize.org/blog
- ["Core knowledge" by Elizabeth S. Spelke and Katherine D. Kinzler](https://www.harvardlds.org/wp-content/uploads/2017/01/SpelkeKinzler07-1.pdf). This is the assumed mammal-like core knowledge that Chollet believes our agents should just understand, and the games depend on it.

## Non-Agent Mode (smoke test)

From the `playgroup_202607_arcagi` folder, clone the ARC AGI repo (pinned to a known-good commit, ensures we are all on the same version), install it, and run the quickstart:

```bash
playgroup$ git clone git@github.com:ianozsvald/playgroup_202607_arcagi.git # clone _this_ repo
cd playgroup_202607_arcagi

# pinned 2026-06-10
git clone git@github.com:arcprize/ARC-AGI.git && cd ARC-AGI && git checkout f12822c4
# (don't worry about the detached head warning, you can always 
# `git log`, then `git checkout HEAD` and `git log` so see how far behind you are)

# Builds the arc-agi package
uv sync

# Verify it works!
uv run quickstart.py
# you'll see the random-move (non llm) agent moving the blob around your shell until it runs out of time
```

> [!NOTE]
> Read `quickstart.py` — it's only two pages and shows a random (non-LLM) mover in the shell, running for 100 steps which includes many restarts (you get the yellow screen when it runs out of energy and restarts). 

You could change to eg. `for step in range(3):` to limit from 100 down to 3 steps, then it is easy to scroll back and see the logging that preceded the game. You'll see that you have an _anonymous scorecard_, you need register for an ARC AGI API key to change this so you can see a history online.

### Get an ARC AGI key

See the [API keys reference](https://docs.arcprize.org/api-keys).

[Log in to the ARC platform](https://arcprize.org/platform) with GitHub or Google. I had to revisit that link to reach the [user page](https://arcprize.org/platform/user). Copy your key and edit `.env` in `ARC-AGI` to read `ARC_API_KEY=4...` (_not_ `ARC_AGI_API`-> https://github.com/arcprize/ARC-AGI-3-Agents/issues/77). Verify: when you run a project it shouldn't report "anonymous key" in the log output.

Traces of example runs appear (delayed) on your [scorecards page](https://arcprize.org/scorecards) (login required).

Without an API key your log (pasted to the screen) will look like:

```
ARC-AGI$ uv run quickstart.py
INFO:arc_agi.scorecard:Initialized ScorecardManager with idle_for=0:15:00 and max_open_for=3 days, 0:00:00
2026-06-29 12:43:54 | INFO | *Got anonymous API key:* b33391fb-5da8-442d-93ed-97c6edd26758
2026-06-29 12:43:54 | INFO | *You can register for an API key at https://three.arcprize.org*
...
```

When you have the API key correctly setup, you should get something similar to (rather than the _anonymous_ API key log):

```
INFO:arc_agi.scorecard:Initialized ScorecardManager with idle_for=0:15:00 and max_open_for=3 days, 0:00:00
2026-06-29 12:02:54 | INFO | Successfully fetched 25 environment(s) from API
2026-06-29 12:02:54 | INFO | *Created new scorecard* : 1c4f2b33-dc9f-432f-a12b-5bab94747c55
```


Note that whilst your API key is setup, this run isn't logged (Ian note - I don't know why, I guess there's a switch to flip somewhere in their default code?). This doesn't stop you, you'll see the online scorecard in the Agents section next.

Following the [Play your first game](https://docs.arcprize.org/#3-play-your-first-game) docs, you can create `my-play.py` (non-LLM) in the same folder and run it:

```bash
# Note: File won't exist by default, see link above to grab the code!
uv run my-play.py
```

The player blob runs off the top of the screen. That's the basic code for writing a non-LLM bot. To move on to an LLM-guided bot, see the [LLM agents notes](https://docs.arcprize.org/llm_agents).

> [!NOTE]
> THINK - why does this bit of code not solve that environment?

## Agent Mode

### 1. Get Agents Repo

From the `playgroup_202607_arcagi` folder (repo root), clone the agents repo (pinned) and set up the environment:

```bash
$ pwd # ... /playgroup_202607_arcagi - check you're not in ARC-AGI still!

# pinned 2026-05-28
git clone git@github.com:arcprize/ARC-AGI-3-Agents.git && cd ARC-AGI-3-Agents && git checkout 10213de8

# Prep the environment file
cp .env.example .env

# Builds the arc-agi Agents package
uv sync

```

### 2. Get an ARC AGI key (same as above)

See the [API keys reference](https://docs.arcprize.org/api-keys).

[Log in to the ARC platform](https://arcprize.org/platform) with GitHub or Google. I had to revisit that link to reach the [user page](https://arcprize.org/platform/user). Copy your key and edit `.env` in `ARC-AGI` to read `ARC_API_KEY=4...` (_not_ `ARC_AGI_API`-> https://github.com/arcprize/ARC-AGI-3-Agents/issues/77). Verify: when you run a project it shouldn't report "anonymous key" in the log output.

Traces of example runs appear (delayed) on your [scorecards page](https://arcprize.org/scorecards) (login required).

### 3. Get an OpenAI Key

[Log in to OpenAI](https://platform.openai.com/home), fund your account, and create an [API key](https://platform.openai.com/api-keys). A run of the reasoning agent example code costs about $0.50, I've funded $25 and I think this is overkill for the day (and it is easy to top up, so maybe start with $10).

### 4. Setup environment

Edit `.env` to set `ARC_API_KEY` and `OPENAI_API_KEY`. I commented out `AGENTOPS_API_KEY`.

*maybe not needed now in 2026-06* Change `HOST` so it reads `HOST=arcprize.org` (i.e. drop the `three.`), else you'll get an error trying to follow the scorecard URL. See https://github.com/arcprize/ARC-AGI-3-Agents/issues/78.

### 5. Test Non-LLM Agent

Run the non-LLM random agent (this also installs the uv environment), then follow the scorecard URL at the end and watch the replay:

```bash
uv run main.py --agent=random --game=ls20
```

> [!NOTE]
> If you didn't edit `HOST` in the step above, your scorecard url at the end of the log will be wrong - strip `three.` from the start to see your scorecard and log. See [All scorecards](https://arcprize.org/scorecards). You're hoping to see something like `2026-06-29 13:02:06,487 | INFO | View your scorecard online: https://arcprize.org/scorecards/766138e0-a880-4e4c-9fca-3b1eafe06b8c` (note the lack of `three.` in the URL).

If you visit https://arcprize.org/platform/scorecards you'll see your runs, the most recent will be the most you just run (hopefully the `random` one above!), click through to that scorecard, then on the right side about halfway down the screen you'll see 'Replay', click the Play icon, you should see the moves animated plus a reasoning log on the right (there's no reasoning, it is just a log of moves).

### 6. Test LLM Agent

Next, visit the [agents quickstart](https://docs.arcprize.org/agents-quickstart), then run the LLM agent (uses your OpenAI key):

```bash
uv run main.py --agent=llm --game=ls20
```

Source: [`llm_agents.py` line 16](./ARC-AGI-3-Agents/agents/templates/llm_agents.py#L16). This took about 2 minutes and $0.09 with `gpt-4o-mini` on my run. Check your [OpenAI balance](https://platform.openai.com/home). Note if you look at the Replay on the scorecard you'll see the moves, but there's no reasoning log - I don't know why!

### 7. Test Guided LLM Agent

Then try the guided LLM agent which has a prompt that's a human-solution to one style of challenge. It doesn't solve `ls20` in my testing, what are we missing? Maybe it is meant for a different challenge?

```bash
uv run main.py --agent=guidedllm --game=ls20
```

Source: [`llm_agents.py` line 496](./ARC-AGI-3-Agents/agents/templates/llm_agents.py#L496).

Visit the scorecard URL that's printed at the end of the run, use the 'play' icon under the 'replays' column and see a video of each frame of the action. What did it get wrong? This scorecard _does_ show a reasoning log (phew). Note that you can `CTRL c` to break out early as with `o3` (the default on this model) it is very slow. You should definitely read the code to check the prompt - it is not a great prompt.

> [!NOTE]
> Whilst the prompt may not _fit_ `ls20` I reckon it is easy to fix it up - maybe this is a *first good challenge*?

#### Rate limiting on lower Tier

In my console log I see `openai.RateLimitError: Error code: 429 - {'error': {'message': 'Rate limit reached for o3 in organization org-gGYdAa4Kw4x1W2XdSybgjxrl on tokens per min (TPM): Limit 30000, Used 26862, Requested 8137. Please try again in 9.998s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}` so probably that's the problem...

Visiting https://platform.openai.com/settings/organization/limits shows that I'm on Tier 1 (with $25 on account) and if I go to $50 on account then I get upgraded to Tier 2. I put myself over $50 and indeed I go up to Tier 2 and my `o3` limit jumps up a lot. It suggests I commit $100 to go up another Tier. Oh, this could get expensive!

### Optional - AgentOps

Looking in `ARC-AGI-3-Agents` I see `llm.txt` which explains how to install agentops for "realtime monitoring and debugging".

### 8. Where next?

* does the prompt in `guidedllm` solve `ls20` or another environment? Try this as a *first good challenge*
* try hand-describing the rules for _another_ environment, modifying `guidedllm`
* rather than prescribing the solution (i.e. `guidedllm` in the prior step), how do we describe _how to figure out how to discover a solution?_
* let's discuss this on the whiteboard - what might we try?
* maybe you want an Anthropic solution, that should need very few code changes

## If you want to go deeper...

### Kaggle description

- [Competition overview](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/overview)
- [Competition data](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/data) — sign in, "Join the competition", "Accept"
- [Leaderboard](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard)
    - Circa 500 teams. 'Stochastic Goose' with 0.25 at rank 220, 'Random Agent' with 0.12 at rank 430, 'Just Explore' with 0.06 at rank 510. Figuring out how these benchmark (non-agentic?) solutions work is a good starting point.
    - [Stochastic Goose](https://github.com/DriesSmit/ARC3-solution)
    - [Blind Squirrel](https://github.com/wd13ca/ARC-AGI-3-Agents)
    - [Play Zero](https://github.com/dhanaabhirajk/ARC-AGI-3-Agentsa) (preview comp)
    - [Explore it Till You Solve It](https://github.com/dolphin-in-a-coma/arc-agi-3-just-explorea) (preview comp)
    - [Fluxonian](https://github.com/FluxonApps/arc-prize-v3-2025) (preview comp)
