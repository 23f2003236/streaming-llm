from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

@app.post("/stream")
async def stream_llm(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    async def event_generator():
        try:
            insights = [
                "Insight 1: Customer satisfaction increased by 18% among users who adopted flexible work schedules. ",
                "Insight 2: 62% of respondents reported higher productivity in remote settings compared to office environments. ",
                "Insight 3: Survey data shows that communication tools directly correlate with engagement scores. ",
                "Insight 4: Teams with structured feedback loops showed 25% better retention rates. ",
                "Insight 5: Data suggests that hybrid models balance collaboration and autonomy effectively."
            ]

            for chunk in insights:
                data = {
                    "choices": [
                        {"delta": {"content": chunk}}
                    ]
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.5)  # simulate streaming delay

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

