"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Charlestone Mayenga

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    
    enemy_type = enemy_type.lower()
    
    if enemy_type == "goblin":
        return {
            'name': 'Goblin',
            'type': 'goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type == "orc":
        return {
            'name': 'Orc',
            'type': 'orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type == "dragon":
        return {
            'name': 'Dragon',
            'type': 'dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
        self.character = character.copy()  # Use copy to not modify original
        self.enemy = enemy.copy()
        self.combat_active = True
        self.turn_count = 0
        self.battle_log = []
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        
        # Check character isn't dead before starting
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight!")
        
        # Display battle start
        display_battle_log(f"⚔️ Battle started: {self.character['name']} vs {self.enemy['name']}!")
        
        # Battle loop
        while self.combat_active:
            # Display current stats
            display_combat_stats(self.character, self.enemy)
            
            # Player turn
            self.player_turn()
            
            # Check if enemy is dead
            result = self.check_battle_end()
            if result == 'player':
                display_battle_log(f"✓ Victory! {self.enemy['name']} has been defeated!")
                rewards = get_victory_rewards(self.enemy)
                return {
                    'winner': 'player',
                    'xp_gained': rewards['xp'],
                    'gold_gained': rewards['gold']
                }
            
            # Enemy turn (if still alive)
            if self.combat_active and self.enemy['health'] > 0:
                self.enemy_turn()
                
                # Check if character is dead
                result = self.check_battle_end()
                if result == 'enemy':
                    display_battle_log(f"✗ Defeat! You have been defeated by {self.enemy['name']}!")
                    return {
                        'winner': 'enemy',
                        'xp_gained': 0,
                        'gold_gained': 0
                    }
            
            self.turn_count += 1
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active!")
        
        # Display options
        print("\nYour turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Basic attack
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
        
        elif choice == '2':
            # Special ability
            try:
                use_special_ability(self.character, self.enemy)
                display_battle_log(f"{self.character['name']} used special ability!")
            except Exception as e:
                display_battle_log(f"Could not use ability: {e}")
        
        elif choice == '3':
            # Try to escape
            if self.attempt_escape():
                display_battle_log("You escaped from battle!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")
        
        else:
            display_battle_log("Invalid choice, basic attack used instead!")
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active!")
        
        # Enemy always attacks (simple AI)
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        
        # Base damage from strength
        base_damage = attacker['strength']
        
        # Reduction from defender's strength
        defense = defender['strength'] // 4
        
        # Calculate final damage
        damage = base_damage - defense
        
        # Ensure minimum damage of 1
        return max(1, damage)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        
        target['health'] -= damage
        
        # Prevent negative health
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        
        if self.enemy['health'] <= 0:
            return 'player'
        elif self.character['health'] <= 0:
            return 'enemy'
        else:
            return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        
        # 50% chance to escape
        if random.random() < 0.5:
            self.combat_active = False
            return True
        else:
            return False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    
    character_class = character.get('class', '').lower()
    
    if character_class == 'warrior':
        return warrior_power_strike(character, enemy)
    elif character_class == 'mage':
        return mage_fireball(character, enemy)
    elif character_class == 'rogue':
        return rogue_critical_strike(character, enemy)
    elif character_class == 'cleric':
        return cleric_heal(character)
    else:
        return "No special ability available for this class"


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    
    damage = character['strength'] * 2
    enemy['health'] -= damage
    
    if enemy['health'] < 0:
        enemy['health'] = 0
    
    return f"Power Strike! Deals {damage} damage!"


def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    
    damage = character['magic'] * 2
    enemy['health'] -= damage
    
    if enemy['health'] < 0:
        enemy['health'] = 0
    
    return f"Fireball! Deals {damage} damage!"


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    
    if random.random() < 0.5:
        # Critical hit!
        damage = character['strength'] * 3
        enemy['health'] -= damage
        
        if enemy['health'] < 0:
            enemy['health'] = 0
        
        return f"Critical Strike! Deals {damage} damage!"
    else:
        # Miss
        return "Critical Strike missed!"


def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    
    heal_amount = 30
    
    # Don't exceed max health
    if character['health'] + heal_amount > character['max_health']:
        heal_amount = character['max_health'] - character['health']
    
    character['health'] += heal_amount
    
    return f"Healing Light! Restored {heal_amount} HP!"


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    
    return character['health'] > 0


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    
    return {
        'xp': enemy.get('xp_reward', 25),
        'gold': enemy.get('gold_reward', 10)
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    
    print(f"\n--- Combat Status ---")
    print(f"{character['name']}: HP={character['health']}/{character['max_health']} | STR={character['strength']} | MAG={character['magic']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']} | STR={enemy['strength']} | MAG={enemy['magic']}")
    print("-" * 40)


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===\n")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"✓ Created enemy: {goblin['name']}")
        print(f"  Health: {goblin['health']}, Strength: {goblin['strength']}\n")
    except InvalidTargetError as e:
        print(f"✗ Invalid enemy: {e}\n")
    
    # Test level-appropriate enemy
    try:
        level1_enemy = get_random_enemy_for_level(1)
        print(f"✓ Level 1 enemy: {level1_enemy['name']}")
        
        level4_enemy = get_random_enemy_for_level(4)
        print(f"✓ Level 4 enemy: {level4_enemy['name']}")
        
        level7_enemy = get_random_enemy_for_level(7)
        print(f"✓ Level 7 enemy: {level7_enemy['name']}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Test warrior battle
    print("Testing Warrior vs Goblin:")
    print("-" * 40)
    
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'level': 1,
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    orc = create_enemy("orc")
    
    battle = SimpleBattle(test_char, orc)
    
    try:
        # Simulate a quick battle
        print(f"✓ Battle initialized: {battle.character['name']} vs {battle.enemy['name']}")
        print(f"  Character: HP={battle.character['health']}, STR={battle.character['strength']}")
        print(f"  Enemy: HP={battle.enemy['health']}, STR={battle.enemy['strength']}\n")
        
        # Test damage calculation
        damage = battle.calculate_damage(battle.character, battle.enemy)
        print(f"✓ Damage calculation: {damage}")
        
        # Test victory rewards
        rewards = get_victory_rewards(orc)
        print(f"✓ Victory rewards: {rewards['xp']} XP, {rewards['gold']} Gold\n")
        
        # Test character fight check
        can_fight = can_character_fight(test_char)
        print(f"✓ Character can fight: {can_fight}\n")
        
    except CharacterDeadError as e:
        print(f"✗ Character is dead: {e}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    print("=== COMBAT SYSTEM TESTS COMPLETE ===")