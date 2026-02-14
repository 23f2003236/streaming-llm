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
    "Insight 1: Customer satisfaction increased by 18% among users who adopted flexible work schedules. Survey comments indicate improved work-life balance, reduced commuting stress, and higher overall morale contributing to long-term engagement and performance gains across departments. ",
    
    "Insight 2: 62% of respondents reported higher productivity in remote settings compared to office environments. Data shows fewer interruptions, customizable workspaces, and flexible time management significantly improved output metrics and deadline adherence across teams. ",
    
    "Insight 3: Survey data shows that communication tools directly correlate with engagement scores. Teams using structured collaboration platforms reported 30% higher clarity in project goals, better documentation practices, and faster issue resolution rates. ",
    
    "Insight 4: Teams with structured feedback loops showed 25% better retention rates over a 12-month period. Continuous performance reviews, peer feedback, and leadership transparency were cited as major contributors to improved employee satisfaction. ",
    
    "Insight 5: Data suggests that hybrid work models balance collaboration and autonomy effectively. Respondents highlighted that combining in-office collaboration days with remote focus days resulted in stronger team cohesion and measurable performance improvements."
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
