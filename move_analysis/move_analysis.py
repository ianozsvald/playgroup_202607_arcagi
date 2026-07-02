import json
import numpy as np
from llm_openrouter import call_llm
from pprint import pprint

def load_frame_logs(filepath: str, frame_number: int) -> tuple[dict, dict]:
    with open(filepath) as f:
        frames = [json.loads(line) for line in f if line.strip()]
    return frames[frame_number], frames[frame_number + 1]


def make_str_of_arr(arr):
    arr_str = "\n".join(",".join(f"{v:2d}" for v in row) for row in arr)
    return arr_str


def make_prompt(frame1, frame2, move_id):
    preamble = """
You are a game playing machine, you have to help me figure out the controls of the game.
It is played on a 64x64 grid of ints (range 0-15 inclusive)
A move is made which has an integer id, we don't know what the move-id changes.
I'm going to give you a before-frame, a move-id and the after-frame. """

    output_request = """
You need to give me a hypothesis of what the move-id does given the context of the frames.
You must also give a guess about the game type given just the information in these two frames.
Reply with:
{'hypothesis': YOUR_HYPOTHESIS,
 'game_type_guess': YOUR_GAME_TYPE_GUESS}
    """

    frame_before_str = make_str_of_arr(frame1)
    frame_after_str = make_str_of_arr(frame2)

    move_description = f"""\n\nThe move id is {move_id}\n\n"""
    nbr_different_cells = int((frame1 != frame2).sum())
    move_meta = f"""\n\nIn total {nbr_different_cells} cells changed between these two frames."""
    request = """\n\nNow reply with your hypothesis and game_type_guess in as a JSON block as requested."""

    prompt = preamble + output_request + "\n\n" + frame_before_str + move_description  \
             + frame_after_str + move_meta + request + output_request
    return prompt, nbr_different_cells


def make_prompt_from_frames(filename, frame_number):
    frame_n, frame_after = load_frame_logs(filename, frame_number)

    frame_n_arr = np.array(frame_n["data"]["frame"][0])
    frame_after_arr = np.array(frame_after["data"]["frame"][0])
    move_id = frame_n['data']['action_input']['id']

    prompt, nbr_different_cells = make_prompt(frame_n_arr, frame_after_arr, move_id)
    return prompt, nbr_different_cells

if __name__ == "__main__":
    filename = "/home/ian/workspace/personal/playgroup/playgroup_202607_arcagi/ARC-AGI-3-Agents/recordings/"
    filename += "ls20-9607627b.ianagent.80.186746b5-307a-4c35-b741-fb4ac29cb429.recording.jsonl"
    frame_nbr = 53
    prompt, nbr_different_cells = make_prompt_from_frames(filename, frame_nbr)
    print(prompt)


    #model_name = "google/gemini-3.1-flash-lite"
    #model_name = "anthropic/claude-sonnet-4.5" # reasonably quick, somewhat wrong
    #model_name = "qwen/qwen2.5-vl-72b-instruct"
    #model_name = "qwen/qwen3.5-plus-20260420" # very sloww...->
    #model_name = "qwen/qwen3.6-flash" # responds 
    model_name = "openai/gpt-5.5"
    #model_name = "deepseek/deepseek-v4-pro" # slow...-> 

    print(f"Calling {model_name=} from {frame_nbr=} with {nbr_different_cells=}...")
    result = call_llm(prompt, model_name)
    pprint(result)

