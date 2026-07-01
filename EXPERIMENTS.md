# Some early experiments that you could follow

To see the bot code get into `/ARC-AGI-3` or look at https://github.com/arcprize/ARC-AGI-3-Agents/

You can see the tasks here: https://arcprize.org/tasks

*Uncertainties for Ian and playgroup to resolve*

* The random bot has a 'reason log' but the online scorecard shows 'no reasoning log captured' - what am I missing?
  * I think it has something to do with `action.reasoning` being recorded in some implementations.
* When an agent talks about the _colours_ in a grid (e.g. colour 4, 3 etc) - open a snapshot URL and you can mouse-over each cell to learn what number represents the colour

## random bot (no llm)

Following the [quickstart](https://docs.arcprize.org/agents-quickstart#step-2-run-an-agent) we can run a non-LLM random-move agent. You can see the code in `agents\templates\random_agent.py` ([online](https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/random_agent.py)). It inherits from `Agent` and so becomes discoverable by `main.py`.

This is a fast random-choice both, it doesn't have a goal. If you look at the code you'll see it is short:
* `MAX_ACTIONS` is set to 80, for 80 steps (common to the other bots too)
* `is_done` checks for `GameState.WIN`
* `choose_action` takes a random move and logs a 'reason'

```
ARC-AGI-3-Agents$ uv run main.py --agent=random --game=ls20
...
2026-04-23 10:50:20,723 | INFO | View your scorecard online: https://arcprize.org/scorecards/faaa67f7-a2ed-428a-a6f4-08ad18b40076
```

You'll end with a scorecard URL like the above (for your login), in there you can view a replay.

> [!NOTE] 
> One of the published solutions (not in this repo) takes a _log_ of an execution, which could be this random bot, and then an LLM _analyses_ the trace to see 'what happened' in response to decisions. E.g. moving into a wall means no movement, moving away from a wall teaches us that we can move in this environment in 4 directions. 

## `LLMAgent` with `gpt-4o-mini`, has observation, no tools

Described: https://docs.arcprize.org/llm_agents

Code: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/llm_agents.py#L16

[Actions](https://github.com/arcprize/ARC-AGI-3-Agents/blob/e61e1238eac285901423afc3921fe4b1a51c6701/agents/templates/llm_agents.py#L269) are described in the code:
* `ACTION1` Up
* `ACTION2` Down 
* `ACTION3` Left 
* `ACTION4` Right
* `ACTION5` Space
* `ACTION6` Click (needs an x,y coord)

I suggest changing `MAX_ACTIONS` to e.g. 10 from 80, else it'll take a while to complete. However you can `ctrl c` to break out and it'll still give you the scorecard URL for the partial run.

```
ARC-AGI-3-Agents$ uv run main.py --agent=llm --game=ls20
```

The prompt is generic and not tuned for `ls20`, see it here https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/llm_agents.py#L361

You'll see from the log (below) that it doesn't know _how_ to play the game.

```
2026-04-23 11:09:12,148 | INFO | Assistant: The current frame consists of a largely homogeneous grid where the values are mostly 5, 4, and some 3s, with a few 9s appearing near the end of the grid. The repeated 5s indicate a solid base level, while the 4s and lower values suggest potential areas for action. However, the main action should focus on surrounding the areas with lower values to consolidate scoring opportunities.

There's a distinct cluster of lower values toward the middle-left area, which should be targeted to maximize the score while minimizing actions. The high density of 5s indicates a stable foundation, and targeting the clusters of 3s is essential as they could be beneficial for increasing the overall score in this frame. 

To proceed effectively, I will call an action that targets these lower-value regions to increase the score while maintaining the integrity of the higher-value areas. Therefore, I will focus on surrounding the cluster of 3s. 

**Action:** I will call the action to target the cluster of low values, aiming to convert them into higher values or at least improve their vicinity to increase scoring potential for the next overall frame.
2026-04-23 11:09:12,148 | INFO | Sending to Assistant for action...
2026-04-23 11:09:14,885 | INFO | Received 13036 tokens, new total 25768
2026-04-23 11:09:15,321 | INFO | ls20-9607627b - ACTION2: count 1, levels completed 0, avg fps 0.05)

```

In my run it just kept trying `ACTION2` which is Down, but it started on the bottom bar, so it went nowhere.

> [!NOTE]
> How might the prompt be changed to help it understand _this_ game, rather than the rather crazy ideas it proposes at each step? How could we _discover_ those ideas?

> [!NOTE]
> Could we show the agent that _the last choice made no change in the environment_? If so, we could ask it to at least try something else?

## `FastLLM` with `gpt-4o-mini`, no observation

This sets `DO_OBSERVATION = FALSE` which means that the step in `LLM` (the parent class) that sends the current grid to the LLM for a description is _skipped_. This agent is therefore rather blind!

## `ReasoningLLM` with `o4-mini`, has observation and tools

Described: https://docs.arcprize.org/llm_agents#reasoningllm

Code: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/llm_agents.py#L403

```
ARC-AGI-3-Agents$ uv run main.py --agent=reasoningllm --game=ls20
```

This also has the simplistic prompt (it inherits it from `LLM`) so the following trace shows that it doesn't understand this environment.

```
2026-04-23 11:51:33,598 | INFO | Assistant: Our character (the single “0”) is tucked into a narrow side-chamber in the lower half of the map, just beneath a pair of breakable blocks (“1”). The large cache of “11” tokens in the bottom-right is currently ringed by hazard tiles (the “8”s) and will require opening that choke point to the left of the wall. It looks safer to skirt the mid-level “9” traps by using the western corridor, clear the breakable blocks above us, then swing around to approach the treasure from the flank.
2026-04-23 11:51:33,598 | INFO | Sending to Assistant for action...
2026-04-23 11:51:39,824 | INFO | Received 13384 tokens, new total 26729
2026-04-23 11:51:40,260 | INFO | ls20-9607627b - ACTION1: count 1, levels completed 0, avg fps 0.06)
...
2026-04-23 11:56:25,089 | INFO | Assistant: The map shows a narrow corridor running east–west through the middle, with a cluster of high-value (“9”) targets slightly to the right. There’s a small open area with “11” power-ups near the bottom center; grabbing one would give us a critical boost before engaging. Next, we should veer south to secure that power-up, then approach the enemy cluster from the flank rather than charging straight down the corridor.
2026-04-23 11:56:25,089 | INFO | Sending to Assistant for action...
...
2026-04-23 11:57:29,367 | INFO | Assistant: We’ve successfully dropped into the open courtyard—no enemy patrols in immediate range. I can see the string of 11-strength power-ups still a few rows below and offset to the right. It’s safe to keep pressing south to collect an 11 next, then pivot east to line up on that flank path toward the 9-strength defenders. continuous downward movement will grab the boost before we advance on the enemy cluster.
2026-04-23 11:57:29,367 | INFO | Sending to Assistant for action...
...
```

It certainly looks like this model thinks it is in a war game and is mis-identifying powerups and potential enemies. 

## `o3` based `GuidedLLM` with `ls20` prompt, has observation and tools

Description: https://docs.arcprize.org/llm_agents#guidedllm

Code: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/llm_agents.py#L496

Prompt: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/llm_agents.py#L569

```
ARC-AGI-3-Agents$ uv run main.py --agent=guidedllm --game=ls20
```

Note that it quickly spots "my avatar" but the location described is the white cross of the key-changer and the avatar description doesn't make sense. It makes a move (up, `ACTION1`), then describes that the rotator is directly ahead (that's the exit gate, not the rotator).

It later notes that it hasn't moved so chooses to go left, but the visual replay shows it moving up.

After this it gets confused, resets itself a couple of times and just goes it circles.

```
2026-04-23 12:19:08,857 | INFO | Assistant: I can spot my 4×4 avatar: two rows of zeros then two rows of fours sitting on the sea of floor-tiles marked ‘3’, roughly a third of the way down the map (about row 31, column 21).  All around me in every direction is open floor (‘3’s), with the nearest solid walls made of ‘5’s a good distance away; so I’m free to move.  The key-/colour-rotator blocks (‘9’s) sit far above me toward the centre-top of the level, while the exit door framed by ‘11’s is far below near the bottom.  Therefore the first leg of the journey is to head generally upward (and a little right) through the open hall toward the rotators, steering clear of any ‘5’ walls.
...
2026-04-23 12:25:35,648 | INFO | Assistant: We seem not to have moved after two upward commands, so something is blocking directly above; squares to our immediate left are just floor (3s), so shifting left should confirm our position and maybe let us skirt whatever is above.
..
```

> [!NOTE]
> I _think_ helping it see that a change did or didn't occur (deterministically) is probably sensible. Maybe we could give it rules about the order of play? This doesn't solve the wider problem about figuring out how to solve these environments afresh, but at least we'd have a bot following our guidance

## `MyCustomLLM`, has observation, `gpt-4o-mini`

This is listed at the end of `llm_agents.py` as a skeleton that you can expand.

You can check which agents `main.py` can "see" with:
```
$ uv run main.py --help
...
options:
  -h, --help            show this help message and exit
  -a {llm,reasoningllm,fastllm,guidedllm,guidedllmian4,langgraphfunc,langgraphtextonly,langgraphrandom,langgraphthinking,multimodalllm,random,smolcodingagent,smolvisionagent ... (and a lot of other crap)
```

## `ReasoningAgent` with `o4-mini`, observation, 400 max actions

Code: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/reasoning_agent.py#L44

This appears to be a more sophisticated agent. The prompt _sort of_ matches `ls20` but doesn't fully describe it, so I'm not sure which environment it is meant to match. 

Maybe this is a *second good investigation* to figure out which environment fits this?

## `SmolCodingAgent` and `SmolVisionAgent`

Code: https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/templates/smolagents.py

I don't know anything about these.

# Thought for an experiment 

Inside `ARC-AGI-3/agents/templates/llm_agents.py` previously I'd added the following block of code.  It is a variant of the existing `GuidedLLM` with a corrected prompt that fits `game=ls20`. I tried this with `gpt-5.2` and it took up to an hour and cost the better part of $10 and then execution stopped (on repeated tries). 

You could try either inserting this variant Agent, or modifying the existing `GuidedLLM` with the better prompt. You could try other LLMs (e.g. gpt 5.4 mini, or gpt 5.4 or gpt 5.5 via https://developers.openai.com/api/docs/models/all). You could try varying the prompt. Can you get it to work?


class GuidedLLMls20(LLM, Agent):
    """Similar to LLM, with explicit human-provided rules in the user prompt to increase success rate."""

    MAX_ACTIONS = 150
    DO_OBSERVATION = True
    #MODEL = "o3"
    #MODEL = "gpt-5.4" # Function tools with reasoning_effort are not supported for gpt-5.4 in /v1/chat/completions. Please use /v1/responses instead.', 'type': 'invalid_request_error
    MODEL = "gpt-5.2"
    print(f"*******************Using model: {MODEL}")
    MODEL_REQUIRES_TOOLS = True
    MESSAGE_LIMIT = 10
    REASONING_EFFORT = "high"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._last_reasoning_tokens = 0
        self._last_response_content = ""
        self._total_reasoning_tokens = 0

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        """Override choose_action to capture and store reasoning metadata."""

        action = super().choose_action(frames, latest_frame)

        # Store reasoning metadata in the action.reasoning field
        action.reasoning = {
            "model": self.MODEL,
            "action_chosen": action.name,
            "reasoning_effort": self.REASONING_EFFORT,
            "reasoning_tokens": self._last_reasoning_tokens,
            "total_reasoning_tokens": self._total_reasoning_tokens,
            "game_context": {
                "score": latest_frame.levels_completed,
                "state": latest_frame.state.name,
                "action_counter": self.action_counter,
                "frame_count": len(frames),
            },
            "agent_type": "guided_llm",
            "game_rules": "locksmith",
            "response_preview": self._last_response_content[:200] + "..."
            if len(self._last_response_content) > 200
            else self._last_response_content,
        }

        return action

    def track_tokens(self, tokens: int, message: str = "") -> None:
        """Override to capture reasoning token information from o3 models."""
        super().track_tokens(tokens, message)

        # Store the response content for reasoning context (avoid empty or JSON strings)
        if message and not message.startswith("{"):
            self._last_response_content = message
        self._last_reasoning_tokens = tokens
        self._total_reasoning_tokens += tokens

    def capture_reasoning_from_response(self, response: Any) -> None:
        """Helper method to capture reasoning tokens from OpenAI API response.

        This should be called from the parent class if we have access to the raw response.
        For o3 models, reasoning tokens are in response.usage.completion_tokens_details.reasoning_tokens
        """
        if hasattr(response, "usage") and hasattr(
            response.usage, "completion_tokens_details"
        ):
            if hasattr(response.usage.completion_tokens_details, "reasoning_tokens"):
                self._last_reasoning_tokens = (
                    response.usage.completion_tokens_details.reasoning_tokens
                )
                self._total_reasoning_tokens += self._last_reasoning_tokens
                logger.debug(
                    f"Captured {self._last_reasoning_tokens} reasoning tokens from o3 response"
                )

    def build_user_prompt(self, latest_frame: FrameData) -> str:
        return textwrap.dedent(
            """
# CONTEXT:
You are an agent playing a dynamic game. Your objective is to
WIN and avoid GAME_OVER while minimizing actions.

One action produces one Frame. One Frame is made of one or more sequential
Grids. Each Grid is a matrix size INT<0,63> by INT<0,63> filled with
INT<0,15> values.

You are playing a game called LockSmith. Rules and strategy:
* RESET: start over, ACTION1: move up, ACTION2: move down, ACTION3: move left, ACTION4: move right (ACTION5 and ACTION6 do nothing in this game)
* you may may one action per turn
* your goal is find and collect a matching key then touch the exit door
* 6 levels total, score shows which level, complete all levels to win (grid row 62)
* start each level with limited energy. you GAME_OVER if you run out (grid row 61)
* your player is a 5x5 square: [[12,12,12,12,12], [12,12,12,12,12], [9,9,9,9,9], [9,9,9,9,9], [9,9,9,9,9]]
* the grid represents a birds-eye view of the level
* walls are made of INT<4>, you cannot move through a wall
* walkable floor area is INT<3>
* current key is shown in bottom-left of entire grid
* the exit door is a 9x9 square with INT<5> interior
* to find a new key shape, touch the key rotator, a 4x4 plus sign denoted by INT<0> and INT<1> 
* if the key shape in the bottom left corner matches the exit door, avoid the key rotator and move towards the exit door
* if the shape doesn't match, rotate more than once, move 1 space away from the rotator and back on
* continue rotating the shape and color of the key until the key matches the one inside the exit door (scaled down 2X)
* if the grid does not change after an action, you probably tried to move into a wall

An example of a good strategy observation:
The player 5x5 made of INT<12> and INT<9> is standing by a wall of INT<4>, so I cannot move up anymore and should
move towards the rotator with a good choice of action.

# TURN:
Call exactly one action.
        """.format()
        )


