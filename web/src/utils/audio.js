import audioSrc from '../assets/UIZephyrThemeWindowOpen.wav';

let audio = new Audio(audioSrc);

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
