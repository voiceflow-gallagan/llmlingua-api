# LLMLingua-2 API | Voiceflow Code Example

This repository contains a FastAPI application designed to compress prompts using the `llmlingua` library and a pre-trained model.

More info about [Microsoft LLMLingua-2](https://llmlingua.com/llmlingua2.html).
Their LLMLingua Github repo: https://github.com/microsoft/LLMLingua

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Docker & Docker Compose installed (see [Docker's official installation guide](https://docs.docker.com/desktop/)).


## Installation

To install this project, follow these steps:

### Clone the repository

```bash
git clone https://github.com/voiceflow-gallagan/llmlingua-api.git
cd llmlingua-api
```

### Create the .env file

```bash
cp .env.template .env
```

Edit the .env file to match your desired settings (default settings should work fine).


### Start the application

```bash
docker-compose up
```

Wait for the application to start, first launch can take time as we need to download the model.
Once it's ready, you should see the following message:

```bash
[+] Running 1/1
 ✔ Container llm-lingua-api  Recreated                                                    0.2s
Attaching to llm-lingua-api
llm-lingua-api  | INFO:     Started server process [1]
llm-lingua-api  | INFO:     Waiting for application startup.
llm-lingua-api  | INFO:     Application startup complete.
llm-lingua-api  | INFO:     Uvicorn running on http://0.0.0.0:3030 (Press CTRL+C to quit)
```
### Test the application

Check that everything is fine by sending a POST request to the `/compress` endpoint.

```bash
curl -X POST "http://localhost:3030/compress" -H "Content-Type: application/json" -d '{
    "text": "John: So, um, I have been thinking about the project, you know, and I believe we need to, uh, make some changes. I mean, we want the project to succeed, right? So, like, I think we should consider maybe revising the timeline.\nSarah: I totally agree, John. I mean, we have to be realistic, you know. The timeline is, like, too tight. You know what I mean? We should definitely extend it.",
    "compression_rate": 0.55,
    "force_tokens": ["\n", ".", "!", "?", ","],
    "chunk_end_tokens": [".", "\n"]
}'
```

##### Expected response
```json
{
  "compressed_prompt": "John : So, um been thinking about project, believe we need to, make some changes., want project to succeed, right?, like, think should consider maybe revising timeline. \n Sarah : agree, John., have to be realistic,. timeline is, like, too tight. know what mean? should extend it.",
  "origin_tokens": 98,
  "compressed_tokens": 64,
  "ratio": "1.5x",
  "rate": "65.3%"
}
```

### Run
If previous test succeeded, you can stop the container using `CTRL+C` and run it again in detach mode using
```bash
docker-compose up -d
```

### Demo Video
https://youtu.be/1LMXbJxLCiI


