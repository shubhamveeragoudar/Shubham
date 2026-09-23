"""
Agentic AI Social Media Agent — FastAPI Backend
Powered by IBM Granite via watsonx.ai + LangChain + ChromaDB RAG
"""

import os
import base64
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from data.mock_data import MOCK_DATA
from agents.granite_client import get_granite_client
from agents.specialized_agents import (
    TrendAgent, SentimentAgent, CompetitorAgent,
    ContentAgent, RecommendationAgent
)
from rag.knowledge_base import retrieve_context


# ─── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """No blocking startup — RAG initialises lazily on first request."""
    print("[Startup] SocialPulse AI backend ready.")
    yield


# ─── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Agentic AI Social Media Agent",
    description="IBM Granite-powered social media intelligence platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000"), "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    conversation_history: list[dict] = []

class ContentRequest(BaseModel):
    platform: str = "instagram"
    content_type: str = "post"
    brand_tone: str = "friendly"
    topic: str = "eco-friendly water bottle"
    image_description: Optional[str] = None

class AgentRunRequest(BaseModel):
    agent: str  # trend | sentiment | competitor | content | recommendation | all


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    client = get_granite_client()
    return {
        "status": "healthy",
        "granite_mode": "demo_mock" if client.is_mock else "ibm_watsonx_ai",
        "granite_model": os.getenv("GRANITE_MODEL_ID", "ibm/granite-13b-chat-v2"),
        "rag_status": "active",
        "data_source": "mock_dataset",
    }


# ─── Dashboard Data ────────────────────────────────────────────────────────────

@app.get("/api/dashboard")
async def get_dashboard():
    """Return all data needed for the main analytics dashboard."""
    brand = MOCK_DATA["brand_info"]
    platform_breakdown = MOCK_DATA["platform_breakdown"]
    total_engagement = sum(p["engagement"] for p in platform_breakdown)
    total_posts = sum(p["posts"] for p in platform_breakdown)

    return {
        "brand_info": brand,
        "metrics": {
            "total_posts": total_posts,
            "total_engagement": total_engagement,
            "engagement_rate": brand["avg_engagement_rate"],
            "follower_count": brand["followers"],
            "monthly_growth": brand["monthly_growth"],
            "avg_reach_per_post": 28400,
            "total_impressions": 4_820_000,
        },
        "sentiment_breakdown": MOCK_DATA["sentiment_breakdown"],
        "platform_breakdown": platform_breakdown,
        "engagement_timeseries": MOCK_DATA["engagement_timeseries"],
        "trending_hashtags": MOCK_DATA["trending_hashtags"][:8],
        "top_posts": sorted(
            [p for p in MOCK_DATA["posts"] if p["is_own_brand"]],
            key=lambda x: x["engagement_rate"],
            reverse=True
        )[:5],
        "competitor_overview": [
            {
                "name": c["name"],
                "followers": c["followers"],
                "engagement_rate": c["avg_engagement_rate"],
                "monthly_growth": c["monthly_growth"],
            }
            for c in MOCK_DATA["competitors"]
        ],
    }


# ─── Posts Feed ────────────────────────────────────────────────────────────────

@app.get("/api/posts")
async def get_posts(
    platform: Optional[str] = None,
    brand: Optional[str] = None,
    sentiment: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    posts = MOCK_DATA["posts"]
    if platform:
        posts = [p for p in posts if p["platform"] == platform.lower()]
    if brand:
        posts = [p for p in posts if p["brand"].lower() == brand.lower()]
    if sentiment:
        posts = [p for p in posts if p["sentiment"] == sentiment.lower()]

    total = len(posts)
    posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)
    return {
        "total": total,
        "posts": posts[offset: offset + limit],
        "limit": limit,
        "offset": offset,
    }


# ─── Trends ────────────────────────────────────────────────────────────────────

@app.get("/api/trends")
async def get_trends():
    agent = TrendAgent()
    return agent.analyze(MOCK_DATA)


# ─── Sentiment ────────────────────────────────────────────────────────────────

