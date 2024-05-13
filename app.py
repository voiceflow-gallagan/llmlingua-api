import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from llmlingua import PromptCompressor
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


app = FastAPI()

model = str(os.environ.get("MODEL", "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank"))

# Load the model
compressor = PromptCompressor(
    model_name=model,
    use_llmlingua2=True,
    device_map="cpu"
)

class CompressRequest(BaseModel):
    text: str
    compression_rate: float
    force_tokens: list = ['\n']
    chunk_end_tokens: list = ['.', '\n']

@app.get('/health')
def health_check():
    return {"status": "OK"}

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
    print(model)
    print(results)
    compressed_prompt = results["compressed_prompt"]
    origin_tokens = results["origin_tokens"]
    compressed_tokens = results["compressed_tokens"]
    ratio = results["ratio"]
    rate = results["rate"]
    #saving = results["saving"]

    response = {
        "compressed_prompt": compressed_prompt,
        "origin_tokens": origin_tokens,
        "compressed_tokens": compressed_tokens,
        "ratio": ratio,
        "rate": rate,
        #"saving": saving
    }

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
    #uvicorn.run(app, host="0.0.0.0", port=port, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
