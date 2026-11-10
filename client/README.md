# PopRank frontend

Vue 3 + Quasar app built with Vite. How to run the whole project (API, database, nginx) is in the [main README](../README.md).

## Commands

```sh
npm install
npm run dev      # dev server on port 3000
npm run build    # production build into dist/
npm run lint     # ESLint, fixes what it can
npm run format   # Prettier for src/
```

## Where things are

```
src/
  views/        pages the router opens
  components/   page content and shared pieces (MovieTile, PosterImage, PasswordInput…)
  styles/       all SCSS, one file per page or part, joined in main.scss
  assets/       images used from CSS (popcorn.svg)
  auth.js       tokens, current user, logIn()
  brand.js      site name, page titles, logo icon
  format.js     ratings, years, vote counts
  reveal.js     v-reveal: fade in on scroll (Motion)
public/         favicons
```
