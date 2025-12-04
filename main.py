import random
import streamlit as st
from entities.enemy import Enemy
from entities.player import Player

if "player" not in st.session_state:
    st.session_state.player = Player("Hero", 300, 100)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_enemy" not in st.session_state:
    st.session_state.current_enemy = None

st.set_page_config(page_title="RPG Button Chat", layout="wide")
st.title("💬 RPG Button Chat Interface")


def generate_unique_item_name(item, inventory):
    base_name = item.name
    counter = 1
    existing_names = [i.name for i in inventory]
    while base_name in existing_names:
        base_name = f"{item.name} #{counter}"
        counter += 1
    item.name = base_name
    return item


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


def apply_damage(player, damage):
    player.health = max(0, player.health - damage)
    if player.health == 0:
        handle_player_death()


def handle_player_death():
    msg = "☠️ You have died!\nGame will reset."
    st.session_state.player = Player("Hero", 300, 100)
    st.session_state.current_enemy = None
    st.session_state.messages = [{"role": "assistant", "content": msg}]
    st.rerun()


def enemy_attack():
    enemy = st.session_state.current_enemy
    if not enemy:
        return ""
    damage = enemy.damage
    if st.session_state.player.equipped_armor:
        damage = max(1, damage - st.session_state.player.equipped_armor.toughness)
    apply_damage(st.session_state.player, damage)
    return f"\n💥 {enemy.name} attacks you for {damage} damage!"


def battle():
    enemy = enemy_generator()
    st.session_state.current_enemy = enemy
    return f"⚔️ {st.session_state.player.name} is battling {enemy.name} (HP: {enemy.health}, DMG: {enemy.damage})!"


def attack():
    enemy = st.session_state.current_enemy
    if not enemy:
        return "No enemy to attack!"

    damage = random.randint(1, 5)
    if st.session_state.player.equipped_weapon:
        damage += st.session_state.player.equipped_weapon.damage

    enemy.health = max(0, enemy.health - damage)
    msg = f"🗡️ You attacked {enemy.name} for {damage} damage. Enemy HP: {enemy.health}."

    if enemy.health <= 0:
        st.session_state.current_enemy = None
        if enemy not in st.session_state.player.kills:
            st.session_state.player.kills.append(enemy)
        msg += f"\n🎉 {enemy.name} defeated!"

        if random.random() < 0.5 and enemy.drop is not None:
            if len(st.session_state.player.inventory) < st.session_state.player.inventory.max_size:
                item_to_add = generate_unique_item_name(enemy.drop, st.session_state.player.inventory)
                success, message = st.session_state.player.inventory.add_item(item_to_add)
                msg += f"\n{message}"
            else:
                gold_amount = enemy.drop.sell_price
                st.session_state.player.money += gold_amount
                msg += f"\n💰 Inventory full! Received {gold_amount}g instead."
        else:
            gold_amount = random.randint(10, 30)
            st.session_state.player.money += gold_amount
            msg += f"\n💰 You received {gold_amount}g!"

    else:
        msg += enemy_attack()

    return msg



def run():
    if st.session_state.current_enemy:
        st.session_state.current_enemy = None
        return "🏃 You ran away!"
    return "No enemy to run from."


def current_commands():
    return ["attack", "run"] if st.session_state.current_enemy else ["battle"]


COMMANDS = {"battle": battle, "attack": attack, "run": run}
COMMAND_ICONS = {"battle": "⚔️", "attack": "🗡️", "run": "🏃"}

st.markdown("""
<style>
.stButton button {width: 100%; height: 3.5rem; font-size: 1.1rem; font-weight: 500;}
.item-button {margin: 0.25rem 0;}
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
with st.sidebar.expander(f"🎒 Inventory ({len(st.session_state.player.inventory)}/{st.session_state.player.inventory.max_size})"):
    if st.session_state.player.inventory.is_empty():
        st.write("*Empty*")
    else:
        for idx, item in enumerate(st.session_state.player.inventory):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item.name}**")
                st.caption(f"_{item.description}_")
                if hasattr(item, "damage"):
                    st.caption(f"⚔️ Damage: {item.damage} | Type: {item.type}")
                elif hasattr(item, "toughness"):
                    st.caption(f"🛡️ Toughness: {item.toughness}")
                elif hasattr(item, "power"):
                    st.caption(f"❤️ Power: {item.power} | Uses: {item.number_of_uses}")
                elif hasattr(item, "saturation"):
                    st.caption(f"🍖 Saturation: {item.saturation}")
                st.caption(f"💰 Sell: {item.sell_price}g")
            with col2:
                if st.button("Use", key=f"use_item_{idx}", use_container_width=True):
                    if hasattr(item, "damage"):
                        st.session_state.player.equip_weapon(item)
                        msg = f"⚔️ Equipped {item.name}!"
                    elif hasattr(item, "toughness"):
                        st.session_state.player.equip_armor(item)
                        msg = f"🛡️ Equipped {item.name}!"
                    elif hasattr(item, "power"):
                        msg = item.use_on_player(st.session_state.player)
                        if item.number_of_uses <= 0:
                            st.session_state.player.inventory.remove_item(item)
                        if st.session_state.current_enemy:
                            msg += enemy_attack()
                    elif hasattr(item, "saturation"):
                        st.session_state.player.hunger = min(st.session_state.player.hunger + item.saturation, 10)
                        st.session_state.player.inventory.remove_item(item)
                        msg = f"🍖 Ate {item.name}! Restored {item.saturation} hunger."
                        if st.session_state.current_enemy:
                            msg += enemy_attack()
                    else:
                        msg = f"Used {item.name}!"
                    st.session_state.messages.append({"role": "user", "content": f"use {item.name}"})
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    st.rerun()
            with col3:
                if st.button("Drop", key=f"drop_item_{idx}", use_container_width=True):
                    if st.session_state.player.equipped_weapon == item:
                        st.session_state.player.equipped_weapon = None
                    if st.session_state.player.equipped_armor == item:
                        st.session_state.player.equipped_armor = None
                    st.session_state.player.inventory.remove_item(item)
                    msg = f"🗑️ Dropped {item.name}!"
                    st.session_state.messages.append({"role": "user", "content": f"drop {item.name}"})
                    st.session_state.messages.append({"role": "assistant", "content": msg})
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
st.sidebar.write(f"⚔️ {st.session_state.player.equipped_weapon.name} (DMG: {st.session_state.player.equipped_weapon.damage})" if st.session_state.player.equipped_weapon else "⚔️ No weapon")
st.sidebar.write(f"🛡️ {st.session_state.player.equipped_armor.name} (DEF: {st.session_state.player.equipped_armor.toughness})" if st.session_state.player.equipped_armor else "🛡️ No armor")
st.sidebar.write(f"**Monsters Slain:** 💀 {len(st.session_state.player.kills)}")
active_effects = st.session_state.player.get_active_effect_names()
if active_effects:
    st.sidebar.markdown("**Active Effects:**")
    for effect in active_effects:
        st.sidebar.write(f"✨ {effect}")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
