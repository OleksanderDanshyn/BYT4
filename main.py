import random
import streamlit as st
from entities.enemy import Enemy
from entities.player import Player

if "player" not in st.session_state:
    st.session_state.player = Player("Hero", 30, 100)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_enemy" not in st.session_state:
    st.session_state.current_enemy = None

st.set_page_config(page_title="RPG Button Chat", layout="wide")
st.title("💬 RPG Button Chat Interface")


def list_commands():
    return "Available commands: " + ", ".join(current_commands())


def enemy_generator():
    from items.weapon import Weapon
    from items.armor import Armor
    from items.potion import Potion
    from items.food import Food

    drop_options = [
        Weapon(
            name="Iron Sword",
            description="A sturdy iron blade",
            buyable=True,
            sell_price=random.randint(20, 40),
            damage=random.randint(5, 10),
            type="sword"
        ),
        Armor(
            toughness=random.randint(3, 8),
            name="Leather Armor",
            description="Light protective gear",
            buyable=True,
            sell_price=random.randint(15, 30)
        ),
        Potion(
            name="Health Potion",
            description="Restores health",
            buyable=True,
            sell_price=random.randint(10, 20),
            number_of_uses=1,
            duration=0,
            power=random.randint(10, 20)
        ),
        Food(
            saturation=random.randint(5, 15),
            name="Bread",
            description="Simple food",
            buyable=True,
            sell_price=random.randint(5, 10),
            number_of_uses=1
        )
    ]
    drop = random.choice(drop_options)

    names = ["goblin", "dragon", "skeleton", "orc", "troll"]
    name = random.choice(names)

    health = random.randint(10, 25)
    damage = random.randint(3, 8)
    return Enemy(drop, name, health, damage)


def enemy_attack():
    enemy = st.session_state.current_enemy
    if not enemy:
        return ""

    damage = enemy.damage

    if st.session_state.player.equipped_armor:
        damage = max(1, damage - st.session_state.player.equipped_armor.toughness)

    st.session_state.player.health -= damage

    msg = f"\n💥 {enemy.name} attacks you for {damage} damage!"

    if st.session_state.player.health <= 0:
        st.session_state.player.health = 0
        msg += "\n☠️ You have been defeated!"
        st.session_state.current_enemy = None

    return msg


def battle():
    enemy = enemy_generator()
    st.session_state.current_enemy = enemy
    return f"⚔️ {st.session_state.player.name} is battling {enemy.name} (HP: {enemy.health}, DMG: {enemy.damage})!"


def use_item():
    if st.session_state.player.inventory.is_empty():
        return "Your inventory is empty!"
    return "Select an item from the inventory panel to use it."


def attack():
    enemy = st.session_state.current_enemy
    if not enemy:
        return "No enemy to attack!"

    base_damage = random.randint(1, 5)
    if st.session_state.player.equipped_weapon:
        base_damage += st.session_state.player.equipped_weapon.damage

    damage = base_damage

    if damage > enemy.health:
        enemy.health = 0
    else:
        enemy.health -= damage

    msg = f"🗡️ You attacked {enemy.name} for {damage} damage. Enemy HP: {max(enemy.health, 0)}."

    if enemy.health <= 0:
        st.session_state.player.slay_monster(enemy)
        st.session_state.current_enemy = None
        msg += f"\n🎉 {enemy.name} defeated!"
#Oleg
        success, message = st.session_state.player.inventory.add_item(enemy.drop)
        msg += f"\n{message}"
    else:
        msg += enemy_attack()

    return msg


def run():
    if st.session_state.current_enemy:
        st.session_state.current_enemy = None
        return "🏃 You ran away!"
    return "No enemy to run from."


def greet():
    return "👋 Hello! Welcome to the game."


def current_commands():
    if st.session_state.current_enemy:
        return ["attack", "use", "run", "list"]
    return ["greet", "list", "battle", "use"]


COMMANDS = {
    "greet": greet,
    "list": list_commands,
    "battle": battle,
    "attack": attack,
    "run": run,
    "use": use_item
}

COMMAND_ICONS = {
    "greet": "👋",
    "list": "📋",
    "battle": "⚔️",
    "attack": "🗡️",
    "run": "🏃",
    "use": "🎒"
}

