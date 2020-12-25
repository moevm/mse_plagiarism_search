import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: 'search'
        },
        {
            path: '/search',
            component: () => import('./views/Search.vue')
        },
        {
            path: '/database',
            component: () => import('./views/Database.vue')
        },
        {
            path: '/history',
            component: () => import('./views/History.vue')
        },
        {
            path: '/about',
            component: () => import('./views/About.vue')
        },
        {
            path: '/search/result',
            component: () => import('./views/Result.vue')
        },
        {
            path: '/search/result/:id',
            component: () => import('./views/File')
        }
    ]
})
