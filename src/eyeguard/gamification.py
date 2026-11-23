"""AsthenoZero - Gamification, OcuCoins Credit Economy & Streak Protocol.

Manages user habit streaks, OcuCoins credits, streak shields, and the
Strict Clinical Ocular Rehabilitation Protocol enforced when credits are depleted.
"""

from __future__ import annotations

import streamlit as st
from datetime import datetime, date

# Reward & Cost Constants
REWARD_DIARY_ENTRY = 15
REWARD_TIMER_COMPLETE = 20
REWARD_EXERCISE_COMPLETE = 25
REWARD_BLINK_DIAGNOSTIC = 35
REWARD_DAILY_STREAK = 10
REWARD_STRICT_GRADUATION = 60

COST_REPAIR_STREAK = 50
COST_BUY_SHIELD = 40


def ensure_gamification_state() -> None:
    """Initializes gamification session state keys if not already present."""
    st.session_state.setdefault("ocu_coins", 100)
    st.session_state.setdefault("daily_streak", 3)
    st.session_state.setdefault("streak_shields", 1)
    st.session_state.setdefault("streak_broken", False)
    st.session_state.setdefault("strict_rehab_mode", False)
    st.session_state.setdefault(
        "strict_rehab_tasks",
        {
            "exercise": False,
            "timer": False,
            "diagnostic": False,
        },
    )
    st.session_state.setdefault("last_activity_date", str(date.today()))
    st.session_state.setdefault("coins_earned_today", 0)


def award_coins(amount: int, reason: str) -> None:
    """Awards OcuCoins, logs the transaction, and triggers a visual notification."""
    ensure_gamification_state()
    st.session_state["ocu_coins"] = st.session_state.get("ocu_coins", 100) + amount
    st.session_state["coins_earned_today"] = st.session_state.get("coins_earned_today", 0) + amount
    st.toast(f"🪙 +{amount} OcuCoins earned! ({reason})", icon="🪙")


def spend_coins(amount: int, reason: str) -> bool:
    """Attempts to deduct OcuCoins. Returns True if successful, False if insufficient balance."""
    ensure_gamification_state()
    current = st.session_state.get("ocu_coins", 0)
    if current >= amount:
        st.session_state["ocu_coins"] = current - amount
        st.toast(f"Spent {amount} OcuCoins for: {reason}", icon="🪙")
        return True
    return False


def break_streak_simulation() -> None:
    """Simulates an unlogged or missed day to test the streak recovery flow."""
    ensure_gamification_state()
    shields = st.session_state.get("streak_shields", 0)
    if shields > 0:
        st.session_state["streak_shields"] = shields - 1
        st.toast("🛡️ Streak Shield activated! Your streak was preserved automatically.", icon="🛡️")
        return

    st.session_state["streak_broken"] = True
    coins = st.session_state.get("ocu_coins", 0)
    if coins < COST_REPAIR_STREAK:
        st.session_state["strict_rehab_mode"] = True
        st.session_state["strict_rehab_tasks"] = {
            "exercise": False,
            "timer": False,
            "diagnostic": False,
        }
        st.toast("🚨 Insufficient OcuCoins! Strict Rehabilitation Mode engaged.", icon="⚠️")
    else:
        st.toast("⚠️ Streak broken! Use your OcuCoins vault to repair it.", icon="⚠️")


def repair_streak_with_coins() -> bool:
    """Repairs a broken streak using coins."""
    ensure_gamification_state()
    if spend_coins(COST_REPAIR_STREAK, "Streak Repair"):
        st.session_state["streak_broken"] = False
        st.session_state["strict_rehab_mode"] = False
        st.toast("✅ Streak successfully repaired and restored!", icon="🔥")
        return True
    st.error("❌ Insufficient OcuCoins to repair streak! You must complete the Strict Rehabilitation Challenge.")
    return False


def buy_shield() -> bool:
    """Purchases a streak shield using coins."""
    ensure_gamification_state()
    if spend_coins(COST_BUY_SHIELD, "Streak Shield Purchase"):
        st.session_state["streak_shields"] = st.session_state.get("streak_shields", 0) + 1
        st.toast("🛡️ Streak Shield purchased! Active in vault.", icon="🛡️")
        return True
    st.error("❌ Insufficient OcuCoins (Requires 40 🪙). Earn more coins by completing exercises and timers!")
    return False


