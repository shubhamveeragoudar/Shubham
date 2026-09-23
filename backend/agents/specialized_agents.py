"""
Specialized AI Agents
Each agent handles a distinct domain: Trend, Sentiment, Competitor, Content, Recommendation.
"""

import json
import random
from typing import Optional
from agents.granite_client import get_granite_client
from rag.knowledge_base import retrieve_context


class TrendAgent:
    """Detects emerging hashtags, trending topics, and forecasts viral potential."""

    def analyze(self, data: dict) -> dict:
        client = get_granite_client()
        hashtags = data.get("trending_hashtags", [])
        top_tags = [h["hashtag"] for h in hashtags[:5]]

        context = retrieve_context("trending hashtags social media strategy")
        prompt = f"""Analyze the following trending hashtags for EcoBottle brand and provide:
1. Which trends to capitalize on immediately
2. Predicted 7-day trajectory for each
3. Content ideas to leverage each trend
4. Risk assessment (could any trend become controversial?)

Trending data: {json.dumps(hashtags[:8], indent=2)}

Provide a structured, actionable analysis."""

        analysis = client.generate(prompt, context)
        emerging = [h for h in hashtags if h.get("growth", 0) > 25]

        return {
            "agent": "TrendAgent",
            "powered_by": "IBM Granite" + (" (Demo)" if client.is_mock else ""),
            "top_trending": hashtags[:5],
            "emerging_fast": emerging,
            "forecast": [
                {
                    "hashtag": h["hashtag"],
                    "current_count": h["count"],
                    "predicted_7d": int(h["count"] * (1 + h["growth"] / 100)),
                    "momentum": "🔥 Surging" if h["growth"] > 30 else "📈 Growing" if h["growth"] > 15 else "➡️ Stable",
                    "action": "Post within 24h" if h["growth"] > 30 else "Include in next 3 posts",
                }
                for h in hashtags[:6]
            ],
            "ai_analysis": analysis,
            "recommended_hashtags": top_tags[:5],
        }


class SentimentAgent:
    """Analyzes audience sentiment from comments and posts."""

    def analyze(self, data: dict) -> dict:
        client = get_granite_client()
        comments = data.get("comments", [])
        breakdown = data.get("sentiment_breakdown", {"positive": 62, "neutral": 26, "negative": 12})

        neg_comments = [c for c in comments if c["sentiment"] == "negative"][:5]
        pos_comments = [c for c in comments if c["sentiment"] == "positive"][:5]

        context = retrieve_context("audience sentiment negative comments brand response crisis")
        prompt = f"""Analyze sentiment data for EcoBottle's social media presence:

Sentiment breakdown: {json.dumps(breakdown)}
Sample negative comments: {json.dumps([c['text'] for c in neg_comments])}
Sample positive comments: {json.dumps([c['text'] for c in pos_comments])}

Provide:
1. Overall sentiment health assessment
2. Root causes of negative sentiment
3. Key positive themes to amplify
4. Specific response strategies for top negative themes
5. Sentiment change predictions for next 2 weeks"""

        analysis = client.generate(prompt, context)

        sentiment_score = (
            breakdown.get("positive", 0) * 1.0 +
            breakdown.get("neutral", 0) * 0.5 -
            breakdown.get("negative", 0) * 1.0
        ) / 100

        top_neg_themes = [
            {"theme": "Lid leaking", "count": 180, "urgency": "High", "action": "Proactive Story response"},
            {"theme": "Price concerns", "count": 142, "urgency": "Medium", "action": "Lifetime value content"},
            {"theme": "Shipping delays", "count": 98, "urgency": "High", "action": "Escalate + DM response"},
        ]
        top_pos_themes = [
            {"theme": "Keeps water cold", "count": 1240, "amplify": "Use as social proof UGC"},
            {"theme": "Love the eco mission", "count": 980, "amplify": "Feature in brand story content"},
            {"theme": "Great quality", "count": 720, "amplify": "Include in product pages"},
        ]

        return {
            "agent": "SentimentAgent",
            "powered_by": "IBM Granite" + (" (Demo)" if client.is_mock else ""),
            "sentiment_breakdown": breakdown,
            "sentiment_score": round(sentiment_score, 3),
            "sentiment_health": "Good" if sentiment_score > 0.4 else "Fair" if sentiment_score > 0.2 else "Needs Attention",
            "top_negative_themes": top_neg_themes,
            "top_positive_themes": top_pos_themes,
            "trend_direction": "+4.2% positive this month",
            "ai_analysis": analysis,
        }


