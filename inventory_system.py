"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Charlestone Mayenga

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    
    # Check if inventory is full
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Inventory is full! Maximum capacity is {MAX_INVENTORY_SIZE}")
    
    # Add item to inventory
    character['inventory'].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    
    # Check if item exists
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory")
    
    # Remove item from inventory
    character['inventory'].remove(item_id)
    return True


def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    
    return item_id in character['inventory']


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    
    return character['inventory'].count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    
    return MAX_INVENTORY_SIZE - len(character['inventory'])


def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    
    # Save items before clearing
    removed_items = character['inventory'].copy()
    
    # Clear inventory
    character['inventory'] = []
    
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    
   # Check item exists
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # ✅ Check item is consumable type
    item_type = item_data.get('type', '')
    if item_type != 'consumable':
        raise InvalidItemTypeError(
            f"Cannot use '{item_id}': item type is '{item_type}', "
            f"not 'consumable'. Only consumable items can be used."
        )
    
    # Apply effect
    if 'effect' in item_data:
        effect = item_data['effect']
        
        # Parse string format: "stat:value"
        if isinstance(effect, str):
            try:
                stat_name, value_str = effect.split(':')
                value = int(value_str)
                apply_stat_effect(character, stat_name, value)
            except (ValueError, IndexError):
                raise InvalidItemTypeError(f"Invalid effect format: {effect}")
        
        # Parse dict format: {'stat': value}
        elif isinstance(effect, dict):
            for stat_name, value in effect.items():
                apply_stat_effect(character, stat_name, value)
    
    # Remove used item
    character['inventory'].remove(item_id)
    
    return f"Used {item_id}"


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    
    # Check item exists
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Check it's a weapon
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"'{item_id}' is not a weapon")
    
    # Unequip current weapon if any
    if character.get('equipped_weapon'):
        old_weapon = character['equipped_weapon']
        try:
            unequip_weapon(character)
        except InventoryFullError:
            # Inventory full, can't unequip
            raise InventoryFullError("Cannot unequip: inventory full")
    
    # Remove from inventory
    character['inventory'].remove(item_id)
    
    # Apply weapon bonus
    if 'effect' in item_data:
        effect = item_data['effect']
        
        # Parse effect if it's a string (format: "stat:value")
        if isinstance(effect, str):
            try:
                stat_name, value_str = effect.split(':')
                value = int(value_str)
                character[stat_name] = character.get(stat_name, 0) + value
            except (ValueError, IndexError):
                raise InvalidItemTypeError(f"Invalid effect format: {effect}")
        
        # Or apply if it's a dict
        elif isinstance(effect, dict):
            for stat_name, value in effect.items():
                character[stat_name] = character.get(stat_name, 0) + value
    
    # Set equipped weapon
    character['equipped_weapon'] = item_id
    
    return f"Equipped {item_id}"


def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    
    # Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Check if item type is armor
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")
    
    # Unequip current armor if exists
    if 'equipped_armor' in character and character['equipped_armor'] is not None:
        unequip_armor(character)
    
    # Parse effect and apply
    effect = item_data.get('effect', {})
    if isinstance(effect, dict):
        for stat_name, value in effect.items():
            apply_stat_effect(character, stat_name, value)
    
    # Store equipped armor
    character['equipped_armor'] = item_id
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    return f"Equipped {item_data.get('name', item_id)}!"


def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    
    # Check if weapon is equipped
    if 'equipped_weapon' not in character or character['equipped_weapon'] is None:
        return None
    
    weapon_id = character['equipped_weapon']
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip weapon.")
    
    # We would need weapon_data to remove bonuses, so for now just store the item
    # The calling function should handle removing stat bonuses
    
    # Add weapon back to inventory
    character['inventory'].append(weapon_id)
    
    # Clear equipped weapon
    character['equipped_weapon'] = None
    
    return weapon_id


def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    
    # Check if armor is equipped
    if 'equipped_armor' not in character or character['equipped_armor'] is None:
        return None
    
    armor_id = character['equipped_armor']
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip armor.")
    
    # Add armor back to inventory
    character['inventory'].append(armor_id)
    
    # Clear equipped armor
    character['equipped_armor'] = None
    
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    
    # Get item cost
    cost = item_data.get('cost', 0)
    
    # Check if character has enough gold
    if character['gold'] < cost:
        raise InsufficientResourcesError(
            f"Not enough gold! Need {cost}, have {character['gold']}"
        )
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot purchase item.")
    
    # Subtract gold
    character['gold'] -= cost
    
    # Add item to inventory
    add_item_to_inventory(character, item_id)
    
    return True


def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    
    # Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Calculate sell price (half of purchase cost)
    cost = item_data.get('cost', 0)
    sell_price = cost // 2
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Add gold to character
    character['gold'] += sell_price
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    
    if ':' not in effect_string:
        return None
    
    parts = effect_string.split(':')
    stat_name = parts[0].strip()
    
    try:
        value = int(parts[1].strip())
        return (stat_name, value)
    except (ValueError, IndexError):
        return None


def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    
    stat_name = stat_name.lower()
    
    # Apply the stat modification
    if stat_name in character:
        character[stat_name] += value
        
        # Ensure health doesn't exceed max_health
        if stat_name == 'health' and 'max_health' in character:
            character['health'] = min(character['health'], character['max_health'])


