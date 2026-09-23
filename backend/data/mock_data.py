"""
Mock Social Media Dataset
Realistic sample data for demonstration purposes.
"""

import random
from datetime import datetime, timedelta

def generate_posts():
    platforms = ["twitter", "instagram", "linkedin", "facebook"]
    brands = ["EcoBottle", "HydroFlow", "GreenSip", "PureWave", "AquaLite"]
    own_brand = "EcoBottle"
    competitors = ["HydroFlow", "GreenSip", "PureWave", "AquaLite"]

    hashtag_pool = [
        "#EcoFriendly", "#Sustainability", "#HydrationGoals", "#GreenLiving",
        "#ZeroWaste", "#WaterBottle", "#EcoWarrior", "#CleanWater",
        "#PlasticFree", "#EarthDay", "#GreenBrand", "#HydroLife",
        "#ReusableBottle", "#EcoConscious", "#WaterIsLife", "#StayHydrated",
        "#SustainableLife", "#EcoDesign", "#GreenProduct", "#NatureLovers"
    ]

    templates_by_platform = {
        "twitter": [
            "Just switched to {brand}'s eco bottle! {hashtags} 🌿",
            "Loving my {brand} bottle - keeps water cold for 24hrs! {hashtags}",
            "{brand} just dropped their new collection! Pre-order now 🌊 {hashtags}",
            "Why is everyone talking about {brand}? {hashtags} Let me explain...",
            "My hydration routine just got an upgrade thanks to {brand} {hashtags}",
            "The {brand} bottle pays for itself in 2 months vs buying plastic {hashtags}",
            "Can we talk about how gorgeous the new {brand} designs are? {hashtags}",
        ],
        "instagram": [
            "Morning hike essentials: my {brand} bottle ✨ {hashtags}",
            "Refill, reuse, repeat 💧 Proud to carry my {brand} {hashtags}",
            "Small changes, big impact. My {brand} saved 365 plastic bottles this year {hashtags}",
            "Obsessed with this color! New {brand} drop is 🔥 {hashtags}",
            "Fueling adventures with {brand} 🏔️ Because the planet matters {hashtags}",
        ],
        "linkedin": [
            "{brand} is leading the charge in sustainable consumer goods. Here's what businesses can learn from their approach to eco-design. {hashtags}",
            "Proud to feature {brand} in our sustainability spotlight. Companies like this are changing the market. {hashtags}",
            "The business case for sustainability: {brand} grew 40% YoY while reducing plastic waste by 2M units. {hashtags}",
            "ESG in action: How {brand} built a loyal community around environmental values. {hashtags}",
        ],
        "facebook": [
            "Just picked up the new {brand} limited edition bottle! Who else is obsessed? 💚 {hashtags}",
            "Sharing my honest review of {brand} after 6 months of daily use. Spoiler: I love it! {hashtags}",
            "{brand} giveaway!! Comment below to win a free bottle and help spread the eco message 🌎 {hashtags}",
            "Our family made the switch to {brand} and we've never looked back! {hashtags}",
        ]
    }

    posts = []
    base_date = datetime.now()

    post_id = 1
    for days_ago in range(30, 0, -1):
        post_date = base_date - timedelta(days=days_ago)
        daily_count = random.randint(8, 20)

        for _ in range(daily_count):
            platform = random.choice(platforms)
            is_own = random.random() > 0.45
            brand = own_brand if is_own else random.choice(competitors)
            hashtags = " ".join(random.sample(hashtag_pool, random.randint(2, 5)))
            template = random.choice(templates_by_platform[platform])
            content = template.format(brand=brand, hashtags=hashtags)

            likes = random.randint(10, 2500) if is_own else random.randint(5, 3200)
            comments = int(likes * random.uniform(0.03, 0.18))
            shares = int(likes * random.uniform(0.01, 0.12))
            views = likes * random.randint(4, 25)
            engagement_rate = round((likes + comments + shares) / max(views, 1) * 100, 2)

            sentiments = ["positive", "neutral", "negative"]
            sentiment_weights = [0.60, 0.28, 0.12]
            sentiment = random.choices(sentiments, weights=sentiment_weights)[0]

            post_hashtags = [h for h in hashtag_pool if h in content]

            posts.append({
                "id": post_id,
                "platform": platform,
                "brand": brand,
                "is_own_brand": is_own,
                "content": content,
                "hashtags": post_hashtags,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "views": views,
                "engagement_rate": engagement_rate,
                "sentiment": sentiment,
                "timestamp": post_date.isoformat(),
                "author": f"@user{random.randint(100, 9999)}",
                "reach": views * random.randint(1, 3),
            })
            post_id += 1

    return posts


