from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from llmlingua import PromptCompressor
import tiktoken

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

""" llm_lingua = PromptCompressor()
compressed_prompt = llm_lingua.compress_prompt(prompt, instruction="", question="", target_token=200) """

# Load the pre-trained model
compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
    use_llmlingua2=True,
    device_map="cpu"
)
tokenizer = tiktoken.encoding_for_model("gpt-4")

class CompressRequest(BaseModel):
    text: str
    compression_rate: float
    force_tokens: list = ['\n']
    chunk_end_tokens: list = ['.', '\n']

@app.post("/compress")
async def compress_text(request: CompressRequest):
    original_prompt = request.text
    compression_rate = request.compression_rate
    force_tokens = request.force_tokens
    chunk_end_tokens = request.chunk_end_tokens

    if '\\n' in force_tokens:
        idx = force_tokens.index('\\n')
        force_tokens[idx] = '\n'

    results = compressor.compress_prompt_llmlingua2(
        original_prompt,
        rate=compression_rate,
        force_tokens=force_tokens,
        chunk_end_tokens=chunk_end_tokens,
        return_word_label=False,
        drop_consecutive=True
    )
    print(results)
    compressed_prompt = results["compressed_prompt"]
    n_word_compressed = len(tokenizer.encode(compressed_prompt))

    word_sep = "\t\t|\t\t"
    label_sep = " "
    lines = results["fn_labeled_original_prompt"].split(word_sep)
    preserved_tokens = []
    for line in lines:
        word, label = line.split(label_sep)
        preserved_tokens.append((word, '+') if label == '1' else (word, None))

    response = {
        "compressed_prompt": compressed_prompt,
        #"preserved_tokens": preserved_tokens,
        "n_word_compressed": n_word_compressed
    }

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
