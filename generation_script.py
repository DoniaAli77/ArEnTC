"""
ArEnTC Dataset Generation Script
=========================================
Generates Arabic-English code-switched sentences for 9 topic categories
using the GPT-4o mini model via the OpenAI API.

Topics: tech, education, business, health, social, shopping, finance, sports, medical

Requirements:
    pip install openai

Usage:
    Set your OpenAI API key as an environment variable:
        export OPENAI_API_KEY="your-api-key-here"
    Then run:
        python generation_script.py
"""

import os
import json
import time
import random
from openai import OpenAI

# ── Configuration ─────────────────────────────────────────────────────────────

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

NUM_SENTENCES = 12000   # Oversample to yield ~10,000 unique after deduplication
BATCH_SIZE    = 10      # Sentences per API call
NUM_BATCHES   = NUM_SENTENCES // BATCH_SIZE
TEMPERATURE   = 0.7
MAX_TOKENS    = 400

# ── Topic Configurations ──────────────────────────────────────────────────────

TOPIC_CONFIGS = {

    "tech": {
        "subtopics": [
            "artificial intelligence", "cybersecurity", "cloud computing",
            "blockchain", "big data", "software development", "computer networks"
        ],
        "adjectives": ["متطور", "مبتكر", "حديث", "فعال", "متقدم", "كفء"],
        "area_key": "tech_area",
        "example_keyword": "machine learning",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **machine learning** بشكل فعال.",
            "هل تعتقد أن **cybersecurity systems** ستتحسن باستخدام **advanced algorithms**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on technology topics such as artificial intelligence, cybersecurity, "
            "cloud computing, blockchain, big data, software development, and computer networks."
        ),
    },

    "education": {
        "subtopics": [
            "higher education", "online learning", "educational technology",
            "curriculum development", "student engagement", "academic research",
            "distance learning", "educational policies", "primary education", "secondary education"
        ],
        "adjectives": ["متميز", "متطور", "متقدم", "مبتكر", "فعّال", "رائد"],
        "area_key": "education_area",
        "example_keyword": "innovative methods",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **innovative methods** بشكل فعال.",
            "هل تعتقد أن **online learning** ستتحسن باستخدام **modern teaching techniques**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on education topics such as higher education, online learning, "
            "educational technology, curriculum development, student engagement, academic research, "
            "distance learning, and educational policies."
        ),
    },

    "business": {
        "subtopics": [
            "corporate strategy", "entrepreneurship", "workplace productivity",
            "human resources", "management", "marketing", "startup culture",
            "innovation", "project management", "business development"
        ],
        "adjectives": ["ناجح", "مبتكر", "فعّال", "رائد", "متطور", "متميز"],
        "area_key": "business_area",
        "example_keyword": "competitive strategies",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **competitive strategies** بشكل فعال.",
            "هل تعتقد أن **marketing campaigns** ستتحسن باستخدام **data-driven insights**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on business and work topics such as corporate strategy, entrepreneurship, "
            "workplace productivity, human resources, management, marketing, startup culture, "
            "innovation, project management, and business development."
        ),
    },

    "health": {
        "subtopics": [
            "healthcare", "wellness", "nutrition", "fitness",
            "mental health", "public health", "medical research",
            "disease prevention", "health technology", "clinical care"
        ],
        "adjectives": ["صحي", "مبتكر", "فعّال", "موثوق", "متطور", "متقدم"],
        "area_key": "health_area",
        "example_keyword": "innovative treatments",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **innovative treatments** بشكل فعال.",
            "هل تعتقد أن **public health** ستتحسن باستخدام **advanced diagnostics**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on health topics such as healthcare, wellness, nutrition, fitness, "
            "mental health, public health, medical research, disease prevention, "
            "health technology, and clinical care."
        ),
    },

    "social": {
        "subtopics": [
            "social media", "community development", "sociocultural trends",
            "public opinion", "social inequality", "family values",
            "interpersonal relationships", "youth culture", "diversity and inclusion",
            "political engagement"
        ],
        "adjectives": ["مهم", "مؤثر", "ملهم", "متنوع", "متجدد", "مبتكر"],
        "area_key": "social_area",
        "example_keyword": "innovative approaches",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **innovative approaches** بشكل فعال.",
            "هل تعتقد أن **social media campaigns** ستتحسن باستخدام **data-driven insights**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on social topics such as social media, community development, "
            "sociocultural trends, public opinion, social inequality, family values, "
            "interpersonal relationships, youth culture, diversity and inclusion, "
            "and political engagement."
        ),
    },

    "shopping": {
        "subtopics": [
            "online shopping", "retail stores", "e-commerce", "discount deals",
            "shopping malls", "consumer electronics", "grocery shopping",
            "fashion retail", "luxury brands", "daily deals"
        ],
        "adjectives": ["مميز", "عصري", "مغري", "مثير", "متنوع", "راقي"],
        "area_key": "shopping_area",
        "example_keyword": "exclusive offers",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **exclusive offers** بشكل فعال.",
            "هل تعتقد أن **retail stores** ستتحسن باستخدام **modern sales techniques**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on shopping topics such as online shopping, retail stores, e-commerce, "
            "discount deals, shopping malls, consumer electronics, grocery shopping, "
            "and fashion retail."
        ),
    },

    "finance": {
        "subtopics": [
            "banking", "investment", "stock market", "cryptocurrency",
            "financial markets", "economic policy", "portfolio management",
            "risk management", "fintech", "trading", "commodities",
            "fiscal policy", "central banking"
        ],
        "adjectives": ["متميز", "متطور", "فعّال", "ناجح", "حديث", "مبتكر"],
        "area_key": "finance_area",
        "example_keyword": "investment strategies",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **investment strategies** بشكل فعال.",
            "هل تعتقد أن **banking systems** ستتحسن باستخدام **quantitative analysis**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on finance topics such as banking, investment, stock market, "
            "cryptocurrency, trading, risk management, fintech, and economic policy."
        ),
    },

    "sports": {
        "subtopics": [
            "football", "basketball", "tennis", "Olympic sports",
            "athletics", "cricket", "rugby", "baseball", "soccer", "swimming"
        ],
        "adjectives": ["متألق", "مثير", "متطور", "قوي", "متفوق", "متميز"],
        "area_key": "sports_area",
        "example_keyword": "team strategies",
        "example_sentences": [
            "أحد أهم التحديات في **{topic}** هو تطوير **team strategies** بشكل فعال.",
            "هل تعتقد أن **basketball** ستتحسن باستخدام **advanced training techniques**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on sports topics such as football, basketball, tennis, "
            "Olympic sports, athletics, cricket, rugby, and soccer."
        ),
    },

    "medical": {
        "subtopics": [
            "healthcare", "medicine", "public health", "pharmaceuticals",
            "clinical research", "surgery", "nutrition", "mental health",
            "biotechnology", "epidemiology"
        ],
        "adjectives": ["متميز", "متطور", "مبتكر", "حديث", "فعّال", "متقدم"],
        "area_key": "medical_area",
        "example_keyword": "innovative treatments",
        "example_sentences": [
            "أحد أهم التحديات في **healthcare** هو تطوير **innovative treatments** بشكل فعال.",
            "هل تعتقد أن **public health** ستتحسن باستخدام **advanced diagnostics**؟"
        ],
        "focus_instruction": (
            "Focus ONLY on medical topics such as healthcare, medicine, public health, "
            "pharmaceuticals, clinical research, surgery, nutrition, mental health, "
            "and biotechnology."
        ),
    },
}