@app.get("/api/sentiment")
async def get_sentiment():
    agent = SentimentAgent()
    return agent.analyze(MOCK_DATA)


# ─── Competitors ──────────────────────────────────────────────────────────────

@app.get("/api/competitors")
async def get_competitors():
    agent = CompetitorAgent()
    return agent.analyze(MOCK_DATA)


# ─── Content Generation ───────────────────────────────────────────────────────

@app.post("/api/generate-content")
async def generate_content(request: ContentRequest):
    agent = ContentAgent()
    return agent.generate(request.model_dump())


@app.post("/api/generate-content-with-image")
async def generate_content_with_image(
    platform: str = Form("instagram"),
    content_type: str = Form("post"),
    brand_tone: str = Form("friendly"),
    topic: str = Form("product showcase"),
    image: Optional[UploadFile] = File(None),
):
    image_description = ""
    if image and image.filename:
        contents = await image.read()
        b64 = base64.b64encode(contents).decode("utf-8")
        image_description = f"User uploaded image ({image.filename}, {len(contents)//1024}KB). Generate content inspired by a product lifestyle photo."

    agent = ContentAgent()
    return agent.generate({
        "platform": platform,
        "content_type": content_type,
        "brand_tone": brand_tone,
        "topic": topic,
        "image_description": image_description,
    })


# ─── Recommendations ──────────────────────────────────────────────────────────

@app.get("/api/recommendations")
async def get_recommendations():
    sentiment_agent = SentimentAgent()
    trend_agent = TrendAgent()
    competitor_agent = CompetitorAgent()
    rec_agent = RecommendationAgent()

    all_data = {
        **MOCK_DATA,
        "trends": trend_agent.analyze(MOCK_DATA),
        "sentiment": sentiment_agent.analyze(MOCK_DATA),
        "competitors": competitor_agent.analyze(MOCK_DATA),
    }
    return rec_agent.recommend(all_data)


# ─── AI Chat ──────────────────────────────────────────────────────────────────

@app.post("/api/chat")
async def chat(request: ChatRequest):
    client = get_granite_client()
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # RAG retrieval
    context = retrieve_context(message, k=4)

    # Append relevant data summaries to context
    brand = MOCK_DATA["brand_info"]
    sentiment = MOCK_DATA["sentiment_breakdown"]
    hashtags = [h["hashtag"] for h in MOCK_DATA["trending_hashtags"][:5]]

    data_summary = f"""
Current Brand Data Summary:
- Followers: {brand['followers']:,}
- Engagement Rate: {brand['avg_engagement_rate']}%
- Monthly Growth: {brand['monthly_growth']}%
- Sentiment: {sentiment['positive']}% positive, {sentiment['neutral']}% neutral, {sentiment['negative']}% negative
- Top Trending Hashtags: {', '.join(hashtags)}
"""

    full_context = context + "\n" + data_summary

    # Route to specialized agent if keyword matches
    msg_lower = message.lower()
    specialized_result = None

    if any(w in msg_lower for w in ["trend", "trending", "hashtag", "viral"]):
        agent = TrendAgent()
        specialized_result = agent.analyze(MOCK_DATA)
    elif any(w in msg_lower for w in ["sentiment", "negative", "positive", "audience feel"]):
        agent = SentimentAgent()
        specialized_result = agent.analyze(MOCK_DATA)
    elif any(w in msg_lower for w in ["competitor", "competition", "rival", "hydroflow", "greensip"]):
        agent = CompetitorAgent()
        specialized_result = agent.analyze(MOCK_DATA)
    elif any(w in msg_lower for w in ["recommend", "suggest", "strategy", "priority"]):
        sentiment_agent = SentimentAgent()
        trend_agent = TrendAgent()
        rec_agent = RecommendationAgent()
        combined = {**MOCK_DATA, "trends": trend_agent.analyze(MOCK_DATA), "sentiment": sentiment_agent.analyze(MOCK_DATA), "competitors": []}
        specialized_result = rec_agent.recommend(combined)

    # Generate AI response
    response_text = client.generate(message, full_context)

    return {
        "response": response_text,
        "powered_by": "IBM Granite" + (" (Demo Mode)" if client.is_mock else " via watsonx.ai"),
        "rag_sources": ["brand_guidelines", "campaign_history", "audience_data", "competitor_intel"],
        "agent_triggered": specialized_result.get("agent") if specialized_result else None,
        "agent_data": specialized_result,
    }


