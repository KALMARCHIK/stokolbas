from re import sub as re_sub

def preprocess_string(s):
    s = s.lower()
    s = re_sub(r'[^\w\s]', '', s)
    s = re_sub(r'\s+', ' ', s).strip()
    return s

def name_matching(name1, name2):
    name1 = preprocess_string(name1)
    name2 = preprocess_string(name2)
    
    reference_tokens = set(name1.split())
    comparison_tokens = set(name2.split())
    
    matches = len(reference_tokens.intersection(comparison_tokens))
    
    total_reference_tokens = len(reference_tokens)
    similarity_percentage = (matches / total_reference_tokens) if total_reference_tokens > 0 else 0
    
    return similarity_percentage