# ── Complexity Templates (shared structure across all topics) ─────────────────

COMPLEXITY_TEMPLATES = {
    "simple": [
        "استخدام {keyword} أصبح شائعاً في {adj} {area}.",
        "هل تعتقد أن {area} ستتحسن باستخدام {keyword}؟",
        "جرّب {keyword} لتعزيز {adj} {area}.",
        "الاعتماد على {keyword} أصبح أساسياً في {adj} {area}."
    ],
    "moderate": [
        "أحد أهم تحديات {area} هو تطوير {keyword} بشكل فعال في بيئة {adj}.",
        "مع تطور {keyword}، كيف يمكن أن يتغير {adj} {area}؟",
        "إذا تم تطبيق {keyword} بفعالية، فإن {area} {adj} سيشهد تحسناً ملحوظاً.",
        "يعتبر تحسين {area} باستخدام {keyword} خطوة {adj} نحو التقدم."
    ],
    "complex": [
        "لو لم يكن هناك {keyword}، كيف سيكون تأثير ذلك على {adj} {area}؟",
        "بينما يستمر {keyword} في التطور، تظهر تحديات جديدة في {area} {adj} تحتاج إلى حلول مبتكرة.",
        "لتعزيز {adj} {area}، نحتاج إلى **cutting-edge solutions**.",
        "تتطلب مواجهة تحديات {adj} في {area} استخدام {keyword} بشكل مبتكر."
    ]
}

