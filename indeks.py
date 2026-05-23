import string

def index_documents(documents: list[str], queries: list[str]) -> list[list[int]]:
    """
    Przetwarza dokumenty i zapytania, zwracając listy indeksów dokumentów,
    w których występuje zapytanie, posortowane według częstości wystąpienia
    danego wyrazu (malejąco), a w przypadku równych częstości - rosnąco wg numeru dokumentu.

    Args:
        documents (list[str]): Lista dokumentów (każdy dokument to ciąg znaków).
        queries (list[str]): Lista zapytań (każdy zapytanie to pojedynczy wyraz).

    Returns:
        list[list[int]]: Lista wyników dla kolejnych zapytań.
    """
    # Słownik, w którym przechowujemy strukturę: {słowo: {id_dokumentu: liczba_wystąpień}}
    inverted_index = {}
    
    # Tworzymy tłumacza, który zamieni wszystkie znaki interpunkcyjne na spacje
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    
    for doc_id, doc in enumerate(documents):
        # Usuwamy interpunkcję i zmieniamy wszystko na małe litery
        cleaned_doc = doc.translate(translator).lower()
        words = cleaned_doc.split()
        
        # Zliczamy wystąpienia każdego słowa w danym dokumencie
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {}
            if doc_id not in inverted_index[word]:
                inverted_index[word][doc_id] = 0
            inverted_index[word][doc_id] += 1
            
    results = []
    
    # Przeszukujemy nasz indeks dla każdego zapytania
    for query in queries:
        q = query.lower().strip()
        if q in inverted_index:
            doc_counts = inverted_index[q]
            # Sortujemy: najpierw po częstości (malejąco), potem po ID dokumentu (rosnąco)
            sorted_docs = sorted(doc_counts.items(), key=lambda x: (x[1], -x[0]), reverse=True)
            # Wyciągamy same ID dokumentów z posortowanej listy
            results.append([doc_id for doc_id, count in sorted_docs])
        else:
            results.append([])
            
    return results


# Przykładowe wywołanie:
if __name__ == "__main__":
    # Zakomentowałem tutaj inputy, żebyś mógł to łatwo przetestować w notatniku 
    # bez ręcznego wpisywania za każdym razem.
    
    doc_test = [
        "Your care set up, do not pluck my care down.",
        "My care is loss of care with old care done.",
        "Your care is gain of care when new care is won."
    ]
    query_test = ["care", "is", "nieistniejaceslowo"]
    
    wyniki = index_documents(doc_test, query_test)
    for res in wyniki:
        print(res)
        
    # Spodziewany wynik:
    # [1, 2, 0]
    # [2, 1]
    # []