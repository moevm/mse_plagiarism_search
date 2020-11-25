import Vuex from 'vuex'
import Vue from 'vue'
import Axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        algorithmResult: {}
    },

    getters: {
        RESULT: state => {
            return state.algorithmResult;
        }
    },

    mutations: {
        SET_RESULT: ((state, payload) => {
            state.algorithmResult = payload;
        })
    },

    actions: {
        SET_RESULT: async (injectee, payload) => {
            let res = await Axios.post(
                'http://127.0.0.1:5000/loadAndCheckFile',
                payload,
                {
                headers: {
                    'Content-Type': 'multipart/form-data; charset=utf-8'
                }
                });
            console.log(res.data);
            injectee.commit('SET_RESULT', res.data);
        }
    }
});