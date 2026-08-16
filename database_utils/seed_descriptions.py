from helpers.chunk_text import chunk_text

DESCRIPTIONS = [
    {
        "slug": "jimmys",
        "description": """Fast, powerful barrel. the bigger it gets, the more perfect. has to be an sw swell. board breaks are common, but so are the tubes of your life. hollow barrels of ~75 meters
intollerant to the predominant SE trade winds, so you need to go early when it's glassy or have a day with western winds (not uncommon, especially if it is cloudy on the coast)
watch out for the end section. it's shallow and the wave closes out. better to get in the barrel, get out and get out the back""",
    },
    {
        "slug": "the_peak",
        "description": """The peak can be described as "the friendliest slab". The wave is a barrelling triangle that whips down the point from deep water and throws itself onto a shallow reef. The barrels are perfect, intense and short.
The wave is moody. There is no formula to when this wave works: sometimes it's best at high tide, sometimes low tide, maybe in between. The only constant is that you need the SE trade winds.
To surf the wave properly, you have to takeoff behind the peak. If you don't, the barrel will behind you or very short.
The left appears the more west in the swell, but the best lefts are on the smaller to medium sized waves.
The wave is often crowded but you can find windows with only a few guys out. Many people think they want to surf here, but soon get much shy after paddling out. Many of the people in the lineup are not catching a lot of waves

When you're surfing, expect:
- waits between sets
- small takeoff zone
- steep and deep backdoor takeoffs
- hitting the reef""",
    },
]


def seed_descriptions(collection):
    for spot in DESCRIPTIONS:
        slug = spot["slug"]
        chunks = chunk_text(spot["description"])

        if not chunks:
            print(f"{slug} skipped: no description chunks")
            continue

        collection.add(
            ids=[f"{slug}chunk{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"source": slug, "chunk_index": i} for i in range(len(chunks))],
        )
        print(f"{slug} processed: {len(chunks)} chunks")
