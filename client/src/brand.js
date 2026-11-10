import { mdiPopcorn } from '@quasar/extras/mdi-v7';

// The site name, used in the header and browser tab titles
export const APP_NAME = 'PopRank';

// 'The Batman' -> 'The Batman | PopRank'; no argument -> 'PopRank'
export function pageTitle(part) {
  return part ? `${part} | ${APP_NAME}` : APP_NAME;
}

// Popcorn bucket in the logo. Ratings use a single kernel (assets/popcorn.svg)
export const LOGO_ICON = mdiPopcorn;