class CompetitorAgent:
    """Monitors competitors, compares engagement, identifies content gaps."""

    def analyze(self, data: dict) -> dict:
        client = get_granite_client()
        competitors = data.get("competitors", [])
        brand_info = data.get("brand_info", {})

        context = retrieve_context("competitor analysis social media strategy content gaps")
        prompt = f"""Conduct a competitive intelligence analysis for EcoBottle against these competitors:

EcoBottle stats: {json.dumps(brand_info)}
Competitors: {json.dumps(competitors, indent=2)}

Provide:
1. Competitive positioning summary
2. EcoBottle's key advantages and vulnerabilities
3. Top 3 immediate competitive threats
4. Content gaps EcoBottle can exploit
5. Specific counter-strategies for top competitors"""

        analysis = client.generate(prompt, context)

        engagement_comparison = [
            {"brand": brand_info.get("name", "EcoBottle"), "engagement_rate": brand_info.get("avg_engagement_rate", 4.8), "followers": brand_info.get("followers", 156000), "is_own": True}
        ] + [
            {"brand": c["name"], "engagement_rate": c["avg_engagement_rate"], "followers": c["followers"], "is_own": False}
            for c in competitors
        ]

        return {
            "agent": "CompetitorAgent",
            "powered_by": "IBM Granite" + (" (Demo)" if client.is_mock else ""),
            "competitors": competitors,
            "engagement_comparison": engagement_comparison,
            "market_position": "2nd by followers, 2nd by engagement rate",
            "key_opportunities": [
                "Educational carousel content (no competitor doing this)",
                "Quantified impact campaigns ('X bottles saved by community')",
                "B2B/corporate sustainability positioning",
                "Micro-influencer partnerships (competitors underinvesting here)",
            ],
            "threats": [
                {"competitor": "HydroFlow", "threat": "New athlete ambassador program launched", "urgency": "High"},
                {"competitor": "PureWave", "threat": "Ocean Cleanup campaign gaining traction", "urgency": "Medium"},
            ],
            "ai_analysis": analysis,
        }


class ContentAgent:
    """Generates social media content: captions, posts, hashtags, campaigns."""

    def generate(self, request: dict) -> dict:
        client = get_granite_client()
        platform = request.get("platform", "instagram")
        content_type = request.get("content_type", "post")
        brand_tone = request.get("brand_tone", "friendly")
        topic = request.get("topic", "eco-friendly water bottle")
        image_desc = request.get("image_description", "")

        context = retrieve_context(f"content generation {platform} {brand_tone} tone {topic} hashtags")

        image_context = f"\n\nImage description provided: {image_desc}\nGenerate caption that directly relates to this image." if image_desc else ""

        prompt = f"""Generate high-quality social media content for EcoBottle brand:

Platform: {platform}
Content Type: {content_type}
Brand Tone: {brand_tone}
Topic/Product: {topic}{image_context}

Create:
1. 2-3 complete post variations optimized for {platform}
2. Platform-appropriate hashtag set (with tier labels: brand/community/discovery)
3. Optimal posting time for this content
4. Predicted engagement estimate
5. A/B test recommendation (which variation to post first and why)

Use the brand context and tone guidelines to ensure brand consistency."""

        generated_content = client.generate(prompt, context)

        hashtag_sets = {
            "instagram": ["#EcoBottle", "#EcoFriendly", "#ZeroWaste", "#HydrationGoals", "#PlasticFree", "#GreenLiving", "#SustainableLife", "#EcoWarrior", "#ReusableBottle"],
            "twitter":   ["#EcoFriendly", "#ZeroWaste", "#Sustainability"],
            "linkedin":  ["#Sustainability", "#ESG", "#GreenBusiness", "#EcoBottle", "#CorporateWellness"],
            "facebook":  ["#EcoBottle", "#EcoFriendly", "#GreenLiving", "#PlasticFree", "#ZeroWaste"],
        }

        return {
            "agent": "ContentAgent",
            "powered_by": "IBM Granite" + (" (Demo)" if client.is_mock else ""),
            "platform": platform,
            "brand_tone": brand_tone,
            "topic": topic,
            "generated_content": generated_content,
            "recommended_hashtags": hashtag_sets.get(platform, hashtag_sets["instagram"]),
            "optimal_post_time": self._get_optimal_time(platform),
            "predicted_engagement": f"{random.uniform(4.2, 7.1):.1f}%",
        }

    def _get_optimal_time(self, platform: str) -> str:
        times = {
            "instagram": "Tuesday 8:30 AM or Thursday 11 AM",
            "twitter":   "Tuesday-Thursday at 9 AM, 12 PM, or 5 PM",
            "linkedin":  "Tuesday or Wednesday 9 AM",
            "facebook":  "Wednesday 11 AM or Saturday 10 AM",
        }
        return times.get(platform, "Tuesday 9 AM")


