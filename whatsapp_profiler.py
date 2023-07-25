from whatsapp_parser import WhatsParser
import translators as ts
from work_personality_classifier import identify_work_personality
from tribe_personality_classifier import identify_tribe

"""
Creates a dictionary mapping each person in the chat file to all of their texts
"""
def get_person_to_text_map(filepath: str) -> dict:
    messages = WhatsParser(filepath)
    person_to_text_map = {}

    for message in messages:
        author = message['author']
        content = message['content']
        if author not in person_to_text_map:
            person_to_text_map[author] = [content]
        if content != '<Media omitted>':
            person_to_text_map[author].append(content)

    return person_to_text_map

"""
if the text is in Spanish, returns the translated text in English; otherwise, returns
the same text that is inputted
"""
def translate_to_english(text: str) -> str:
    return ts.translate_text(text)

"""
Categorizes each piece of text sent by the person as being either ant, leech, or bee
and then returns the percentage of the texts that fall into each category as a dictionary
"""
def get_personality_profile(personality_types: list[str], texts: list[str]) -> list[dict]:
    personality_counts = {}
    personality_to_texts = {}

    for personality in personality_types:
        personality_counts[personality] = 0
        personality_to_texts[personality] = []
    
    for text in texts:
        text = translate_to_english(text)
        if 'bee' in personality_types:
            personality_type = identify_work_personality(text)
        elif 'treehugger' in personality_types:
            personality_type = identify_tribe(text)
        else:
            assert('make sure that you have loaded the correct personality types as inputs')

        if personality_type:
            personality_counts[personality_type] += 1
            personality_to_texts[personality_type].append(text)
    
    total_count = 0
    for count in personality_counts.values():
        total_count += count
    
    personality_percentages = {}
    for personality, count in personality_counts.items():
        personality_percentages[personality] = count / total_count
    
    return personality_percentages, personality_to_texts

def get_tribe_personality_profile(texts: list[str]) -> list[dict]:
    personalities = ['treehugger', 'spiritualist', 'nerd', 'fatherlander']
    return get_personality_profile(personalities, texts)

def get_work_personality_profile(texts: list[str]) -> list[dict]:
    personalities = ['ant', 'bee', 'leech']
    return get_personality_profile(personalities, texts)

def profile_whatsapp_messages(filepath):
    person_to_personality_profile = {}
    person_to_text_map = get_person_to_text_map(filepath)

    for person, texts in person_to_text_map.items():
        work_personality_percentages, work_personality_to_texts = get_work_personality_profile(texts)
        tribe_percentages, tribe_to_texts = get_tribe_personality_profile(texts)
        person_to_personality_profile[person] = [work_personality_percentages, work_personality_to_texts, tribe_percentages, tribe_to_texts]
        print(person)
        print(work_personality_percentages)
        print(work_personality_to_texts)
        print(tribe_percentages) 
        print(tribe_to_texts)

    return person_to_personality_profile

print(profile_whatsapp_messages('data-sets/whatsapp_beauvoir.txt'))

