
Set .env file using .env.template
PORT=3030
MODEL=microsoft/llmlingua-2-xlm-roberta-large-meetingbank

docker-compose up -d

https://github.com/microsoft/LLMLingua


curl -X POST "http://localhost:8000/compress" -H "Content-Type: application/json" -d '{
    "text": "John: So, um, I'\''ve been thinking about the project, you know, and I believe we need to, uh, make some changes. I mean, we want the project to succeed, right? So, like, I think we should consider maybe revising the timeline.\nSarah: I totally agree, John. I mean, we have to be realistic, you know. The timeline is, like, too tight. You know what I mean? We should definitely extend it.",
    "compression_rate": 0.55,
    "force_tokens": ["\n", ".", "!", "?", ","],
    "chunk_end_tokens": [".", "\n"]
}'
