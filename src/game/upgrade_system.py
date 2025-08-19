from typing import Dict, List, Tuple
from .resource_manager import ResourceManager

class Upgrade:
    def __init__(self, name: str, description: str, 
                 cost_meat: int = 0, cost_eggs: int = 0, cost_dna: int = 0, cost_cells: int = 0,
                 effect_type: str = "stat", effect_value: float = 1.0, effect_target: str = ""):
        self.name = name
        self.description = description
        self.cost_meat = cost_meat
        self.cost_eggs = cost_eggs  
        self.cost_dna = cost_dna
        self.cost_cells = cost_cells
        self.effect_type = effect_type  # "stat", "ability", "unlock"
        self.effect_value = effect_value
        self.effect_target = effect_target  # "speed", "cargo", "size", etc.
        self.level = 0
        self.max_level = 5

class UpgradeSystem:
    def __init__(self, alien, resources: ResourceManager):
        self.alien = alien
        self.resources = resources
        self.upgrades: Dict[str, Upgrade] = {}
        
        # Link alien to upgrade system for evolution visuals
        self.alien._upgrade_system_ref = self
        
        self.init_upgrades()
    
    def init_upgrades(self):
        # Speed upgrades
        self.upgrades["speed"] = Upgrade(
            "Alien Speed", "Move faster to hunt more efficiently",
            cost_meat=5, effect_type="stat", effect_value=50, effect_target="speed"
        )
        
        # Cargo capacity upgrades
        self.upgrades["cargo"] = Upgrade(
            "Stomach Capacity", "Carry more humans before returning to base",
            cost_meat=10, effect_type="stat", effect_value=2, effect_target="cargo"
        )
        
        # Size upgrades
        self.upgrades["size"] = Upgrade(
            "Alien Growth", "Grow larger to consume humans more easily",
            cost_meat=8, cost_eggs=2, effect_type="stat", effect_value=3, effect_target="size"
        )
        
        # Collection efficiency
        self.upgrades["efficiency"] = Upgrade(
            "Feeding Efficiency", "Convert humans to more meat",
            cost_meat=15, cost_dna=1, effect_type="stat", effect_value=1, effect_target="efficiency"
        )
    
    def can_afford(self, upgrade_name: str) -> bool:
        upgrade = self.upgrades.get(upgrade_name)
        if not upgrade or upgrade.level >= upgrade.max_level:
            return False
        
        # Calculate cost based on level (increases each level)
        level_multiplier = upgrade.level + 1
        cost_meat = upgrade.cost_meat * level_multiplier
        cost_eggs = upgrade.cost_eggs * level_multiplier
        cost_dna = upgrade.cost_dna * level_multiplier
        cost_cells = upgrade.cost_cells * level_multiplier
        
        return self.resources.can_afford(cost_meat, cost_eggs, cost_dna, cost_cells)
    
    def get_upgrade_cost(self, upgrade_name: str) -> Tuple[int, int, int, int]:
        upgrade = self.upgrades.get(upgrade_name)
        if not upgrade:
            return (0, 0, 0, 0)
        
        level_multiplier = upgrade.level + 1
        return (
            upgrade.cost_meat * level_multiplier,
            upgrade.cost_eggs * level_multiplier,
            upgrade.cost_dna * level_multiplier,
            upgrade.cost_cells * level_multiplier
        )
    
    def purchase_upgrade(self, upgrade_name: str) -> bool:
        if not self.can_afford(upgrade_name):
            return False
        
        upgrade = self.upgrades[upgrade_name]
        cost_meat, cost_eggs, cost_dna, cost_cells = self.get_upgrade_cost(upgrade_name)
        
        # Pay the cost
        self.resources.spend_meat(cost_meat)
        self.resources.spend_eggs(cost_eggs)
        self.resources.spend_dna(cost_dna)
        self.resources.spend_cells(cost_cells)
        
        # Apply the upgrade
        upgrade.level += 1
        self.apply_upgrade_effect(upgrade)
        
        return True
    
    def apply_upgrade_effect(self, upgrade: Upgrade):
        if upgrade.effect_type == "stat":
            if upgrade.effect_target == "speed":
                self.alien.speed += upgrade.effect_value
            elif upgrade.effect_target == "cargo":
                self.alien.max_cargo += int(upgrade.effect_value)
            elif upgrade.effect_target == "size":
                self.alien.size += int(upgrade.effect_value)
            elif upgrade.effect_target == "efficiency":
                self.alien.efficiency_bonus += int(upgrade.effect_value)
    
    def get_upgrade_info(self, upgrade_name: str) -> Dict:
        upgrade = self.upgrades.get(upgrade_name)
        if not upgrade:
            return {}
        
        cost_meat, cost_eggs, cost_dna, cost_cells = self.get_upgrade_cost(upgrade_name)
        
        return {
            "name": upgrade.name,
            "description": upgrade.description,
            "level": upgrade.level,
            "max_level": upgrade.max_level,
            "cost_meat": cost_meat,
            "cost_eggs": cost_eggs,
            "cost_dna": cost_dna,
            "cost_cells": cost_cells,
            "can_afford": self.can_afford(upgrade_name),
            "maxed": upgrade.level >= upgrade.max_level
        }