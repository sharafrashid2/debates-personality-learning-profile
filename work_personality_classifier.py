from transformers import pipeline

# the following three lists are the three categories for which classifications will be made
values = ['benevolence', 'conformity', 'competitive', 'power']
morals = ['just', 'exploitative']
personality = ['open-minded', 'creative', 'dutiful', 'judgemental']
# risk_taking = ['social risk', 'financial risk', 'ethical risk', 'no risk']

personality_traits = values+personality+morals
personality_traits = list(dict.fromkeys(personality_traits))

traits = list(dict.fromkeys(personality_traits))

types_to_traits = {'ant': {'conformity', 'dutiful', 'competitive', 'neutral'},
                  'bee': {'benevolence', 'creative', 'selfless', 'open-minded', 'just'},
                  'leech': {'achievement', 'power', 'selfish', 'judgemental', 'exploitative'}}

traits_to_type = {}
for type, traits in types_to_traits.items():
    for trait in traits:
        traits_to_type[trait] = type

# the classifier that will be used to identify the personality traits
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

"""
From the inference made with the classifier, returns the trait with the highest percentage
"""
def get_highest_score_trait(inference):
    return inference['labels'][0]

"""
Using the three classifiers, follows an algorithm specified below to determine which personality
type matches the text the most.

The algorithm for determining this is the following:
    If there is a personality trait within the values list that is the dominant trait by at least 10%,
        if that dominant trait is power and the dominant trait for morals is exploitative,
            then the personality type is a leech
        else if that dominant trait is power and the dominant trait for morals is NOT exploitative,
            then the personality type is an ant
        else,
            the personality type is the type that the dominant trait matches with
    Else,
        if exploitative is the dominant trait with percentage more than 60%,
            the personality type is a leech
        else if there is a personality trait within the personality list that is the dominant trait by at least 10%,
            the personality type is the type that the dominant trait matches with
        else,
            no personality type can be determined 
"""
def get_type(values_inference, morals_inference, personality_inference):

    highest_score_value = get_highest_score_trait(values_inference)
    highest_score = values_inference['scores'][0]

    significant_check = True

    for i, score in enumerate(values_inference['scores']):
        if (values_inference['labels'][i] != highest_score_value and values_inference['labels'][i] != 'no risk' and 
            abs(score - highest_score) < 0.10 and traits_to_type[values_inference['labels'][i]] != traits_to_type[highest_score_value]):
            significant_check = False

    if significant_check and highest_score_value == 'power':
        if morals_inference['labels'][0] == 'exploitative':
            return 'leech'
        else:
            return 'ant'
    
    elif significant_check:
        return traits_to_type[highest_score_value]
    
    else:
        highest_score_personality = get_highest_score_trait(personality_inference)
        highest_score = personality_inference['scores'][0]

        significant_check = True

        for i, score in enumerate(personality_inference['scores']):
            if (personality_inference['labels'][i] !=  highest_score_personality and personality_inference['labels'][i] != 'no risk' and 
                abs(score - highest_score) < 0.10 and traits_to_type[personality_inference['labels'][i]] != traits_to_type[highest_score_personality]):
                significant_check = False
        
        if significant_check:
            return traits_to_type[highest_score_personality]
        if morals_inference['labels'][0] == 'exploitative' and morals_inference['scores'][0] >= 0.6:
            return 'leech'
        return None

"""
Function that gets the inferences for morals, values, and personality and then uses the inferences
to return the personality type identified from the given text
"""
def identify_work_personality(text):
    morals_inference = classifier(text, candidate_labels=morals)
    values_inference = classifier(text, candidate_labels=values)
    personality_inference = classifier(text, candidate_labels=personality)
    return get_type(values_inference, morals_inference, personality_inference)

print(identify_work_personality("I don't care about the outcome of others. I just want to be successful."))