def generate_comments():
    positive_comments = [
        "Absolutely love this product! Changed my hydration game completely.",
        "Best purchase I've made this year. So eco-friendly and stylish!",
        "Already recommended to all my friends. Worth every penny.",
        "The quality is outstanding. Keeps my water cold all day.",
        "So happy I made the switch to sustainable. This brand gets it!",
        "Incredible design and even better mission. 10/10 recommend.",
        "My morning routine is incomplete without my eco bottle now!",
    ]
    negative_comments = [
        "The lid leaked after 2 weeks. Very disappointed.",
        "Overpriced for what you get. Found better options elsewhere.",
        "Customer service was unhelpful when my bottle cracked.",
        "The insulation stopped working after a month. Not worth it.",
        "Too heavy to carry around. Wish they made a lighter version.",
    ]
    neutral_comments = [
        "Just received my order. Will update after I try it.",
        "How long does shipping usually take?",
        "Do these come in more colors?",
        "Is this dishwasher safe?",
        "Comparing this with another brand before I decide.",
        "Seen this advertised a lot lately.",
    ]

    all_comments = []
    comment_id = 1
    base_date = datetime.now()

    for days_ago in range(30, 0, -1):
        comment_date = base_date - timedelta(days=days_ago)
        for _ in range(random.randint(15, 40)):
            r = random.random()
            if r < 0.60:
                text = random.choice(positive_comments)
                sentiment = "positive"
            elif r < 0.88:
                text = random.choice(neutral_comments)
                sentiment = "neutral"
            else:
                text = random.choice(negative_comments)
                sentiment = "negative"

            all_comments.append({
                "id": comment_id,
                "text": text,
                "sentiment": sentiment,
                "timestamp": comment_date.isoformat(),
                "likes": random.randint(0, 120),
                "platform": random.choice(["twitter", "instagram", "facebook", "linkedin"]),
            })
            comment_id += 1

    return all_comments


def generate_trending_hashtags():
    return [
        {"hashtag": "#EcoFriendly", "count": 14820, "growth": 32.4, "sentiment": "positive"},
        {"hashtag": "#Sustainability", "count": 12340, "growth": 18.7, "sentiment": "positive"},
        {"hashtag": "#ZeroWaste", "count": 9870, "growth": 45.2, "sentiment": "positive"},
        {"hashtag": "#HydrationGoals", "count": 7650, "growth": 22.1, "sentiment": "positive"},
        {"hashtag": "#PlasticFree", "count": 6540, "growth": 38.9, "sentiment": "positive"},
        {"hashtag": "#GreenLiving", "count": 5430, "growth": 15.3, "sentiment": "positive"},
        {"hashtag": "#WaterBottle", "count": 4890, "growth": 8.6, "sentiment": "neutral"},
        {"hashtag": "#EcoWarrior", "count": 4210, "growth": 28.4, "sentiment": "positive"},
        {"hashtag": "#ReusableBottle", "count": 3870, "growth": 19.2, "sentiment": "positive"},
        {"hashtag": "#CleanWater", "count": 3540, "growth": 12.8, "sentiment": "positive"},
    ]


def generate_competitor_data():
    return [
        {
            "name": "HydroFlow",
            "followers": 128000,
            "avg_engagement_rate": 4.2,
            "posts_per_week": 12,
            "top_hashtags": ["#HydroLife", "#StayHydrated", "#WaterIsLife"],
            "sentiment_score": 0.72,
            "recent_campaigns": ["Summer Hydration", "Trail Ready"],
            "monthly_growth": 3.1,
        },
        {
            "name": "GreenSip",
            "followers": 94000,
            "avg_engagement_rate": 3.8,
            "posts_per_week": 9,
            "top_hashtags": ["#GreenSip", "#EcoDesign", "#SustainableLife"],
            "sentiment_score": 0.68,
            "recent_campaigns": ["Eco Warriors", "Green Friday"],
            "monthly_growth": 2.4,
        },
        {
            "name": "PureWave",
            "followers": 67000,
            "avg_engagement_rate": 5.1,
            "posts_per_week": 7,
            "top_hashtags": ["#PureWave", "#NatureLovers", "#CleanLiving"],
            "sentiment_score": 0.81,
            "recent_campaigns": ["Ocean Cleanup", "Pure Beginnings"],
            "monthly_growth": 4.7,
        },
        {
            "name": "AquaLite",
            "followers": 45000,
            "avg_engagement_rate": 2.9,
            "posts_per_week": 5,
            "top_hashtags": ["#AquaLite", "#LightWeight", "#EcoConscious"],
            "sentiment_score": 0.61,
            "recent_campaigns": ["Lite and Green"],
            "monthly_growth": 1.2,
        },
    ]


def get_engagement_timeseries(days: int = 30):
    base_date = datetime.now()
    series = []
    base_engagement = 3800
    for i in range(days, 0, -1):
        date = base_date - timedelta(days=i)
        noise = random.uniform(0.75, 1.35)
        weekend_boost = 1.25 if date.weekday() >= 5 else 1.0
        engagement = int(base_engagement * noise * weekend_boost)
        series.append({
            "date": date.strftime("%Y-%m-%d"),
            "engagement": engagement,
            "posts": random.randint(4, 18),
            "reach": engagement * random.randint(8, 20),
        })
    return series


def get_platform_breakdown():
    return [
        {"platform": "Instagram", "posts": 312, "engagement": 48200, "followers": 89000},
        {"platform": "Twitter",   "posts": 487, "engagement": 31500, "followers": 62000},
        {"platform": "LinkedIn",  "posts": 124, "engagement": 18900, "followers": 34000},
        {"platform": "Facebook",  "posts": 198, "engagement": 22400, "followers": 51000},
    ]


def get_sentiment_breakdown():
    return {"positive": 62, "neutral": 26, "negative": 12}


MOCK_DATA = {
    "posts": generate_posts(),
    "comments": generate_comments(),
    "trending_hashtags": generate_trending_hashtags(),
    "competitors": generate_competitor_data(),
    "engagement_timeseries": get_engagement_timeseries(),
    "platform_breakdown": get_platform_breakdown(),
    "sentiment_breakdown": get_sentiment_breakdown(),
    "brand_info": {
        "name": "EcoBottle",
        "followers": 156000,
        "total_posts": 1121,
        "avg_engagement_rate": 4.8,
        "monthly_growth": 5.2,
    },
}