class RecommendationAgent:
    """Synthesizes all agent outputs to produce actionable recommendations."""

    def recommend(self, all_data: dict) -> dict:
        client = get_granite_client()
        trend_data = all_data.get("trends", {})
        sentiment_data = all_data.get("sentiment", {})
        competitor_data = all_data.get("competitors", {})
        brand_info = all_data.get("brand_info", {})
        engagement_series = all_data.get("engagement_timeseries", [])

        recent_engagement = [e["engagement"] for e in engagement_series[-7:]] if engagement_series else []
        trend = "increasing" if (recent_engagement and recent_engagement[-1] > recent_engagement[0]) else "decreasing"

        context = retrieve_context("posting schedule recommendations engagement optimization strategy")
        prompt = f"""As EcoBottle's AI social media strategist, provide comprehensive recommendations:

Brand performance: Engagement trend is {trend} over last 7 days.
Follower count: {brand_info.get('followers', 156000)}
Current engagement rate: {brand_info.get('avg_engagement_rate', 4.8)}%
Sentiment health: {sentiment_data.get('sentiment_health', 'Good')}
Top trending hashtag: {trend_data.get('top_trending', [{}])[0].get('hashtag', '#EcoFriendly') if trend_data.get('top_trending') else '#EcoFriendly'}

Provide:
1. Top 5 priority actions for this week (ranked by impact)
2. Optimal content calendar recommendations
3. Platform-specific strategy adjustments
4. Expected outcomes if recommendations are followed
5. 30-day growth forecast"""

        recommendations = client.generate(prompt, context)

        return {
            "agent": "RecommendationAgent",
            "powered_by": "IBM Granite" + (" (Demo)" if client.is_mock else ""),
            "priority_actions": [
                {
                    "priority": 1,
                    "action": "Launch #ZeroWaste impact campaign",
                    "platform": "Instagram + Twitter",
                    "expected_impact": "+22-35% engagement",
                    "timeline": "This week",
                    "effort": "Medium",
                },
                {
                    "priority": 2,
                    "action": "Address lid-leak mentions proactively",
                    "platform": "Instagram Stories",
                    "expected_impact": "+8% positive sentiment shift",
                    "timeline": "Within 48 hours",
                    "effort": "Low",
                },
                {
                    "priority": 3,
                    "action": "Publish LinkedIn thought leadership piece",
                    "platform": "LinkedIn",
                    "expected_impact": "2-4 B2B leads",
                    "timeline": "Tuesday 9 AM",
                    "effort": "Medium",
                },
                {
                    "priority": 4,
                    "action": "Activate micro-influencer outreach (8-12 creators)",
                    "platform": "All platforms",
                    "expected_impact": "+15-25% reach",
                    "timeline": "This month",
                    "effort": "High",
                },
                {
                    "priority": 5,
                    "action": "Refresh hashtag rotation strategy",
                    "platform": "Instagram",
                    "expected_impact": "+10-18% algorithmic reach",
                    "timeline": "Immediate",
                    "effort": "Low",
                },
            ],
            "posting_schedule": {
                "instagram": "Daily at 8:30 AM (weekdays), 9:30 AM (weekends)",
                "twitter": "3-5x daily at 9 AM, 12 PM, 5 PM",
                "linkedin": "1x weekday, Tuesday-Wednesday preferred",
                "facebook": "4-5x/week, Wednesday 11 AM + Saturday 10 AM peak",
            },
            "predicted_monthly_growth": "+5-8% followers, +12-18% engagement",
            "ai_recommendations": recommendations,
        }
