import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from '../utils/auth'

const Layout = () => import('../layouts/MainLayout.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true, title: '登录' },
  },
  {
    path: '/p/asset/:token',
    name: 'PublicAsset',
    component: () => import('../views/PublicAsset.vue'),
    meta: { public: true, title: '资产信息' },
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '主页', icon: 'HomeFilled' },
      },
      {
        path: 'assets',
        redirect: '/dashboard',
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('../views/Messages.vue'),
        meta: { title: '日志' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { public: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta?.public) return true
  if (!isLoggedIn()) {
    const redirect = encodeURIComponent(to.fullPath)
    return { path: '/login', query: { redirect } }
  }
  if (to.path === '/login' && isLoggedIn()) {
    return { path: '/dashboard' }
  }
  return true
})

export default router
