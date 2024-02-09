

import spacy 
  
nlp = spacy.load('en_core_web_lg') 
  
  
text = '''Goodman told FOS that the city had initially shown the team’s owners a site with around 60 to 100 acres in the “historic, old part of town … where all major interstate highways come together” and with seven access points'''
word_token = nlp("Deforestation") 
sentence_token = nlp(text)

cleared_sentence_token = nlp(" ".join([t.text for t in sentence_token if not t.is_stop and t.is_alpha]))

similarities = []

for token in cleared_sentence_token:
    sim = token.similarity(word_token)
    similarities.append(sim)
    print(token.text, sim)

similarity = word_token.similarity(sentence_token)
print('similiarity between word and sentence : ', similarity)