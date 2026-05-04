"""
src/sound.py – Správce zvuků.
Generuje zvuky procedurálně přes numpy + pygame.sndarray,
takže nepotřebujeme žádné externí .wav soubory.
"""
 
import pygame
import numpy as np
 
 
def _make_sound(samples: np.ndarray, volume: float = 0.5) -> pygame.mixer.Sound:
    samples = np.clip(samples * volume, -1.0, 1.0)
    buf = (samples * 32767).astype(np.int16)
    stereo = np.column_stack([buf, buf])
    return pygame.sndarray.make_sound(stereo)
 
 
def _sine(freq, duration, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)
 
 
def _noise(duration, sr=44100):
    return np.random.uniform(-1, 1, int(sr * duration))
 
 
def _envelope(sig, attack=0.01, decay=0.1, sustain=0.6, release=0.1):
    n = len(sig)
    env = np.ones(n)
    a = int(n * attack)
    d = int(n * decay)
    r = int(n * release)
    s_start = a + d
    s_end = n - r
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if d > 0:
        env[a:a+d] = np.linspace(1, sustain, d)
    env[s_start:s_end] = sustain
    if r > 0:
        env[s_end:] = np.linspace(sustain, 0, len(env[s_end:]))
    return sig * env
 
 
class SoundManager:
    """
    Centrální správce zvuků.
    Volá se jako singleton: SoundManager.instance()
    """
    _instance = None
 
    def __init__(self, volume: int = 70):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._volume = volume / 100
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._generate_all()
 
    @classmethod
    def instance(cls, volume: int = 70):
        if cls._instance is None:
            cls._instance = cls(volume)
        return cls._instance
 
    def set_volume(self, volume: int):
        self._volume = volume / 100
        for s in self._sounds.values():
            s.set_volume(self._volume)
 
    # ------------------------------------------------------------------
    # Generování zvuků
    # ------------------------------------------------------------------
    def _generate_all(self):
        sr = 44100
 
        # Výstřel luku – krátký "fwoosh"
        t = np.linspace(0, 0.12, int(sr * 0.12))
        arrow = _noise(0.12) * np.exp(-30 * t)
        self._sounds["arrow"] = _make_sound(_envelope(arrow, 0.005, 0.05, 0.3, 0.05), self._volume)
 
        # Výbuch děla – basový "boom"
        t = np.linspace(0, 0.35, int(sr * 0.35))
        boom = (_sine(80, 0.35) * 0.6 + _noise(0.35) * 0.4) * np.exp(-8 * t)
        self._sounds["cannon"] = _make_sound(_envelope(boom, 0.005, 0.1, 0.4, 0.15), self._volume)
 
        # Mrazivá střela – ledový "shink"
        freeze = _sine(1200, 0.18) * 0.5 + _sine(900, 0.18) * 0.3
        t = np.linspace(0, 0.18, int(sr * 0.18))
        freeze *= np.exp(-12 * t)
        self._sounds["freeze"] = _make_sound(_envelope(freeze, 0.01, 0.05, 0.5, 0.1), self._volume)
 
        # Nepřítel zemřel – "splat"
        t = np.linspace(0, 0.2, int(sr * 0.2))
        death = _noise(0.2) * np.exp(-15 * t)
        self._sounds["enemy_die"] = _make_sound(_envelope(death, 0.002, 0.05, 0.2, 0.1), self._volume * 0.7)
 
        # Postavení věže – pozitivní "ding"
        place = _sine(520, 0.25) * 0.5 + _sine(780, 0.15) * 0.3
        t = np.linspace(0, 0.25, int(sr * 0.25))
        place *= np.exp(-10 * t)
        self._sounds["place_tower"] = _make_sound(place, self._volume)
 
        # Začátek vlny – dramatický "whoosh"
        t = np.linspace(0, 0.5, int(sr * 0.5))
        freqs = np.linspace(200, 600, int(sr * 0.5))
        wave_snd = np.sin(2 * np.pi * freqs * t / sr * np.arange(int(sr * 0.5)))
        wave_snd = wave_snd * np.exp(-4 * t)
        self._sounds["wave_start"] = _make_sound(_envelope(wave_snd, 0.05, 0.1, 0.5, 0.2), self._volume)
 
        # Ztráta života – nízký "thud"
        t = np.linspace(0, 0.3, int(sr * 0.3))
        life = (_sine(120, 0.3) * 0.7 + _noise(0.3) * 0.3) * np.exp(-10 * t)
        self._sounds["lose_life"] = _make_sound(life, self._volume)
 
        # Výhra – fanfára
        notes = [523, 659, 784, 1047]
        parts = []
        for n in notes:
            s = _sine(n, 0.15)
            t = np.linspace(0, 0.15, len(s))
            parts.append(s * np.exp(-5 * t))
        win = np.concatenate(parts)
        self._sounds["win"] = _make_sound(win, self._volume)
 
        # Prohra – smutný sestup
        notes_down = [523, 440, 349, 262]
        parts = []
        for n in notes_down:
            s = _sine(n, 0.18)
            t = np.linspace(0, 0.18, len(s))
            parts.append(s * np.exp(-4 * t))
        lose = np.concatenate(parts)
        self._sounds["lose"] = _make_sound(lose, self._volume)
 
    def play(self, name: str):
        if name in self._sounds:
            self._sounds[name].play()