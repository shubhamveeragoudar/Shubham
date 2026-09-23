"""
IBM Granite LLM Client
Wraps IBM watsonx.ai with fallback to a template-based mock for demo when no API key is set.
"""

import os
import re
from typing import Optional


class GraniteClient:
    """Client for IBM Granite models via watsonx.ai, with graceful mock fallback."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-13b-chat-v2")
        self._llm = None
        self._use_mock = not (self.api_key and self.project_id and
                               self.api_key != "your_ibm_watsonx_api_key_here")

    def _get_llm(self):
        if self._llm is not None:
            return self._llm
        if self._use_mock:
            return None
        try:
            from langchain_ibm import WatsonxLLM  # type: ignore
            params = {
                "decoding_method": "greedy",
                "max_new_tokens": 1024,
                "min_new_tokens": 1,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 1,
                "repetition_penalty": 1.1,
            }
            self._llm = WatsonxLLM(
                model_id=self.model_id,
                url=self.url,
                apikey=self.api_key,
                project_id=self.project_id,
                params=params,
            )
            return self._llm
        except Exception as e:
            print(f"[GraniteClient] Failed to initialize WatsonxLLM: {e}. Using mock mode.")
            self._use_mock = True
            return None

    def generate(self, prompt: str, context: str = "") -> str:
        llm = self._get_llm()
        if llm is None:
            return self._mock_generate(prompt, context)
        try:
            full_prompt = f"""<|system|>
You are an expert social media strategist and AI analyst for EcoBottle brand. 
You use real data and brand knowledge to provide specific, actionable recommendations.
Always ground your recommendations in the provided context data.

Brand Context:
{context}
<|user|>
{prompt}
<|assistant|>"""
            return llm.invoke(full_prompt)
        except Exception as e:
            print(f"[GraniteClient] Inference error: {e}. Falling back to mock.")
            return self._mock_generate(prompt, context)

    @property
    def is_mock(self) -> bool:
        return self._use_mock

    def _mock_generate(self, prompt: str, context: str = "") -> str:
        """Intelligent template-based responses for demo mode."""
        p = prompt.lower()

        if any(w in p for w in ["trending", "trend", "hashtag", "popular topic"]):
            return self._mock_trending_response(context)
        elif any(w in p for w in ["sentiment", "negative", "positive", "audience feeling"]):
            return self._mock_sentiment_response(context)
        elif any(w in p for w in ["competitor", "competition", "rival", "compare"]):
            return self._mock_competitor_response(context)
        elif any(w in p for w in ["generate", "create", "write", "caption", "post", "campaign", "content"]):
            return self._mock_content_response(prompt, context)
        elif any(w in p for w in ["when", "post time", "schedule", "best time", "publish"]):
            return self._mock_schedule_response(context)
        elif any(w in p for w in ["engagement", "decreased", "dropped", "increase", "why"]):
            return self._mock_engagement_response(context)
        elif any(w in p for w in ["predict", "forecast", "expect", "will"]):
            return self._mock_prediction_response(context)
        elif any(w in p for w in ["recommend", "suggest", "advice", "strategy"]):
            return self._mock_recommendation_response(context)
        else:
            return self._mock_general_response(prompt, context)

    def _mock_trending_response(self, context: str) -> str:
        return """## 📈 Trending Analysis — IBM Granite AI (Demo Mode)

**Currently Trending for EcoBottle's Niche:**

1. **#ZeroWaste** — ↑ 45.2% growth this week. Sustainability content is surging due to recent UN Climate Report coverage. Estimated 9,870 posts today.

2. **#EcoFriendly** — ↑ 32.4% growth. Consumer brands pivoting to sustainability are driving massive engagement. 14,820 posts and rising.

3. **#PlasticFree** — ↑ 38.9% growth. Gaining momentum ahead of World Oceans Day. Strong positive sentiment (91%).

4. **#HydrationGoals** — ↑ 22.1% growth. Fitness communities on Instagram and TikTok are active. Best window: 6–8 AM weekdays.

