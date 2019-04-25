# Spell Checker
### Checks for misspellings in a text


Given an input word from the user, the wordSplitSet function generates a list of tuples with all possible combinations of the input word
1. The words are juggled/ re-assembled
2. Additional alphabetic characters are added at various positions of all combinations
3. In the case of repetitive characters, replacement is done instead of addition
4. Alphabetic characters are also deleted to generate more suggestions
5. Looks up for the word in the corpus
6. Creates a dictionary with the word suggestion as the 'key' and its probabilty of occurence as the 'value'

### Provides the best two possible word suggestions based on the concept of probability
Cases
1. When the word is not present in the corpus
2. When the word is present, but has incorect spelling
3. When the word is present, but has possibly a correct spelling
4. When the word is present with correct spelling, but with second best frequency in the corpus