def notify_activity_completed(activity_type: str) -> None:
    """Updates gamification state when the user completes an ergonomic task.

    activity_type: 'exercise' | 'timer' | 'diagnostic' | 'diary'
    """
    ensure_gamification_state()

    # Award base coins
    if activity_type == "diary":
        award_coins(REWARD_DIARY_ENTRY, "Habit Diary Logged")
    elif activity_type == "timer":
        award_coins(REWARD_TIMER_COMPLETE, "20-20-20 Micro-Break Done")
    elif activity_type == "exercise":
        award_coins(REWARD_EXERCISE_COMPLETE, "Vision Gym Exercise Done")
    elif activity_type == "diagnostic":
        award_coins(REWARD_BLINK_DIAGNOSTIC, "60s Blink Diagnostic Done")

    # If in strict rehab mode, mark step as completed and check for graduation
    if st.session_state.get("strict_rehab_mode", False):
        tasks = st.session_state.get("strict_rehab_tasks", {})
        if activity_type in tasks:
            tasks[activity_type] = True
            st.session_state["strict_rehab_tasks"] = tasks

        # Check if all 3 strict requirements are met
        if tasks.get("exercise") and tasks.get("timer") and tasks.get("diagnostic"):
            st.session_state["streak_broken"] = False
            st.session_state["strict_rehab_mode"] = False
            st.session_state["daily_streak"] = st.session_state.get("daily_streak", 1) + 1
            award_coins(REWARD_STRICT_GRADUATION, "Strict Rehabilitation Graduation Bonus")
            st.balloons()
            st.success(
                "🎉 **STRICT REHABILITATION COMPLETE!** You fulfilled all clinical ocular recovery protocols. "
                "Your streak has been fully restored and +60 OcuCoins have been added to your vault!"
            )


def render_top_navbar_badges() -> str:
    """Generates HTML snippet for live Streak & Coin badges in the hero banner."""
    ensure_gamification_state()
    coins = st.session_state.get("ocu_coins", 0)
    streak = st.session_state.get("daily_streak", 0)
    shields = st.session_state.get("streak_shields", 0)
    broken = st.session_state.get("streak_broken", False)
    strict = st.session_state.get("strict_rehab_mode", False)

    if strict:
        streak_badge = '<span class="telemetry-pill" style="border-color:#EF4444; color:#F87171; background:rgba(239,68,68,0.18);">🚨 Strict Rehab Active</span>'
    elif broken:
        streak_badge = '<span class="telemetry-pill" style="border-color:#F59E0B; color:#FBBF24; background:rgba(245,158,11,0.18);">⚠️ Streak at Risk</span>'
    else:
        streak_badge = f'<span class="telemetry-pill active-cyan" style="font-weight:800;">🔥 Streak: {streak} Days</span>'

    shield_badge = f'<span class="telemetry-pill" style="border-color:#38BDF8; color:#7DD3FC;">🛡️ Shields: {shields}</span>'
    coin_badge = f'<span class="telemetry-pill active-emerald" style="font-weight:800; border-color:#10B981;">🪙 {coins} OcuCoins</span>'

    return f"{streak_badge} {coin_badge} {shield_badge}"


def render_strict_rehab_alert() -> None:
    """Renders prominent visual banner when user is in Strict Rehabilitation Mode or Streak is broken."""
    ensure_gamification_state()
    if not st.session_state.get("streak_broken", False):
        return

    is_strict = st.session_state.get("strict_rehab_mode", False)
    coins = st.session_state.get("ocu_coins", 0)

    if is_strict or coins < COST_REPAIR_STREAK:
        tasks = st.session_state.get("strict_rehab_tasks", {})
        t1 = "✅" if tasks.get("exercise") else "⭕"
        t2 = "✅" if tasks.get("timer") else "⭕"
        t3 = "✅" if tasks.get("diagnostic") else "⭕"

        st.html(
            f"""<div style="background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(15,23,42,0.95)); border: 2px solid #EF4444; border-radius: 14px; padding: 18px 24px; margin-bottom: 24px; box-shadow: 0 0 25px rgba(239,68,68,0.25);">
<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
    <div>
        <div style="font-size:1.15rem; font-weight:800; color:#FCA5A5; display:flex; align-items:center; gap:8px;">
            🚨 STRICT CLINICAL REHABILITATION PROTOCOL ACTIVE
        </div>
        <div style="font-size:0.88rem; color:#E2E8F0; margin-top:4px; max-width:800px; line-height:1.6;">
            Your daily streak has lapsed and you have depleted your OcuCoins vault ({coins} coins remaining).
            Under clinical protocol, you cannot purchase a recovery bypass. To unfreeze and restore your 
            <strong>{st.session_state.get('daily_streak', 1)}-Day Streak</strong>, you must complete all 3 therapeutic recovery tasks:
        </div>
    </div>
    <div style="background:rgba(0,0,0,0.4); padding:10px 16px; border-radius:10px; border:1px solid rgba(239,68,68,0.3); text-align:center;">
        <div style="font-size:0.75rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">Rehab Status</div>
        <div style="font-size:1.1rem; font-weight:800; color:#F87171;">FROZEN</div>
    </div>
</div>
<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:12px; margin-top:14px;">
    <div style="background:rgba(15,23,42,0.7); border:1px solid {'#10B981' if tasks.get('exercise') else 'rgba(255,255,255,0.1)'}; padding:10px 14px; border-radius:8px;">
        <span style="font-size:1.1rem;">{t1}</span> <strong style="color:#F8FAFC;">1. Eye Relaxation Drill</strong>
        <div style="font-size:0.78rem; color:#94A3B8; margin-top:2px;">Complete 1 exercise in Vision Gym tab</div>
    </div>
    <div style="background:rgba(15,23,42,0.7); border:1px solid {'#10B981' if tasks.get('timer') else 'rgba(255,255,255,0.1)'}; padding:10px 14px; border-radius:8px;">
        <span style="font-size:1.1rem;">{t2}</span> <strong style="color:#F8FAFC;">2. 20-20-20 Micro-Break</strong>
        <div style="font-size:0.78rem; color:#94A3B8; margin-top:2px;">Complete 1 break session in Rest Timer tab</div>
    </div>
    <div style="background:rgba(15,23,42,0.7); border:1px solid {'#10B981' if tasks.get('diagnostic') else 'rgba(255,255,255,0.1)'}; padding:10px 14px; border-radius:8px;">
        <span style="font-size:1.1rem;">{t3}</span> <strong style="color:#F8FAFC;">3. 60s Blink Diagnostic</strong>
        <div style="font-size:0.78rem; color:#94A3B8; margin-top:2px;">Complete 60s reading test in Blink Test tab</div>
    </div>
</div>
</div>"""
        )
    else:
        st.html(
            f"""<div style="background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(15,23,42,0.95)); border: 2px solid #F59E0B; border-radius: 14px; padding: 18px 24px; margin-bottom: 24px; box-shadow: 0 0 25px rgba(245,158,11,0.25);">
<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
    <div>
        <div style="font-size:1.15rem; font-weight:800; color:#FDE68A;">⚠️ DAILY STREAK AT RISK</div>
        <div style="font-size:0.88rem; color:#E2E8F0; margin-top:4px;">
            Your streak was broken! You can spend <strong>50 OcuCoins</strong> from your vault ({coins} available) to repair and protect your streak.
        </div>
    </div>
</div>
</div>"""
        )
        col_rep1, col_rep2 = st.columns([1, 2])
        with col_rep1:
            if st.button("🪙 Repair Streak (Cost: 50 OcuCoins)", type="primary", use_container_width=True):
                repair_streak_with_coins()
                st.rerun()