st.markdown("""
<style>
    .stButton button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 500;
    }

    .item-button {
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Commands")
for cmd in current_commands():
    icon = COMMAND_ICONS.get(cmd, "🎮")
    if st.sidebar.button(f"{icon} {cmd.capitalize()}", key=cmd, use_container_width=True):
        response = COMMANDS[cmd]()
        st.session_state.messages.append({"role": "user", "content": cmd})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

st.sidebar.markdown("---")
with st.sidebar.expander(
        f"🎒 Inventory ({len(st.session_state.player.inventory)}/{st.session_state.player.inventory.max_size})",
        expanded=False):
    if st.session_state.player.inventory.is_empty():
        st.write("*Empty*")
    else:
        for idx, item in enumerate(st.session_state.player.inventory):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item.name}**")
                st.caption(f"_{item.description}_")

                if hasattr(item, 'damage'):  # Weapon
                    st.caption(f"⚔️ Damage: {item.damage} | Type: {item.type}")
                elif hasattr(item, 'toughness'):  # Armor
                    st.caption(f"🛡️ Toughness: {item.toughness}")
                elif hasattr(item, 'power'):  # Potion
                    st.caption(f"❤️ Power: {item.power} | Uses: {item.number_of_uses}")
                elif hasattr(item, 'saturation'):  # Food
                    st.caption(f"🍖 Saturation: {item.saturation}")

                st.caption(f"💰 Sell: {item.sell_price}g")

            with col2:
                if st.button("Use", key=f"use_item_{idx}", use_container_width=True):
                    item_to_use = list(st.session_state.player.inventory)[idx]

                    if hasattr(item_to_use, 'damage'):
                        st.session_state.player.equip_weapon(item_to_use)
                        msg = f"⚔️ Equipped {item_to_use.name}!"

                    elif hasattr(item_to_use, 'toughness'):
                        st.session_state.player.equip_armor(item_to_use)
                        msg = f"🛡️ Equipped {item_to_use.name}!"
#Oleg
                    elif hasattr(item_to_use, 'power'):
                        msg = item_to_use.use_on_player(st.session_state.player)

                        if item_to_use.number_of_uses <= 0:
                            st.session_state.player.inventory.remove_item(item_to_use)

                        active_effects = st.session_state.player.get_active_effect_names()

                        if active_effects:
                            msg += f"\n✨ Active effects: {', '.join(active_effects)}"

                        if st.session_state.current_enemy:
                            msg += enemy_attack()

                    elif hasattr(item_to_use, 'saturation'):
                        st.session_state.player.hunger = min(
                            st.session_state.player.hunger + item_to_use.saturation,
                            10
                        )
                        st.session_state.player.inventory.remove_item(item_to_use)
                        msg = f"🍖 Ate {item_to_use.name}! Restored {item_to_use.saturation} hunger."

                        if st.session_state.current_enemy:
                            msg += enemy_attack()

                    else:
                        msg = f"Used {item_to_use.name}!"

                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"use {item_to_use.name}"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": msg
                    })
                    st.rerun()

            with col3:
                if st.button("Drop", key=f"drop_item_{idx}", use_container_width=True):
                    item_to_drop = list(st.session_state.player.inventory)[idx]

                    if st.session_state.player.equipped_weapon == item_to_drop:
                        st.session_state.player.equipped_weapon = None
                    if st.session_state.player.equipped_armor == item_to_drop:
                        st.session_state.player.equipped_armor = None

                    st.session_state.player.inventory.remove_item(item_to_drop)
                    msg = f"🗑️ Dropped {item_to_drop.name}!"

                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"drop {item_to_drop.name}"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": msg
                    })
                    st.rerun()

            st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Player Stats")
st.sidebar.write(f"**Name:** {st.session_state.player.name}")

health_percentage = (st.session_state.player.health / st.session_state.player.max_health) * 100
health_color = "🟢" if health_percentage > 60 else "🟡" if health_percentage > 30 else "🔴"
st.sidebar.write(f"**Health:** {health_color} {st.session_state.player.health}/{st.session_state.player.max_health}")

st.sidebar.write(f"**Hunger:** 🍖 {st.session_state.player.hunger}/10")
st.sidebar.write(f"**Money:** 💰 {st.session_state.player.money}g")

st.sidebar.markdown("**Equipment:**")
if st.session_state.player.equipped_weapon:
    st.sidebar.write(
        f"⚔️ {st.session_state.player.equipped_weapon.name} (DMG: {st.session_state.player.equipped_weapon.damage})")
else:
    st.sidebar.write("⚔️ No weapon")

if st.session_state.player.equipped_armor:
    st.sidebar.write(
        f"🛡️ {st.session_state.player.equipped_armor.name} (DEF: {st.session_state.player.equipped_armor.toughness})")
else:
    st.sidebar.write("🛡️ No armor")

st.sidebar.write(f"**Monsters Slain:** 💀 {len(st.session_state.player.kills)}")

active_effects = st.session_state.player.get_active_effect_names()
if active_effects:
    st.sidebar.markdown("**Active Effects:**")
    for effect in active_effects:
        st.sidebar.write(f"✨ {effect}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])