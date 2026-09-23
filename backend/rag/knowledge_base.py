"""
RAG Knowledge Base — lazy import guard
Falls back gracefully when chromadb/sentence-transformers are not installed.
"""

import os

KNOWLEDGE_BASE_DOCS_TEXT = [
    ("brand_identity", "Brand: EcoBottle. Mission: Provide premium reusable water bottles that eliminate single-use plastic. Target Audience: Eco-conscious millennials and Gen Z (ages 18-38), outdoor enthusiasts, fitness-minded professionals. Brand Values: Sustainability, innovation, community, transparency, quality."),
    ("brand_tone", "Brand Tone Guidelines: Professional: authoritative, data-driven, LinkedIn-suitable. Friendly: warm, conversational, Facebook/general. Humorous: witty, Twitter-suitable. Premium: sophisticated, aspirational, Instagram. Educational: informative, clear. Promotional: urgent, benefit-focused, action-oriented."),
    ("products", "Products: EcoBottle Classic $29.99, Pro $44.99 (24hr cold), Sport $34.99, Luxe $54.99, Kids $22.99. All: 100% recyclable packaging, lifetime warranty, carbon-neutral shipping, 1% revenue to clean water."),
    ("target_audience", "Segments: Eco Warriors 22-32 female Instagram. Fitness Enthusiasts 25-40 Instagram/Twitter. Professionals 28-45 LinkedIn. Parents 30-45 Facebook. Gen Z 18-24 Instagram. Best times: Instagram 8-10AM Tue-Thu, LinkedIn 9AM Tue-Wed, Twitter 9AM/12PM/5PM, Facebook 11AM Wed."),
    ("campaign_history", "Campaigns: Refill Revolution Jan 2024: 2.4M impressions 4.8% ER 12K UGC posts. 30-Day Hydration Challenge Mar 2024: 890K participants 25K new followers. Earth Day Pledge Apr 2024: 14 corporate partnerships 6.2% ER LinkedIn. Back to School Aug 2024: 2100 units $94K revenue."),
    ("content_insights", "Top content: Short video 7.2% ER, Carousel 5.8%, UGC 5.4%, Behind-scenes 4.9%, Lifestyle photo 4.3%. Best topics: sustainability facts 8.1%, product demos 6.4%, customer stories 6.2%. Post frequency: Instagram 1x/day, Twitter 3-5x/day, LinkedIn 1x weekday."),
    ("competitor_intelligence", "HydroFlow 128K followers 4.2% ER athlete-focused. GreenSip 94K 3.8% ER eco-aesthetic. PureWave 67K 5.1% ER ocean-campaigns. AquaLite 45K 2.9% ER lightweight focus. EcoBottle advantages: community, product range, eco-storytelling."),
    ("posting_strategy", "Best posting times: Instagram Tue 8-10AM Thu 11AM-1PM Sun 7-9AM. Twitter Tue-Thu 9AM 12PM 5PM. LinkedIn Tue-Wed 8-10AM 12-1PM. Facebook Wed 11AM Sat 10AM-12PM. Respond to comments within 2 hours to boost reach."),
    ("hashtag_strategy", "Tier1 brand: #EcoBottle #RefillRevolution. Tier2 community: #EcoFriendly #ZeroWaste #SustainableLife #PlasticFree. Tier3 discovery: #HydrationGoals #GreenLiving #StayHydrated. Optimal count: Instagram 8-15, Twitter 1-3, LinkedIn 3-5, Facebook 3-7."),
    ("crisis_management", "Response SLA: negative reviews 2hrs, product defects 1hr. Tone: empathetic never defensive. Common issues: lid leaking (resolved v2), shipping delays, price concerns. Counter price with lifetime value. Never argue publicly or delete comments."),
]

_vector_store = None
_rag_available = None


def _check_rag_available():
    global _rag_available
    if _rag_available is not None:
        return _rag_available
    try:
        import chromadb  # noqa
        from sentence_transformers import SentenceTransformer  # noqa
        _rag_available = True
    except ImportError:
        _rag_available = False
    return _rag_available


def _simple_retrieve(query: str, k: int = 4) -> str:
    """Keyword-based retrieval fallback when ChromaDB is unavailable."""
    q = query.lower()
    scored = []
    for category, text in KNOWLEDGE_BASE_DOCS_TEXT:
        score = sum(1 for word in q.split() if len(word) > 3 and word in text.lower())
        scored.append((score, category, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    parts = [f"[Context - {cat}]\n{text.strip()}" for _, cat, text in top]
    return "\n\n".join(parts)


def _chroma_retrieve(query: str, k: int = 4) -> str:
    global _vector_store
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.schema import Document

        if _vector_store is None:
            persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./rag/chroma_db")
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            docs = [Document(page_content=text, metadata={"category": cat})
                    for cat, text in KNOWLEDGE_BASE_DOCS_TEXT]
            splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
            chunks = splitter.split_documents(docs)
            _vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=persist_dir,
                collection_name="social_media_knowledge",
            )

        results = _vector_store.similarity_search(query, k=k)
        parts = [f"[Context - {d.metadata.get('category','general')}]\n{d.page_content.strip()}"
                 for d in results]
        return "\n\n".join(parts) if parts else "No specific context found."
    except Exception as e:
        print(f"[RAG] ChromaDB error: {e}, falling back to keyword search.")
        return _simple_retrieve(query, k)


def retrieve_context(query: str, k: int = 4) -> str:
    """Retrieve relevant brand context. Uses ChromaDB if available, else keyword fallback."""
    if _check_rag_available():
        return _chroma_retrieve(query, k)
    return _simple_retrieve(query, k)
