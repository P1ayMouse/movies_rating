import { createRouter, createWebHistory } from 'vue-router';
import { ensureUserLoaded, nextPath } from '../auth.js';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ForgotPasswordView from '../views/ForgotPasswordView.vue';
import ResetPasswordView from '../views/ResetPasswordView.vue';
import MoviesListView from '../views/MoviesListView.vue';
import ProfileView from '../views/ProfileView.vue';
import MovieView from '../views/MovieView.vue';
import PersonView from '../views/PersonView.vue';
import NotFoundView from '../views/NotFoundView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/movies/'
    },
    {
      path: '/login/',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/register/',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true }
    },
    {
      path: '/password-forgot/',
      name: 'password-forgot',
      component: ForgotPasswordView
    },
    {
      path: '/password-reset/:token/',
      name: 'password-reset',
      component: ResetPasswordView,
      props: true
    },
    {
      path: '/movies/:search',
      name: 'movies-search',
      component: MoviesListView,
      props: true
    },
    {
      path: '/movies/',
      name: 'movies',
      component: MoviesListView
    },
    {
      path: '/profile/',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/movies/movie/:id',
      name: 'movie',
      component: MovieView,
      props: true
    },
    {
      path: '/person/:id',
      name: 'person',
      component: PersonView,
      props: true
    },
    {
      // Any other address
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView
    }
  ]
});

router.beforeEach(async (to) => {
  if (!to.meta.guestOnly) return true;
  const user = await ensureUserLoaded();
  return user ? nextPath(to) : true;
});

export default router;