def render_gamification_sidebar() -> None:
    """Renders the Credit & Streak Vault in the sidebar."""
    ensure_gamification_state()
    coins = st.session_state.get("ocu_coins", 0)
    streak = st.session_state.get("daily_streak", 0)
    shields = st.session_state.get("streak_shields", 0)
    broken = st.session_state.get("streak_broken", False)
    is_strict = st.session_state.get("strict_rehab_mode", False)

    st.markdown("### 🏆 Streak & OcuCoins Vault")

    st.html(
        f"""<div class="clinical-card" style="padding:14px 16px !important; margin-bottom:12px !important; border-left: 4px solid #10B981 !important;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
    <span style="font-size:0.85rem; font-weight:700; color:#94A3B8;">OcuCoins Balance:</span>
    <span style="font-size:1.15rem; font-weight:800; color:#10B981;">🪙 {coins}</span>
</div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
    <span style="font-size:0.85rem; font-weight:700; color:#94A3B8;">Daily Habit Streak:</span>
    <span style="font-size:1.15rem; font-weight:800; color:{'#EF4444' if broken else '#38BDF8'};">🔥 {streak} Days</span>
</div>
<div style="display:flex; justify-content:space-between; align-items:center;">
    <span style="font-size:0.85rem; font-weight:700; color:#94A3B8;">Streak Shields:</span>
    <span style="font-size:1.15rem; font-weight:800; color:#38BDF8;">🛡️ {shields}</span>
</div>
</div>"""
    )

    with st.expander("🪙 Credit Economy & Vault Actions", expanded=broken or is_strict):
        st.markdown(
            """**Earn OcuCoins:**
- 📝 Log Daily Habit Diary: `+15 🪙`
- 🧘 Vision Gym Exercise: `+25 🪙`
- ⏱️ 20-20-20 Break Timer: `+20 🪙`
- 👁️ 60s Blink Diagnostic: `+35 🪙`
- 🎓 Strict Rehab Graduation: `+60 🪙`
"""
        )
        st.divider()

        if st.button("🛡️ Buy Streak Shield (40 🪙)", use_container_width=True, help="Auto-protects streak if you miss a day"):
            if buy_shield():
                st.rerun()

        if broken:
            if coins >= COST_REPAIR_STREAK:
                if st.button("🔄 Repair Streak (50 🪙)", type="primary", use_container_width=True):
                    repair_streak_with_coins()
                    st.rerun()
            else:
                st.warning("⚠️ Insufficient coins to repair streak! Follow Strict Rehabilitation Protocol.")

        st.caption("🧪 Evaluator / Test Controls:")
        test_col1, test_col2 = st.columns(2)
        with test_col1:
            if st.button("Simulate Missed Day", help="Breaks streak to test recovery flow", use_container_width=True):
                break_streak_simulation()
                st.rerun()
        with test_col2:
            if st.button("Drain Coins (Test 0 🪙)", help="Sets coins to 0 to test strict challenge", use_container_width=True):
                st.session_state["ocu_coins"] = 0
                st.session_state["streak_broken"] = True
                st.session_state["strict_rehab_mode"] = True
                st.toast("OcuCoins set to 0. Strict Rehabilitation mode engaged!", icon="⚠️")
                st.rerun()
