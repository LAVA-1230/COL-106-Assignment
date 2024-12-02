from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        
        self.collision_type = collision_type
        self.params = params
        self.z = params[0]
        self.num_elements = 0
        if self.collision_type == "Double":
            self.z2 = params[1]
            self.c2 = params[2]
            self.table_size=params[3]
        else:
            self.table_size = params[1]
        self.table = [None] * self.table_size
        
        pass
        
    def hash_function(self, key):
        h = 0
        for i, char in enumerate(key):
            if 'a' <= char <= 'z':
                p = ord(char) - ord('a')
            elif 'A' <= char <= 'Z':
                p = ord(char) - ord('A') + 26
            h += p * (self.z ** i)
        return h % self.table_size
    
    

    def second_hash_function(self, key):
        h = 0
        for i, char in enumerate(key):
            if 'a' <= char <= 'z':
                p = ord(char) - ord('a')
            elif 'A' <= char <= 'Z':
                p = ord(char) - ord('A') + 26
            h += p * (self.z2 ** i)
        return self.c2 - (h % self.c2)
    
    
    def insert(self, x):
        
        if self.collision_type == "Chain":
            self.insert_Chain(x)
        elif self.collision_type == "Linear":
            self.insert_Linear(x)
        elif self.collision_type == "Double":
            self.insert_Double(x)
        self.num_elements += 1
        pass
 
    def find(self, key):
        if self.collision_type == "Chain":
            return self.find_Chain(key)
        elif self.collision_type == "Linear":
            return self.find_Linear(key)
        elif self.collision_type == "Double":
            return self.find_Double(key)
        pass
    
    def get_slot(self, key):
        return self.hash_function(key)
        pass
    
    def get_load(self):
        return self.num_elements / self.table_size
        pass
    
    def __str__(self):
        
        result = []
        for slot in self.table:
            if slot is None:
                result.append("<EMPTY>")
            elif isinstance(slot, list):
                result.append(" ; ".join(f"({item[0]},{item[1]})" if isinstance(item, tuple) else str(item) for item in slot))
            elif isinstance(slot, tuple):
                result.append(f"({slot[0]},{slot[1]})")
            else:
                result.append(str(slot))
        return " | ".join(result)
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        new_table_size=get_next_size()
        new_table=[None]*new_table_size
        old_table=self.table
        self.table_size=new_table_size
        self.table=new_table
        new_num_elemnts=self.num_elements
        self.num_elements=0
        for slot in old_table:
            if slot is None:
                continue 
            # for chaining
            elif isinstance(slot,list):
                for i in slot: 
                    self.insert(i)
            # for double,linear probing       
            else:
                self.insert(slot)
        self.num_elements=new_num_elemnts
        pass
    
   
    
    
    def insert_Chain(self, x):
        idx = self.hash_function(x[0] if isinstance (x, tuple) else x)
        if self.table[idx] is None:
            self.table[idx] = [x]
        else:
            if isinstance(x,tuple):
                for item in self.table[idx]:
                    if item[0] == x[0]:
                        return
                self.table[idx].append(x)
            else:
                for item in self.table[idx]:
                    if item == x:
                        return
                self.table[idx].append(x)
        
    def insert_Linear(self, x):
        idx = self.hash_function(x[0] if isinstance (x, tuple) else x)
        probe=0
        
        if isinstance(x,tuple):
            while self.table[idx] is not None:
                if self.table[idx][0] == x[0]:
                    return
                idx = (idx + 1) % self.table_size
                probe+=1
                if(probe==self.table_size):
                    raise Exception("Table is full")
            self.table[idx] = x
        else:
            while self.table[idx] is not None:
                if self.table[idx] == x:
                    return
                idx = (idx + 1) % self.table_size
                probe+=1
                if(probe==self.table_size):
                    raise Exception("Table is full")
            self.table[idx] = x
        

    def insert_Double(self, x):
        idx = self.hash_function(x[0] if isinstance(x, tuple) else x)
        step = self.second_hash_function(x[0] if isinstance(x, tuple) else x)
        probe = 0 
        
        
        if isinstance(x,tuple):
            while probe < self.table_size:
                
                if self.table[idx] is None:
                    self.table[idx] = x
                    return
                
                if self.table[idx][0] == x[0]:
                    return
                

                probe += 1
                idx = (idx +  step) % self.table_size
            raise Exception("Table is full")
        
        
        else:
            while probe < self.table_size:
                
                if self.table[idx] is None:
                    self.table[idx] = x
                    return
                
                if self.table[idx] == x:
                    return
                
                probe += 1
                idx = (idx +  step) % self.table_size
            raise Exception("Table is full")
            

    
    def find_Chain(self, key):
        idx = self.hash_function(key)
        if self.table[idx] is not None:
            for item in self.table[idx]:
                if isinstance(item, tuple):
                    if item[0] == key:
                        return item[1]
                elif item == key:
                    return True
        return False
    
    
    def find_Linear(self, key):
        idx = self.hash_function(key)
        count=0
        while self.table[idx] is not None:
            if isinstance(self.table[idx], tuple) and self.table[idx][0] == key:
                if count== self.table_size:
                    return None
                return self.table[idx][1]
            elif self.table[idx] == key:
                if count== self.table_size:
                    return False
                return True
            idx = (idx + 1) % self.table_size    
        return False
    
    def find_Double(self, key):
        idx = self.hash_function(key)
        step = self.second_hash_function(key)
        probe=0

        while probe<self.table_size:
            if isinstance(self.table[idx], tuple) and self.table[idx][0] == key:
                return self.table[idx][1]
            
            elif self.table[idx] == key:
                return True
            probe+=1
            idx = (idx + step) % self.table_size
            
        return False
    
    def size(self):
        return self.num_elements
    
    def table_size_func(self):
        return self.table_size

    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE



    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
        pass
    
    def insert(self, key):
        super().insert(key)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
        pass
    
    def get_all_keys(self):
        """
        Returns a list of all keys (distinct words) stored in the hash table.
        """
        keys = []
        if self.collision_type == "Chain":
            for slot in self.table:
                if slot:  
                    keys.extend(slot)  
        else:
            for slot in self.table:
                if slot is not None:  
                    keys.append(slot)
        
        return keys
    
    def size(self):
        return super().size()
    
    def table_size_func(self):
        return super().table_size_func()
    
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
        pass
    
    def insert(self, x):
        # x = (key, value)
        super().insert(x)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
    
    def size(self):
        return super().size()
    
    def table_size_func(self):
        return super().table_size_func()
    
    
    
    
    
  