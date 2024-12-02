import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        
        pass
    
    def distinct_words(self, book_title):
        
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):      
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        combined = list(zip(book_titles, texts))
        sorted_combined = self.merge_sort(combined, key=lambda x: x[0])  #tc is klogk
        book_titles, texts = zip(*sorted_combined)
        book_titles = list(book_titles)
        texts = [self.merge_sort(text) for text in texts]     #tc is k*WlogW
        
        self.book_titles= book_titles
        self.texts = texts

        self.distinct_words_list = [self.calculate_distinct_words(text) for text in self.texts]   #tc is k*W thus can be neglected 
        
        pass

    def merge_sort(self, arr, key=lambda x: x):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key)
        right = self.merge_sort(arr[mid:], key)

        return self.merge(left, right, key)

    def merge(self, left, right, key):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    
    def distinct_words(self, book_title):
        index = self.binary_search(book_title,self.book_titles)
        
        return self.distinct_words_list[index]
        
        
        pass
    
    def count_distinct_words(self, book_title):
        index = self.binary_search(book_title,self.book_titles)
        return len(self.distinct_words_list[index])
        pass
    
    def search_keyword(self, keyword):
        book_containg_key=[]
        for idx,book in enumerate(self.book_titles):
            if self.binary_search(keyword,self.distinct_words_list[idx])!=-1:
                book_containg_key.append(book)
        return book_containg_key
        pass
    
    def print_books(self):
        for title, distinct_words in zip(self.book_titles, self.distinct_words_list):
            formatted_words = " | ".join(distinct_words)
            print(f"{title}: {formatted_words}")
        
        pass
    
    def binary_search(self,key,list_searched):
        s=0
        e=len(list_searched)-1  
        while(s<=e):
            mid=(s+e)//2
            if list_searched[mid]==key:
                return mid
            elif list_searched[mid]<key:
                s=mid+1
            else:
                e=mid-1
            
        return -1  
    
    
    def calculate_distinct_words(self, text):
        distinct_words = []
        previous_word = None
        for word in text:
            if word != previous_word:  
                distinct_words.append(word)
            previous_word = word
        return distinct_words
                
        
class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        
        self.name=name
        self.params=params
        
        self.books = self.create_hash_map_class(self.name,self.params)
        self.nonemptylist =[]
        pass
    
    def create_hash_set_class(self, name, params):
        if name == "Jobs":
            return ht.HashSet("Chain", params)  # Chaining
        elif name == "Gates":
            return ht.HashSet("Linear", params)  # Linear probing
        elif name == "Bezos":
            return ht.HashSet("Double", params)  # Double Chaining
    
    
    def create_hash_map_class(self, name, params):
        if name == "Jobs":
            return ht.HashMap("Linear", params)  # Chaining
        elif name == "Gates":
            return ht.HashMap("Linear", params)  # Linear probing
        elif name == "Bezos":
            return ht.HashMap("Linear", (params[0],params[3])) #Double Hashing
        
        
    
    def add_book(self, book_title, text):
        book_hash_table = self.create_hash_set_class(self.name,self.params) 
        for word in text: 
            if not book_hash_table.find(word):
                book_hash_table.insert(word)  
        self.books.insert((book_title, book_hash_table))
        self.nonemptylist.append((book_title, book_hash_table))
        pass
    
    def distinct_words(self, book_title):
        book_hash_table = self.books.find(book_title)
        if book_hash_table:
            return book_hash_table.get_all_keys()  
        pass
    
    def count_distinct_words(self, book_title):
        book_hash_table = self.books.find(book_title)
        if book_hash_table:
            return book_hash_table.size()  
    
    def search_keyword(self, keyword):
        matching_books = []
        for slot in self.nonemptylist:
            if slot and isinstance(slot, tuple):  
                title, book_hash_table = slot
                if book_hash_table.find(keyword):  
                    matching_books.append(title)
        return matching_books
        pass
    
    def print_books(self):
        for slot in self.nonemptylist:
            if slot and isinstance(slot, tuple): 
                title, book_hash_table = slot
                print(f"{title}: {self.format_hash_table(book_hash_table)}")
        
                
    def format_hash_table(self, hash_table):
        formatted_slots = []

        if hash_table.collision_type == "Chain":
            for slot in hash_table.table:
                if slot is None:
                    formatted_slots.append("<EMPTY>") 
                else:
                    formatted_slots.append(" ; ".join(map(str, slot)))  
            return " | ".join(formatted_slots)
        
        else:
            for slot in hash_table.table:
                if slot is None:
                    formatted_slots.append("<EMPTY>")
                else:
                    formatted_slots.append(str(slot))
            return " | ".join(formatted_slots)