import { createRouter, createWebHistory } from 'vue-router'
import Landing from '@/components/Landing';
import NotFound from '@/components/NotFound';
import About from '@/components/About';
import Prediction from '@/components/Prediction';
import Game from '@/components/Game';
import User from '@/services/UserService';

// eslint-disable-next-line
const ifAuthenticated = (to, from, next) => {
  return User.isAuthenticated ? next() : next('/');
};

const routes = [
  {
    path: '/:pathMatch(.*)*',
    name: 'Not Found',
    component: NotFound,
  },
  {
    path: '/',
    name: 'Landing',
    component: Landing,
  },
  {
    path: '/about',
    name: 'About the Game',
    component: About,
  },
  {
    path: '/prediction',
    name: 'Prediction Tool',
    component: Prediction,
  },
  {
    path: '/game',
    name: 'game',
    component: Game,
    beforeEnter: ifAuthenticated,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})
export default router;