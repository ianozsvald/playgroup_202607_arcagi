import json
import logging
import os
import base64

from dotenv import load_dotenv
from openai import OpenAI
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_fh = logging.FileHandler("llm_calls.log")
_fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(_fh)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)

def _get_providers(model_name):
    only_providers = "unspecified"
    # https://openrouter.ai/deepseek/deepseek-v3.2-speciale
    if model_name.startswith("deepseek/deepseek-v3.2-speciale"):
        only_providers = ["atlas-cloud"]
    if model_name.startswith("deepseek/deepseek-v4-pro"):
        only_providers = ["baidu"]
    # https://openrouter.ai/deepseek/deepseek-v3.1-terminus
    if model_name.startswith("deepseek/deepseek-v3.1-terminus"):
        only_providers = ["atlas-cloud"]
    if model_name.startswith('qwen/qwen2.5'):
        only_providers = ['nebius']
        #only_providers = ['parasail']
    if model_name.startswith('qwen/qwen3.5-plus') or model_name.startswith('qwen/qwen3.6-flash'):
        only_providers = None # Alibaba only
    if model_name.startswith("z-ai/glm-4.7"):
        only_providers = ["z-ai"]
    if model_name.startswith("anthropic"):
        only_providers = None  # ["anthropic"] gives 521 and 520 errors intermittently
    if model_name.startswith("openai"):
        only_providers = None
    if "gemini-" in model_name:
        only_providers = None #["google"]
    
    # IF YOU GET THIS, you need to add a provider as I've done above
    # to fix 1 single provider for consistency of calls
    assert only_providers != "unspecified", "No provider found for {model_name}, you need to set one in the code"
    return only_providers

def call_llm(prompt, model_name):
    instructions = "Follow the instructions in the prompt template.\n"

    logger.info("Prompt:\n%s", prompt)
    # NOTE we need 'only_providers' to be set otherwise
    # openroute will fall back on other providers with different configurations
    # and quantization levels and we'll get inconsistent results
    only_providers = _get_providers(model_name)
    extra_params = {"provider": {"allow_fallbacks": False, "only": only_providers}}
    logger.info("LLM calling with %s", model_name)
    # extra_params = {}
    while True:
        try:
            response = client.responses.create(
                model=model_name,
                instructions=instructions,
                input=prompt,
                extra_body=extra_params,
            )
            break  # jump out if we're successful
        except json.JSONDecodeError:
            logger.warning("Oops, got a JSONDecodeError after calling LLM")

    logger.info("Raw return from llm call:\n%s", response.output_text)
    extracted = utils.extract_from_triple_backticks(response.output_text)
    logger.info("Extracted answer:\n%s", extracted)
    return extracted


def send_image_to_llm(model_name, prompt, image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_b64}"

    logger.info("Prompt (image):\n%s", prompt)
    only_providers = _get_providers(model_name)
    extra_params = {"provider": {"allow_fallbacks": False, "only": only_providers}}
    logger.info("LLM (image) calling with %s", model_name)

    input_payload = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": image_url},
            ],
        }
    ]

    while True:
        try:
            response = client.responses.create(
                model=model_name,
                input=input_payload,
                extra_body=extra_params,
            )
            break
        except json.JSONDecodeError:
            logger.warning("Oops, got a JSONDecodeError after calling image LLM")

    logger.info("Raw return from image llm call:\n%s", response.output_text)
    return response.output_text


if __name__ == "__main__":
    print("Openrouter API key: ", os.getenv('OPENROUTER_API_KEY')[:12] + "...")

    if False:
        model_name = "google/gemini-3.1-flash-lite"
        print(f"Using model: {model_name}")

        prompt = """
    You are an expert at extracting information from UK charity financial documents.
    You are given a single page of a document as an image.
    Your task is to extract the registere address from the page.

    - If you can find the Registered Address respond with exactly the full address in a single line
    - If you cannot find the Registered Address on this page, respond with exactly: NOT_FOUND

    """

        #image_path = "extracted_pages_as_png/34646877386855695219579059c07302_1.png"
        image_path = "extracted_pages_as_png/44ba842bbbd4f18587ad8ae3fe4ecdd7_3.png"
        result = send_image_to_llm(model_name, prompt, image_path)
        print("Model raw output:")
        print(result)
