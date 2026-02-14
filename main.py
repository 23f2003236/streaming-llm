from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stream")
async def stream_llm(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    async def event_generator():
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
            await asyncio.sleep(0.5)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