EXTRA_PHRASES = [
    "", " حاول استكشاف زوايا جديدة.", " استخدم أساليب مبتكرة.", " تذكر أن تكون مبدعاً."
]

# ── Prompt Builder ────────────────────────────────────────────────────────────

def build_prompt(config):
    topic       = random.choice(config["subtopics"])
    complexity  = random.choice(["simple", "moderate", "complex"])
    adj         = random.choice(config["adjectives"])
    template    = random.choice(COMPLEXITY_TEMPLATES[complexity])
    example_s   = template.format(
        keyword=f"**{config['example_keyword']}**",
        area=f"**{topic}**",
        adj=adj
    )
    ex1, ex2    = config["example_sentences"]
    extra       = random.choice(EXTRA_PHRASES)

    return (
        f"Generate {BATCH_SIZE} Arabic-English code-switched sentences in JSON format. "
        f"Each sentence should be 15-20 words long, containing ~44% English. "
        f"Ensure natural phrase-level switching, not just single words. "
        f"Use varied structures: statements, questions, conditionals, imperatives, and cause-effect. "
        f"{config['focus_instruction']}\n\n"
        f"Examples:\n"
        f"- \"{ex1.format(topic=topic)}\"\n"
        f"- \"{ex2}\"\n"
        f"- \"{example_s}\"\n\n"
        f"Return ONLY a JSON array of sentences, e.g., [\"sentence1\", \"sentence2\", ...].{extra}"
    )

# ── Generation Loop ───────────────────────────────────────────────────────────

def generate_topic(topic_name, config):
    print(f"\n{'='*60}")
    print(f"Generating topic: {topic_name.upper()}")
    print(f"{'='*60}")

    dataset = []
    total_tokens = 0

    for i in range(NUM_BATCHES):
        print(f"  Batch {i+1}/{NUM_BATCHES}...", end="\r")
        prompt = build_prompt(config)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

            if response and response.choices:
                text = response.choices[0].message.content.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()
                try:
                    sentences = json.loads(text)
                    if isinstance(sentences, list):
                        dataset.extend(sentences)
                except json.JSONDecodeError:
                    print(f"\n  Warning: JSON decode failed on batch {i+1}")

                total_tokens += response.usage.total_tokens

        except Exception as e:
            print(f"\n  Error on batch {i+1}: {e}")

        # Save progress every 50 batches
        if (i + 1) % 50 == 0:
            with open(f"{topic_name}_progress.json", "w", encoding="utf-8") as f:
                json.dump(dataset, f, ensure_ascii=False, indent=4)

        time.sleep(1)  # Avoid rate limits

    print(f"\n  Raw sentences collected: {len(dataset)}")
    print(f"  Estimated cost: ${(total_tokens / 1000) * 0.0005:.4f}")
    return dataset

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    for topic_name, config in TOPIC_CONFIGS.items():
        raw = generate_topic(topic_name, config)

        # Save raw output per topic
        output_file = f"{topic_name}_raw.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=4)
        print(f"  Saved: {output_file} ({len(raw)} sentences)")

    print(f"\n{'='*60}")
    print("Generation complete. Raw outputs saved per topic.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