def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    
    inventory = character.get('inventory', [])
    
    if not inventory:
        print("Inventory is empty!")
        return
    
    print("\n--- Inventory ---")
    print(f"Capacity: {len(inventory)}/{MAX_INVENTORY_SIZE}")
    
    # Count unique items
    item_counts = {}
    for item_id in inventory:
        if item_id not in item_counts:
            item_counts[item_id] = 0
        item_counts[item_id] += 1
    
    # Display items
    for item_id, count in sorted(item_counts.items()):
        item_data = item_data_dict.get(item_id, {})
        item_name = item_data.get('name', item_id)
        item_type = item_data.get('type', 'unknown')
        
        if count > 1:
            print(f"  • {item_name} ({item_type}) x{count}")
        else:
            print(f"  • {item_name} ({item_type})")
    
    # Display equipped items
    print("\n--- Equipment ---")
    if 'equipped_weapon' in character and character['equipped_weapon']:
        weapon_id = character['equipped_weapon']
        weapon_data = item_data_dict.get(weapon_id, {})
        weapon_name = weapon_data.get('name', weapon_id)
        print(f"  Weapon: {weapon_name}")
    else:
        print(f"  Weapon: None")
    
    if 'equipped_armor' in character and character['equipped_armor']:
        armor_id = character['equipped_armor']
        armor_data = item_data_dict.get(armor_id, {})
        armor_name = armor_data.get('name', armor_id)
        print(f"  Armor: {armor_name}")
    else:
        print(f"  Armor: None")
    
    print("-" * 30)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===\n")
    
    # Create test character
    test_char = {
        'name': 'TestHero',
        'inventory': [],
        'gold': 200,
        'health': 80,
        'max_health': 100,
        'strength': 15,
        'magic': 5,
        'equipped_weapon': None,
        'equipped_armor': None
    }
    
    # Create test items
    health_potion = {
        'item_id': 'health_potion',
        'name': 'Health Potion',
        'type': 'consumable',
        'effect': {'health': 20},
        'cost': 25,
        'description': 'Restores 20 health'
    }
    
    iron_sword = {
        'item_id': 'iron_sword',
        'name': 'Iron Sword',
        'type': 'weapon',
        'effect': {'strength': 5},
        'cost': 50,
        'description': 'A basic iron sword'
    }
    
    steel_armor = {
        'item_id': 'steel_armor',
        'name': 'Steel Armor',
        'type': 'armor',
        'effect': {'max_health': 20},
        'cost': 100,
        'description': 'Protective steel armor'
    }
    
    item_data_dict = {
        'health_potion': health_potion,
        'iron_sword': iron_sword,
        'steel_armor': steel_armor
    }
    
    # Test adding items
    print("Test 1: Adding Items to Inventory")
    print("-" * 40)
    try:
        add_item_to_inventory(test_char, 'health_potion')
        print(f"✓ Added health potion")
        print(f"  Inventory: {test_char['inventory']}\n")
    except InventoryFullError as e:
        print(f"✗ {e}\n")
    
    # Test item count
    print("Test 2: Counting Items")
    print("-" * 40)
    add_item_to_inventory(test_char, 'health_potion')
    count = count_item(test_char, 'health_potion')
    print(f"✓ Health potion count: {count}\n")
    
    # Test using consumable
    print("Test 3: Using Consumable Item")
    print("-" * 40)
    print(f"  Health before: {test_char['health']}")
    try:
        result = use_item(test_char, 'health_potion', health_potion)
        print(f"✓ {result}")
        print(f"  Health after: {test_char['health']}")
        print(f"  Inventory: {test_char['inventory']}\n")
    except ItemNotFoundError as e:
        print(f"✗ {e}\n")
    
    # Test purchasing
    print("Test 4: Purchasing Items")
    print("-" * 40)
    print(f"  Gold before: {test_char['gold']}")
    try:
        purchase_item(test_char, 'iron_sword', iron_sword)
        print(f"✓ Purchased Iron Sword")
        print(f"  Gold after: {test_char['gold']}")
        print(f"  Inventory: {test_char['inventory']}\n")
    except (InsufficientResourcesError, InventoryFullError) as e:
        print(f"✗ {e}\n")
    
    # Test equipping weapon
    print("Test 5: Equipping Weapon")
    print("-" * 40)
    print(f"  Strength before: {test_char['strength']}")
    try:
        result = equip_weapon(test_char, 'iron_sword', iron_sword)
        print(f"✓ {result}")
        print(f"  Strength after: {test_char['strength']}")
        print(f"  Equipped: {test_char.get('equipped_weapon')}\n")
    except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
        print(f"✗ {e}\n")
    
    # Test purchasing armor
    print("Test 6: Purchasing and Equipping Armor")
    print("-" * 40)
    print(f"  Max health before: {test_char['max_health']}")
    try:
        purchase_item(test_char, 'steel_armor', steel_armor)
        print(f"✓ Purchased Steel Armor")
        result = equip_armor(test_char, 'steel_armor', steel_armor)
        print(f"✓ {result}")
        print(f"  Max health after: {test_char['max_health']}\n")
    except (InsufficientResourcesError, InventoryFullError, ItemNotFoundError, InvalidItemTypeError) as e:
        print(f"✗ {e}\n")
    
    # Test selling
    print("Test 7: Selling Items")
    print("-" * 40)
    test_char['inventory'].append('health_potion')
    print(f"  Gold before: {test_char['gold']}")
    try:
        gold_received = sell_item(test_char, 'health_potion', health_potion)
        print(f"✓ Sold Health Potion for {gold_received} gold")
        print(f"  Gold after: {test_char['gold']}\n")
    except ItemNotFoundError as e:
        print(f"✗ {e}\n")
    
    # Test inventory space
    print("Test 8: Inventory Space")
    print("-" * 40)
    space = get_inventory_space_remaining(test_char)
    print(f"✓ Inventory space remaining: {space}/{MAX_INVENTORY_SIZE}\n")
    
    # Test display inventory
    print("Test 9: Display Inventory")
    print("-" * 40)
    display_inventory(test_char, item_data_dict)
    
    print("\n=== INVENTORY SYSTEM TESTS COMPLETE ===")