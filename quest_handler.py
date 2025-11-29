"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Complete Implementation

Name: Charlestone Mayenga

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists, level requirement, prerequisites, not already done/active
    # Add to character['active_quests']
    
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    quest = quest_data_dict[quest_id]
    
    if quest_id in character.get('completed_quests', []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed")
    
    if quest_id in character.get('active_quests', []):
        return True
    
    required_level = quest.get('required_level', 1)
    if character['level'] < required_level:
        raise InsufficientLevelError(
            f"Character level {character['level']} below required {required_level}"
        )
    
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if prerequisite not in character.get('completed_quests', []):
            raise QuestRequirementsNotMetError(f"Must complete '{prerequisite}' first")
    
    if 'active_quests' not in character:
        character['active_quests'] = []
    character['active_quests'].append(quest_id)
    
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists and is active, award rewards, move to completed
    
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    quest = quest_data_dict[quest_id]
    
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    xp_reward = quest.get('reward_xp', 0)
    gold_reward = quest.get('reward_gold', 0)
    
    character['gold'] += gold_reward
    character['active_quests'].remove(quest_id)
    
    if 'completed_quests' not in character:
        character['completed_quests'] = []
    character['completed_quests'].append(quest_id)
    
    return {
        'quest_id': quest_id,
        'quest_title': quest.get('title', quest_id),
        'xp_reward': xp_reward,
        'gold_reward': gold_reward
    }


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    
    active_quests = []
    for quest_id in character.get('active_quests', []):
        if quest_id in quest_data_dict:
            active_quests.append(quest_data_dict[quest_id])
    
    return active_quests


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    
    completed_quests = []
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            completed_quests.append(quest_data_dict[quest_id])
    
    return completed_quests


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    
    available = []
    
    for quest_id, quest in quest_data_dict.items():
        if quest_id in character.get('completed_quests', []):
            continue
        if quest_id in character.get('active_quests', []):
            continue
        
        required_level = quest.get('required_level', 1)
        if character['level'] < required_level:
            continue
        
        prerequisite = quest.get('prerequisite', 'NONE')
        if prerequisite != 'NONE':
            if prerequisite not in character.get('completed_quests', []):
                continue
        
        available.append(quest)
    
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    
    return quest_id in character.get('completed_quests', [])


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    
    return quest_id in character.get('active_quests', [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    if quest_id in character.get('completed_quests', []):
        return False
    
    if quest_id in character.get('active_quests', []):
        return False
    
    required_level = quest.get('required_level', 1)
    if character['level'] < required_level:
        return False
    
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if prerequisite not in character.get('completed_quests', []):
            return False
    
    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    chain = []
    current_id = quest_id
    visited = set()
    
    while current_id is not None:
        if current_id in visited:
            break
        visited.add(current_id)
        
        if current_id not in quest_data_dict:
            break
        
        chain.insert(0, current_id)
        
        quest = quest_data_dict[current_id]
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite == 'NONE':
            break
        
        current_id = prerequisite
    
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    
    if not quest_data_dict:
        return 0.0
    
    total_quests = len(quest_data_dict)
    completed_quests = len(character.get('completed_quests', []))
    
    percentage = (completed_quests / total_quests) * 100
    return percentage


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    
    total_xp = 0
    total_gold = 0
    
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get('reward_xp', 0)
            total_gold += quest.get('reward_gold', 0)
    
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    
    quests = []
    
    for quest_id, quest in quest_data_dict.items():
        required_level = quest.get('required_level', 1)
        if min_level <= required_level <= max_level:
            quests.append(quest)
    
    return quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    
    print(f"\n{'=' * 50}")
    print(f"=== {quest_data.get('title', 'Unknown Quest')} ===")
    print(f"{'=' * 50}")
    print(f"\nDescription: {quest_data.get('description', 'No description')}")
    print(f"\nRequirements:")
    print(f"  Level: {quest_data.get('required_level', 1)}")
    
    prerequisite = quest_data.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        print(f"  Prerequisite: {prerequisite}")
    
    print(f"\nRewards:")
    print(f"  Experience: {quest_data.get('reward_xp', 0)} XP")
    print(f"  Gold: {quest_data.get('reward_gold', 0)} Gold")
    print(f"\n{'=' * 50}\n")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    
    if not quest_list:
        print("\nNo quests to display.")
        return
    
    print(f"\n{'=' * 60}")
    print(f"{'Title':<25} {'Level':<10} {'XP':<10} {'Gold':<10}")
    print(f"{'=' * 60}")
    
    for quest in quest_list:
        title = quest.get('title', 'Unknown')[:23]
        level = quest.get('required_level', 1)
        xp = quest.get('reward_xp', 0)
        gold = quest.get('reward_gold', 0)
        
        print(f"{title:<25} {level:<10} {xp:<10} {gold:<10}")
    
    print(f"{'=' * 60}\n")


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print(f"\n{'=' * 50}")
    print("QUEST PROGRESS")
    print(f"{'=' * 50}")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {percentage:.1f}%")
    print(f"\nTotal Rewards Earned:")
    print(f"  Experience: {rewards['total_xp']} XP")
    print(f"  Gold: {rewards['total_gold']} Gold")
    print(f"{'=' * 50}\n")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    
    for quest_id, quest in quest_data_dict.items():
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite != 'NONE':
            if prerequisite not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Quest '{quest_id}' has invalid prerequisite '{prerequisite}'"
                )
    
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===\n")
    
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        },
        'second_quest': {
            'quest_id': 'second_quest',
            'title': 'Next Challenge',
            'description': 'Take on a greater challenge',
            'reward_xp': 150,
            'reward_gold': 75,
            'required_level': 3,
            'prerequisite': 'first_quest'
        },
        'dragon_quest': {
            'quest_id': 'dragon_quest',
            'title': 'Slay the Dragon',
            'description': 'The ultimate challenge',
            'reward_xp': 500,
            'reward_gold': 250,
            'required_level': 6,
            'prerequisite': 'second_quest'
        }
    }
    
    print("Test 1: Accept Quest")
    print("-" * 40)
    try:
        result = accept_quest(test_char, 'first_quest', test_quests)
        print(f"✓ Quest accepted!")
        print(f"  Active: {test_char['active_quests']}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    print("Test 2: Complete Quest")
    print("-" * 40)
    try:
        result = complete_quest(test_char, 'first_quest', test_quests)
        print(f"✓ Completed: {result['quest_title']}")
        print(f"  Gold: {test_char['gold']}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    print("Test 3: Level Requirement")
    print("-" * 40)
    try:
        accept_quest(test_char, 'second_quest', test_quests)
        print(f"✗ Should have failed!\n")
    except InsufficientLevelError as e:
        print(f"✓ Correctly blocked: {e}\n")
    
    print("Test 4: Prerequisite Chain")
    print("-" * 40)
    try:
        chain = get_quest_prerequisite_chain('dragon_quest', test_quests)
        print(f"✓ Chain: {chain}\n")
    except QuestNotFoundError as e:
        print(f"✗ Error: {e}\n")
    
    print("Test 5: Quest Statistics")
    print("-" * 40)
    percentage = get_quest_completion_percentage(test_char, test_quests)
    print(f"✓ Completion: {percentage:.1f}%\n")
    
    print("=== QUEST HANDLER TESTS COMPLETE ===")