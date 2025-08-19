from typing import Dict, List, Optional
from enum import Enum

class QuestType(Enum):
    COLLECT_RESOURCES = "collect_resources"
    UPGRADE_STAT = "upgrade_stat"
    SURVIVAL_TIME = "survival_time"

class QuestStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CLAIMED = "claimed"

class Quest:
    def __init__(self, title: str, description: str, quest_type: QuestType,
                 target_value: int, reward_meat: int = 0, reward_eggs: int = 0, 
                 reward_dna: int = 0, reward_cells: int = 0, **kwargs):
        self.title = title
        self.description = description
        self.quest_type = quest_type
        self.target_value = target_value
        self.current_value = 0
        self.status = QuestStatus.ACTIVE
        
        # Rewards
        self.reward_meat = reward_meat
        self.reward_eggs = reward_eggs
        self.reward_dna = reward_dna
        self.reward_cells = reward_cells
        
        # Additional parameters for specific quest types
        self.resource_type = kwargs.get('resource_type', 'meat')
        self.upgrade_name = kwargs.get('upgrade_name', '')
    
    def update_progress(self, value: int):
        if self.status == QuestStatus.ACTIVE:
            self.current_value = min(self.target_value, value)
            if self.current_value >= self.target_value:
                self.status = QuestStatus.COMPLETED
    
    def is_completed(self) -> bool:
        return self.status == QuestStatus.COMPLETED
    
    def is_claimed(self) -> bool:
        return self.status == QuestStatus.CLAIMED
    
    def claim_reward(self) -> Dict[str, int]:
        if self.status == QuestStatus.COMPLETED:
            self.status = QuestStatus.CLAIMED
            return {
                'meat': self.reward_meat,
                'eggs': self.reward_eggs,
                'dna': self.reward_dna,
                'cells': self.reward_cells
            }
        return {}

class QuestSystem:
    def __init__(self, resources, upgrade_system):
        self.resources = resources
        self.upgrade_system = upgrade_system
        self.quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        
        self.init_starting_quests()
    
    def init_starting_quests(self):
        """Create initial set of quests"""
        starting_quests = [
            Quest("First Harvest", "Collect 5 meat", QuestType.COLLECT_RESOURCES, 
                  5, reward_eggs=2, resource_type='meat'),
            Quest("Golden Hunter", "Collect 3 eggs", QuestType.COLLECT_RESOURCES,
                  3, reward_dna=1, resource_type='eggs'),
            Quest("Speed Demon", "Upgrade speed to level 2", QuestType.UPGRADE_STAT,
                  2, reward_meat=10, upgrade_name='speed'),
            Quest("Cargo Master", "Upgrade cargo capacity to level 1", QuestType.UPGRADE_STAT,
                  1, reward_eggs=3, upgrade_name='cargo'),
            Quest("DNA Collector", "Collect 2 DNA", QuestType.COLLECT_RESOURCES,
                  2, reward_cells=1, resource_type='dna'),
        ]
        
        # Add first few quests
        self.quests = starting_quests[:3]  # Start with 3 active quests
    
    def update(self):
        """Update quest progress based on current game state"""
        for quest in self.quests:
            if quest.status == QuestStatus.ACTIVE:
                if quest.quest_type == QuestType.COLLECT_RESOURCES:
                    if quest.resource_type == 'meat':
                        quest.update_progress(self.resources.meat)
                    elif quest.resource_type == 'eggs':
                        quest.update_progress(self.resources.eggs)
                    elif quest.resource_type == 'dna':
                        quest.update_progress(self.resources.dna)
                    elif quest.resource_type == 'cells':
                        quest.update_progress(self.resources.cells)
                
                elif quest.quest_type == QuestType.UPGRADE_STAT:
                    upgrade = self.upgrade_system.upgrades.get(quest.upgrade_name)
                    if upgrade:
                        quest.update_progress(upgrade.level)
    
    def claim_quest_reward(self, quest_index: int) -> bool:
        """Claim reward for completed quest"""
        if 0 <= quest_index < len(self.quests):
            quest = self.quests[quest_index]
            if quest.is_completed() and not quest.is_claimed():
                rewards = quest.claim_reward()
                
                # Add rewards to resources
                self.resources.add_meat(rewards['meat'])
                self.resources.add_eggs(rewards['eggs'])
                self.resources.add_dna(rewards['dna'])
                self.resources.add_cells(rewards['cells'])
                
                # Move to completed quests and add new quest
                self.completed_quests.append(quest)
                self.quests.remove(quest)
                self.add_new_quest()
                
                return True
        return False
    
    def add_new_quest(self):
        """Add a new quest when one is completed"""
        new_quests = [
            Quest("Evolution Path", "Collect 10 DNA", QuestType.COLLECT_RESOURCES,
                  10, reward_meat=20, resource_type='dna'),
            Quest("Size Matters", "Upgrade size to level 3", QuestType.UPGRADE_STAT,
                  3, reward_eggs=5, upgrade_name='size'),
            Quest("Efficiency Expert", "Upgrade efficiency to level 1", QuestType.UPGRADE_STAT,
                  1, reward_dna=3, upgrade_name='efficiency'),
            Quest("Resource Hoarder", "Collect 50 meat", QuestType.COLLECT_RESOURCES,
                  50, reward_cells=5, resource_type='meat'),
            Quest("Cell Division", "Collect 5 cells", QuestType.COLLECT_RESOURCES,
                  5, reward_meat=30, resource_type='cells'),
        ]
        
        # Add random new quest
        if new_quests and len(self.quests) < 3:
            import random
            new_quest = random.choice(new_quests)
            self.quests.append(new_quest)
    
    def get_active_quests(self) -> List[Quest]:
        return [q for q in self.quests if q.status == QuestStatus.ACTIVE]
    
    def get_completed_quests(self) -> List[Quest]:
        return [q for q in self.quests if q.status == QuestStatus.COMPLETED]