# ─── Full Agentic Run ─────────────────────────────────────────────────────────

@app.post("/api/agents/run")
async def run_agents(request: AgentRunRequest):
    """Run one or all specialized agents and return combined results."""
    results = {}

    if request.agent in ("trend", "all"):
        results["trend"] = TrendAgent().analyze(MOCK_DATA)

    if request.agent in ("sentiment", "all"):
        results["sentiment"] = SentimentAgent().analyze(MOCK_DATA)

    if request.agent in ("competitor", "all"):
        results["competitor"] = CompetitorAgent().analyze(MOCK_DATA)

    if request.agent in ("recommendation", "all"):
        combined = {**MOCK_DATA, **results}
        results["recommendation"] = RecommendationAgent().recommend(combined)

    if not results:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {request.agent}. Use trend|sentiment|competitor|recommendation|all")

    return {"agents_run": list(results.keys()), "results": results}


# ─── Campaigns ────────────────────────────────────────────────────────────────

@app.get("/api/campaigns")
async def get_campaigns():
    return {
        "campaigns": [
            {
                "id": 1, "name": "Refill Revolution", "status": "completed",
                "platform": ["instagram", "twitter"], "start_date": "2024-01-15", "end_date": "2024-02-15",
                "impressions": 2_400_000, "engagement_rate": 4.8, "new_followers": 8900,
                "posts_generated": 48, "sentiment_score": 0.78, "revenue_attributed": 12400,
            },
            {
                "id": 2, "name": "30-Day Hydration Challenge", "status": "completed",
                "platform": ["instagram", "twitter", "facebook", "linkedin"], "start_date": "2024-03-01", "end_date": "2024-03-31",
                "impressions": 8_900_000, "engagement_rate": 6.2, "new_followers": 25000,
                "posts_generated": 124, "sentiment_score": 0.85, "revenue_attributed": 28700,
            },
            {
                "id": 3, "name": "Earth Day Pledge", "status": "completed",
                "platform": ["linkedin", "instagram"], "start_date": "2024-04-15", "end_date": "2024-04-30",
                "impressions": 1_800_000, "engagement_rate": 6.2, "new_followers": 4200,
                "posts_generated": 22, "sentiment_score": 0.91, "revenue_attributed": 8900,
            },
            {
                "id": 4, "name": "Back to School", "status": "completed",
                "platform": ["instagram", "facebook"], "start_date": "2024-08-01", "end_date": "2024-08-31",
                "impressions": 3_200_000, "engagement_rate": 5.1, "new_followers": 11200,
                "posts_generated": 67, "sentiment_score": 0.74, "revenue_attributed": 94000,
            },
            {
                "id": 5, "name": "EcoBottle365 Challenge", "status": "active",
                "platform": ["instagram", "twitter", "tiktok"], "start_date": "2024-09-01", "end_date": None,
                "impressions": 1_240_000, "engagement_rate": 5.8, "new_followers": 6800,
                "posts_generated": 34, "sentiment_score": 0.82, "revenue_attributed": 18400,
            },
        ]
    }


# ─── Analytics ────────────────────────────────────────────────────────────────

@app.get("/api/analytics/engagement-timeseries")
async def get_engagement_timeseries(days: int = 30):
    return {"data": MOCK_DATA["engagement_timeseries"][-days:]}


@app.get("/api/analytics/top-posts")
async def get_top_posts(limit: int = 10, is_own: bool = True):
    posts = [p for p in MOCK_DATA["posts"] if p["is_own_brand"] == is_own]
    sorted_posts = sorted(posts, key=lambda x: x["likes"] + x["comments"] + x["shares"], reverse=True)
    return {"posts": sorted_posts[:limit]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
