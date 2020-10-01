import Vue from 'vue';
import App from './App.vue';
import router from './router';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap-vue/dist/bootstrap-vue.min.css';

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

import DefaultLayout from "@/layouts/DefaultLayout";

Vue.component('default-layout', DefaultLayout);

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
