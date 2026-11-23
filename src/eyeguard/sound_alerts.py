"""Web Audio API synthesis for zero-dependency clinical chimes and notifications."""

from __future__ import annotations

import streamlit.components.v1 as components


def get_web_audio_script(sound_type: str = "focus_complete") -> str:
    """Return inline JavaScript for Web Audio synthetic chimes."""
    if sound_type == "break_complete":
        # Two-tone rising chime (E5 -> G5)
        frequencies = "[659.25, 783.99]"
        durations = "[0.2, 0.4]"
    elif sound_type == "micro_ping":
        # Gentle single ping (A5)
        frequencies = "[880.0]"
        durations = "[0.25]"
    elif sound_type == "alpha_focus":
        # Soothing 432Hz harmonic tone for deep ocular relaxation & focused presence
        frequencies = "[432.0, 540.0]"
        durations = "[1.2, 1.8]"
    else:  # focus_complete
        # Harmonious dual bell chime (C5 -> E5)
        frequencies = "[523.25, 659.25]"
        durations = "[0.25, 0.5]"

    return f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            
            const freqs = {frequencies};
            const durs = {durations};
            let startTime = ctx.currentTime + 0.05;

            freqs.forEach((freq, idx) => {{
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = "sine";
                osc.frequency.setValueAtTime(freq, startTime);
                
                // Exponential decay envelope
                gain.gain.setValueAtTime(0.001, startTime);
                gain.gain.exponentialRampToValueAtTime(0.3, startTime + 0.03);
                gain.gain.exponentialRampToValueAtTime(0.0001, startTime + durs[idx]);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.start(startTime);
                osc.stop(startTime + durs[idx]);
                startTime += durs[idx] * 0.7;
            }});
        }} catch(e) {{
            console.warn("Web Audio chime could not play:", e);
        }}
    }})();
    </script>
    """


def trigger_audio_chime(sound_type: str = "focus_complete") -> None:
    """Trigger a synthetic browser chime safely in Streamlit."""
    html_code = get_web_audio_script(sound_type)
    components.html(html_code, height=0, width=0)