5. **#GreenLiving** — ↑ 15.3% steady growth. Evergreen topic with consistent professional audience engagement.

**🔮 Forecast:** The #ClimateAction wave will likely peak this weekend. Recommend posting 3–5 pieces of eco-impact content by Friday to capture this traffic surge.

**⚡ Action:** Create a short Reel showing "1 EcoBottle = 365 less plastic bottles" with #ZeroWaste #PlasticFree #EcoFriendly for maximum reach this week."""

    def _mock_sentiment_response(self, context: str) -> str:
        return """## 💬 Sentiment Analysis Report — IBM Granite AI (Demo Mode)

**Overall Sentiment Distribution (Last 30 Days):**
- 🟢 Positive: **62%** (7,440 mentions)
- ⚪ Neutral: **26%** (3,120 mentions)
- 🔴 Negative: **12%** (1,440 mentions)

**Sentiment Shift:** +4.2% improvement in positive sentiment vs last month ✅

**Top Positive Themes:**
1. *"keeps water cold all day"* — 1,240 mentions, avg ❤️ 84
2. *"love the eco mission"* — 980 mentions, avg ❤️ 67
3. *"great quality, worth the price"* — 720 mentions, avg ❤️ 51
4. *"perfect for outdoor adventures"* — 640 mentions, avg ❤️ 48

**Top Negative Themes:**
1. *"lid leaked"* — 180 mentions (Note: Issue resolved in v2 — recommend proactive response)
2. *"expensive"* — 142 mentions (Counter with lifetime value messaging)
3. *"shipping was slow"* — 98 mentions (Escalate to logistics team)

**Actionable Insight:** The lid-leaking issue is appearing in 1.2% of posts. While low, it's trending slightly. Recommend a proactive Story post acknowledging the v2 improvement to get ahead of the narrative.

**Influencer Alert:** @eco_maven (82K followers) posted a glowing 5-star review yesterday — engage immediately and request permission to repurpose as UGC."""

    def _mock_competitor_response(self, context: str) -> str:
        return """## 🏆 Competitor Intelligence Report — IBM Granite AI (Demo Mode)

**Competitive Landscape Summary:**

| Brand | Followers | Eng. Rate | Growth/Mo |
|-------|-----------|-----------|-----------|
| **EcoBottle** | 156K | **4.8%** | 5.2% |
| HydroFlow | 128K | 4.2% | 3.1% |
| PureWave | 67K | 5.1% | 4.7% |
| GreenSip | 94K | 3.8% | 2.4% |
| AquaLite | 45K | 2.9% | 1.2% |

**Key Findings:**

🔴 **HydroFlow Alert:** Launched a new athlete ambassador program with 3 micro-influencers this week. Their Instagram Stories engagement spiked 28%. EcoBottle should counter with eco-focused micro-influencer partnerships.

🟡 **PureWave Opportunity:** Their "Ocean Cleanup" campaign is resonating strongly (5.1% ER). EcoBottle can compete by launching a data-driven impact campaign ("EcoBottle community saved X tons of plastic").

🟢 **GreenSip Weakness:** Despite similar positioning, GreenSip's engagement is declining (-0.4% this week). Their content is becoming repetitive — an opportunity for EcoBottle to capture their disengaged audience.

**Content Gap EcoBottle Can Own:** None of the competitors are doing **educational carousel posts** about plastic pollution statistics. High-search, low-competition content opportunity.

**Recommended Action:** Launch a "Plastic-Free Pledge" campaign before GreenSip or PureWave do — first-mover advantage in this content space could deliver 30-50% higher organic reach."""

    def _mock_content_response(self, prompt: str, context: str) -> str:
        p = prompt.lower()
        if "linkedin" in p:
            return """## ✍️ LinkedIn Post — IBM Granite AI (Demo Mode)

**Professional Tone | Estimated Engagement: 5.8-6.4% (above your 4.8% avg)**

---

**Draft Post:**

Every year, the average professional contributes 156 single-use plastic bottles to landfills — from desk water, gym sessions, and daily commutes alone.

At EcoBottle, we built a solution: a premium reusable bottle engineered to last a lifetime, eliminating 365 plastic bottles per year while delivering 24-hour cold and 18-hour hot retention that outperforms competitors at half the price-per-use.

The ROI of sustainability isn't just ethical — it's financial. Our Corporate Wellness program has helped 47 organizations reduce plastic procurement costs by an average of $12,000/year while improving employee wellness scores.

The business case for going plastic-free is clear. The only question is when.

🔗 Learn about our Corporate Program → [Link in bio]

**Hashtags:** #Sustainability #CorporateWellness #ESG #PlasticFree #GreenBusiness #EcoBottle

---
*Why this works: Opens with a surprising statistic (pattern interrupt), provides clear value proposition, includes social proof with specific numbers, ends with soft CTA. Ideal for Tuesday 9 AM post.*"""

        elif "instagram" in p:
            return """## 📸 Instagram Content Package — IBM Granite AI (Demo Mode)

**Premium Tone | Estimated Engagement: 6.2-7.1%**

---

**Caption Option 1 (Lifestyle):**
Cold water, warm adventures. ✨

One bottle. Endless possibilities. 
EcoBottle Pro keeps your hydration pure for 24 hours — from morning meetings to mountain summits.

Because the planet deserves your best, and so do you. 🌿

Shop via link in bio.
#EcoBottle #HydrationGoals #EcoFriendly #ZeroWaste #GreenLiving #SustainableLife #PlasticFree #StayHydrated

---

**Caption Option 2 (Impact-focused):**
You just saved another plastic bottle from the ocean. 🌊

That's 187 this year with your EcoBottle. Keep going.
Every refill is a vote for the world you want to live in.

Drop your refill count below 👇
#RefillRevolution #ZeroWaste #EcoWarrior #PlasticFree #EcoBottle #EcoFriendly

---

**Story CTAs:** "How many bottles have YOU saved? 🌿" [Poll: 1-100 / 100-365+]"""

        elif "twitter" in p or "x post" in p:
            return """## 🐦 Twitter/X Posts — IBM Granite AI (Demo Mode)

**Friendly/Humorous Tone | Estimated Engagement: 3.8-4.5%**

---

**Option 1 (Witty):**
Buying a plastic water bottle in 2025 is giving "I still use Internet Explorer" energy 💀

Just saying. #EcoBottle #ZeroWaste

---

**Option 2 (Fact-based):**
Fun fact: Your EcoBottle pays for itself in 73 days of replacing $0.50 plastic bottles.

Math is hitting different today 🧮 #SustainableLiving #EcoFriendly

---

**Option 3 (Community):**
Drop your EcoBottle color below 👇 

I'll start: Midnight Navy. The ONLY correct answer is Midnight Navy.

(Ocean Green and Forest Green are also acceptable, I suppose) 🌊🌿

---

*Post Option 1 at 9 AM, Option 2 at 12 PM, Option 3 at 5 PM for maximum reach.*"""

        else:
            return """## 🎯 Campaign Ideas — IBM Granite AI (Demo Mode)

**Campaign: "1 Bottle. 365 Days. 0 Plastic."**

**Platform Mix:** Instagram (primary) + LinkedIn (B2B) + Twitter (conversation)

**Campaign Concept:** Launch a 30-day UGC challenge where users photograph their EcoBottle in a new location daily. The hashtag #EcoBottle365 becomes both a challenge and a metric of impact.

**Content Ideas:**
1. 📹 Reel: Time-lapse of plastic bottles accumulating vs. one EcoBottle (high virality potential, estimated 180K+ reach)
2. 🎠 Carousel: "Day 1 vs Day 365 of going plastic-free" transformation stories from real customers
3. 📊 Infographic: Annual plastic savings calculator (highly shareable, LinkedIn-optimized)
4. 🤝 Partnership: Collaborate with 5 eco-influencers (50K-200K) for authentic endorsements
5. 🎁 Giveaway: "Tag 3 friends who need to make the switch" (community growth hack)

**Predicted Engagement:** 4.9-6.8% (vs 4.8% avg baseline)
**Estimated Reach:** 480K-1.2M over 30 days
**Conversion Potential:** 2.4-3.1% click-through rate

**Best Launch Day:** Tuesday 8:30 AM (Instagram) + Wednesday 9 AM (LinkedIn)"""

    def _mock_schedule_response(self, context: str) -> str:
        return """## ⏰ Optimal Posting Schedule — IBM Granite AI (Demo Mode)

**This Week's Recommended Schedule (based on your audience data):**

**Monday**
- 📸 Instagram: 8:00 AM — Motivational week-start post with eco impact stat
- 🐦 Twitter: 9:00 AM, 5:00 PM — Engagement bait + reply to trending eco threads

**Tuesday** ⭐ *Best engagement day*
- 📸 Instagram: 8:30 AM — Product feature or UGC repost
- 💼 LinkedIn: 9:00 AM — Thought leadership piece on corporate sustainability
- 🐦 Twitter: 9:00 AM, 12:00 PM, 5:00 PM — Three posts

**Wednesday**
- 📘 Facebook: 11:00 AM — Community question or giveaway
- 💼 LinkedIn: 12:00 PM — Industry stats or case study
- 📸 Instagram: 6:00 PM — Lifestyle content (captures after-work browsing)

**Thursday**
- 📸 Instagram: 11:00 AM — Carousel (educational or product comparison)
- 🐦 Twitter: 9:00 AM — React to trending sustainability news

**Friday**
- 📸 Instagram: 8:00 AM — Weekend vibes / adventure content
- 📘 Facebook: 3:00 PM — Weekend-prep content or flash sale

**Saturday** ⭐ *Highest reach day for Instagram*
- 📸 Instagram: 9:30 AM — Premium lifestyle photography
- 📘 Facebook: 11:00 AM — Community highlights/UGC

**Sunday**
- 📸 Instagram: 7:30 AM — "Week ahead" hydration inspiration
- 🐦 Twitter: 7:00 PM — Light community engagement

**📊 Prediction:** Following this schedule should improve reach by 18-24% vs random posting."""

    def _mock_engagement_response(self, context: str) -> str:
        return """## 📉 Engagement Analysis — IBM Granite AI (Demo Mode)

**Why Engagement Decreased This Week:**

Based on analysis of your 30-day data and brand context, I identified **3 contributing factors:**

**1. Posting Frequency Drop (Primary Cause — 40% impact)**
Your post volume dropped from an average of 14 posts/week to 9 posts/week. The Instagram algorithm rewards consistent posting. Recommendation: Maintain 1 Instagram post/day minimum.

**2. Content Type Shift (Secondary Cause — 35% impact)**
Last week had 4 straight product-only images with no community engagement hooks. Your audience's top-performing content is UGC reposts (5.4% ER) and educational carousels (5.8% ER). Switching back to these formats should recover engagement within 72 hours.

**3. Hashtag Fatigue (Minor Cause — 25% impact)**
The same 8 hashtags were used in 11 consecutive posts. Instagram suppresses reach when hashtag sets are repeated too frequently. Rotate your hashtag pools every 3-4 posts.

**Recovery Plan:**
- Today: Post an engaging question in Stories ("What's your favorite way to stay hydrated? 💧")
- Tomorrow 8 AM: UGC repost from a customer with strong imagery
- Day 3: Educational carousel about plastic pollution statistics
- Expected recovery time: 3-5 days to return to baseline 4.8% engagement rate"""

    def _mock_prediction_response(self, context: str) -> str:
        return """## 🔮 Engagement Prediction — IBM Granite AI (Demo Mode)

**⚠️ Note: Predictions are estimates based on historical patterns, not guarantees.**

**Next 7-Day Engagement Forecast:**

| Day | Predicted Posts | Predicted Engagement | Confidence |
|-----|----------------|---------------------|------------|
| Mon | 3 | 4,200-4,800 | 78% |
| Tue | 4 | 5,100-5,900 | 82% |
| Wed | 3 | 4,400-5,000 | 75% |
| Thu | 3 | 4,600-5,200 | 79% |
| Fri | 3 | 4,800-5,600 | 77% |
| Sat | 2 | 5,200-6,100 | 71% |
| Sun | 2 | 4,100-4,700 | 73% |

**Weekly Total Prediction:** 32,400-37,300 engagements

**Campaign Comparison (if you launch the eco-campaign this week):**
- Without campaign: ~34,800 engagements (baseline)
- With campaign: ~52,000-64,000 engagements (+49-84%)

**Factors that could outperform predictions:**
- Viral Reel (probability: 12% any given week)
- Trending hashtag alignment (probability: 34%)
- Influencer organic mention (probability: 8%)

**Highest potential post format this week:** Educational carousel about plastic statistics, posted Tuesday 8 AM. Predicted ER: 6.4-7.8%"""

    def _mock_recommendation_response(self, context: str) -> str:
        return """## 🎯 Strategic Recommendations — IBM Granite AI (Demo Mode)

Based on your current performance data, brand context, and market trends, here are your top 5 action items:

**Priority 1: Launch Impact Campaign This Week** 🔥
Your audience responds strongly to quantified eco-impact. Create a "EcoBottle Community has saved X plastic bottles" campaign. Use real cumulative data. Expected engagement lift: +22-35%.

**Priority 2: Activate Micro-Influencer Program**
PureWave's engagement advantage (5.1% vs your 4.8%) comes from authentic micro-influencer content. Identify 8-12 influencers in the 15K-80K range with high eco-engagement rates. Budget: $3,000-5,000/month for significantly better ROI than paid ads.

**Priority 3: Respond to Lid-Leak Mentions**
180 organic mentions of the lid issue are live. A proactive Story post ("We heard you — here's what we improved") can convert negative sentiment to brand loyalty. Studies show public issue-resolution increases NPS by avg 14 points.

**Priority 4: Capture LinkedIn B2B Opportunity**
The Earth Day campaign proved LinkedIn's B2B potential (14 partnerships). Post 3 thought leadership pieces this month targeting sustainability managers at 500+ employee companies. Low effort, high-value pipeline.

**Priority 5: Hashtag Refresh**
Rotate in these emerging hashtags now (before they peak): #SustainableOffice #EcoMinimalist #PlasticFreeJuly #GreenInnovation. First-mover advantage in these sets could deliver 20-40% higher organic reach."""

    def _mock_general_response(self, prompt: str, context: str) -> str:
        return f"""## 🤖 AI Analysis — IBM Granite AI (Demo Mode)

I've analyzed your query: *"{prompt[:100]}..."*

Based on EcoBottle's brand data and social media performance:

**Key Insights from Your Data:**
- Your current engagement rate of 4.8% is above the industry average of 3.2% — solid foundation
- Instagram is your highest-engagement platform, followed by LinkedIn
- Positive sentiment is at 62% — healthy but room to grow to 70%+ target
- Trending opportunities: #ZeroWaste and #PlasticFree are both growing 30-45% this week

**Recommended Next Steps:**
1. Create platform-specific content aligned with peak posting times
2. Leverage trending eco-sustainability hashtags while they're surging
3. Address the negative sentiment themes with proactive content
4. Consider a competitor gap analysis to identify untapped content opportunities

**IBM Granite Model Status:** Running in demo mode. Configure your `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` in the `.env` file to enable full IBM Granite 13B model inference with more detailed, contextual responses.

*All recommendations are based on analysis of your brand context and social media data.*"""


# Singleton
_client = None

def get_granite_client() -> GraniteClient:
    global _client
    if _client is None:
        _client = GraniteClient()
    return _client
