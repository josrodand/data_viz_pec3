

def clean_abrv(text):
    """"""
    if '_' in text:
        return text.split('_')[1]
    else:
        return text