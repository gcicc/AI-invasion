class ResourceManager:
    def __init__(self):
        self.meat = 0
        self.eggs = 0
        self.dna = 0
        self.cells = 0
        
        self.meat_per_second = 0.0
        self.eggs_per_second = 0.0
        
        self.idle_timer = 0.0
    
    def update(self, dt: float):
        self.idle_timer += dt
        
        if self.idle_timer >= 1.0:
            self.meat += int(self.meat_per_second)
            self.eggs += int(self.eggs_per_second)
            self.idle_timer = 0.0
    
    def add_meat(self, amount: int):
        self.meat += amount
    
    def add_eggs(self, amount: int):
        self.eggs += amount
    
    def add_dna(self, amount: int):
        self.dna += amount
    
    def add_cells(self, amount: int):
        self.cells += amount
    
    def spend_meat(self, amount: int) -> bool:
        if self.meat >= amount:
            self.meat -= amount
            return True
        return False
    
    def spend_eggs(self, amount: int) -> bool:
        if self.eggs >= amount:
            self.eggs -= amount
            return True
        return False
    
    def spend_dna(self, amount: int) -> bool:
        if self.dna >= amount:
            self.dna -= amount
            return True
        return False
    
    def spend_cells(self, amount: int) -> bool:
        if self.cells >= amount:
            self.cells -= amount
            return True
        return False
    
    def can_afford(self, meat: int = 0, eggs: int = 0, dna: int = 0, cells: int = 0) -> bool:
        return (self.meat >= meat and 
                self.eggs >= eggs and 
                self.dna >= dna and 
                self.cells >= cells)