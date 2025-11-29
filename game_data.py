"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Charlestone Mayenga

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    
    # Check if file exists
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")
    
    # Try to read the file
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        raise CorruptedDataError(f"Could not read quest file: {e}")
    
    # Parse quests (separated by blank lines)
    quests = {}
    quest_blocks = content.strip().split('\n\n')
    
    try:
        for block in quest_blocks:
            if not block.strip():
                continue
            
            # Parse this quest block
            lines = block.strip().split('\n')
            quest = parse_quest_block(lines)
            
            # Validate the quest
            validate_quest_data(quest)
            
            # Store by quest_id
            quests[quest['quest_id']] = quest
    
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error parsing quest data: {e}")
    
    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    
    # Check if file exists
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    # Try to read the file
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        raise CorruptedDataError(f"Could not read item file: {e}")
    
    # Parse items (separated by blank lines)
    items = {}
    item_blocks = content.strip().split('\n\n')
    
    try:
        for block in item_blocks:
            if not block.strip():
                continue
            
            # Parse this item block
            lines = block.strip().split('\n')
            item = parse_item_block(lines)
            
            # Validate the item
            validate_item_data(item)
            
            # Store by item_id
            items[item['item_id']] = item
    
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error parsing item data: {e}")
    
    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    
    required_fields = {
        'quest_id': str,
        'title': str,
        'description': str,
        'reward_xp': int,
        'reward_gold': int,
        'required_level': int,
        'prerequisite': str
    }
    
    # Check each required field
    for field, field_type in required_fields.items():
        # Check if field exists
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
        # Check field type
        if not isinstance(quest_dict[field], field_type):
            raise InvalidDataFormatError(
                f"Invalid type for field '{field}': expected {field_type.__name__}, "
                f"got {type(quest_dict[field]).__name__}"
            )
    
    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    
    required_fields = {
        'item_id': str,
        'name': str,
        'type': str,
        'effect': dict,
        'cost': int,
        'description': str
    }
    
    # Check each required field
    for field, field_type in required_fields.items():
        # Check if field exists
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
        # Check field type
        if not isinstance(item_dict[field], field_type):
            raise InvalidDataFormatError(
                f"Invalid type for field '{field}': expected {field_type.__name__}, "
                f"got {type(item_dict[field]).__name__}"
            )
    
    # Validate item type
    valid_types = {'weapon', 'armor', 'consumable'}
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(
            f"Invalid item type: {item_dict['type']}. Must be one of {valid_types}"
        )
    
    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    
    # Create data directory if needed
    if not os.path.exists("data"):
        try:
            os.makedirs("data")
        except Exception as e:
            print(f"Warning: Could not create data directory: {e}")
    
    # Create default quests file
    quests_file = "data/quests.txt"
    if not os.path.exists(quests_file):
        try:
            default_quests = """QUEST_ID: defeat_goblin
TITLE: Defeat the Goblin
DESCRIPTION: A goblin has been causing trouble in the nearby forest. Defeat it!
REWARD_XP: 50
REWARD_GOLD: 25
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: slay_orc
TITLE: Slay the Orc
DESCRIPTION: A powerful orc has been terrorizing the village. Defeat it to save the people!
REWARD_XP: 150
REWARD_GOLD: 75
REQUIRED_LEVEL: 3
PREREQUISITE: defeat_goblin

QUEST_ID: defeat_dragon
TITLE: Defeat the Dragon
DESCRIPTION: The mighty dragon must be stopped before it destroys everything!
REWARD_XP: 500
REWARD_GOLD: 250
REQUIRED_LEVEL: 6
PREREQUISITE: slay_orc"""
            
            with open(quests_file, 'w') as f:
                f.write(default_quests)
            print(f"✓ Created default quests file: {quests_file}")
        except Exception as e:
            print(f"Warning: Could not create default quests file: {e}")
    
    # Create default items file
    items_file = "data/items.txt"
    if not os.path.exists(items_file):
        try:
            default_items = """ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 50
DESCRIPTION: A basic iron sword. Good for beginners.

ITEM_ID: steel_armor
NAME: Steel Armor
TYPE: armor
EFFECT: defense:3
COST: 100
DESCRIPTION: Protective steel armor. Reduces incoming damage.

ITEM_ID: health_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:50
COST: 25
DESCRIPTION: Restores 50 health points when used.

ITEM_ID: ancient_bow
NAME: Ancient Bow
TYPE: weapon
EFFECT: strength:8
COST: 150
DESCRIPTION: A legendary bow carved from ancient wood.

ITEM_ID: dragon_scale_armor
NAME: Dragon Scale Armor
TYPE: armor
EFFECT: defense:8
COST: 300
DESCRIPTION: Forged from real dragon scales. Extremely protective."""
            
            with open(items_file, 'w') as f:
                f.write(default_items)
            print(f"✓ Created default items file: {items_file}")
        except Exception as e:
            print(f"Warning: Could not create default items file: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    
    quest = {}
    
    try:
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for colon separator
            if ':' not in line:
                raise InvalidDataFormatError(f"Malformed line in quest data: {line}")
            
            # Split on colon and strip whitespace
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Parse different field types
            if key == 'quest_id':
                quest['quest_id'] = value
            elif key == 'title':
                quest['title'] = value
            elif key == 'description':
                quest['description'] = value
            elif key == 'reward_xp':
                quest['reward_xp'] = int(value)
            elif key == 'reward_gold':
                quest['reward_gold'] = int(value)
            elif key == 'required_level':
                quest['required_level'] = int(value)
            elif key == 'prerequisite':
                quest['prerequisite'] = value
            else:
                raise InvalidDataFormatError(f"Unknown field in quest: {key}")
    
    except ValueError as e:
        raise InvalidDataFormatError(f"Could not convert value to correct type: {e}")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")
    
    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    
    item = {}
    
    try:
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for colon separator
            if ':' not in line:
                raise InvalidDataFormatError(f"Malformed line in item data: {line}")
            
            # Split on colon and strip whitespace
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Parse different field types
            if key == 'item_id':
                item['item_id'] = value
            elif key == 'name':
                item['name'] = value
            elif key == 'type':
                item['type'] = value.lower()
            elif key == 'effect':
                # Parse effect as stat:value pair
                if ':' not in value:
                    raise InvalidDataFormatError(f"Invalid effect format: {value}")
                stat, stat_value = value.split(':', 1)
                item['effect'] = {stat.strip(): int(stat_value.strip())}
            elif key == 'cost':
                item['cost'] = int(value)
            elif key == 'description':
                item['description'] = value
            else:
                raise InvalidDataFormatError(f"Unknown field in item: {key}")
    
    except ValueError as e:
        raise InvalidDataFormatError(f"Could not convert value to correct type: {e}")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")
    
    return item


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===\n")
    
    # Test creating default files
    print("Creating default data files...")
    create_default_data_files()
    print()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"✓ Loaded {len(quests)} quests")
        for quest_id, quest in quests.items():
            print(f"  - {quest['title']} (ID: {quest_id}, Level: {quest['required_level']})")
        print()
    except MissingDataFileError as e:
        print(f"✗ Quest file not found: {e}\n")
    except InvalidDataFormatError as e:
        print(f"✗ Invalid quest format: {e}\n")
    except CorruptedDataError as e:
        print(f"✗ Corrupted quest data: {e}\n")
    
    # Test loading items
    try:
        items = load_items()
        print(f"✓ Loaded {len(items)} items")
        for item_id, item in items.items():
            print(f"  - {item['name']} (ID: {item_id}, Type: {item['type']}, Cost: {item['cost']})")
        print()
    except MissingDataFileError as e:
        print(f"✗ Item file not found: {e}\n")
    except InvalidDataFormatError as e:
        print(f"✗ Invalid item format: {e}\n")
    except CorruptedDataError as e:
        print(f"✗ Corrupted item data: {e}\n")
    
    # Test validation
    try:
        test_quest = {
            'quest_id': 'test',
            'title': 'Test Quest',
            'description': 'A test quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
        validate_quest_data(test_quest)
        print("✓ Quest validation passed\n")
    except InvalidDataFormatError as e:
        print(f"✗ Quest validation failed: {e}\n")
    
    try:
        test_item = {
            'item_id': 'test_item',
            'name': 'Test Item',
            'type': 'weapon',
            'effect': {'strength': 5},
            'cost': 100,
            'description': 'A test item'
        }
        validate_item_data(test_item)
        print("✓ Item validation passed\n")
    except InvalidDataFormatError as e:
        print(f"✗ Item validation failed: {e}\n")
    
    print("=== GAME DATA MODULE TESTS COMPLETE ===")