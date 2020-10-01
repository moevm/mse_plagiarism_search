import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/plagiarism_search',
            component: Home
        },

        {
            path: '/todos',
            component: () => import('./views/Todos.vue')
        }
    ]
})