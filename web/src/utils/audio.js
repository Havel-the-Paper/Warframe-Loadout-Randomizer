const AUDIO_URL = '/audio/UIZephyrThemeWindowOpen.wav';

let audio = new Audio(AUDIO_URL);

export function playRollSound() {
  audio.currentTime = 0;
  audio.play().catch(() => {});
}

export function playClickSound() {
  audio.currentTime = 0;
  audio.play().catch(() => {});
}

export function playLockSound() {
  audio.currentTime = 0;
  audio.play().catch(() => {});
}

export function playRewardSound() {
  audio.currentTime = 0;
  audio.play().catch(() => {});
}
