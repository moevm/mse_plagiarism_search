import Vuex from 'vuex';
import Vue from 'vue';
import Axios from 'axios';
import {URL} from '@/url.config';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        algorithmResults: [],
    },

    getters: {
        RESULTS: state => {
            return state.algorithmResults;
        },
    },

    mutations: {
        SET_RESULTS: (state, payload) => {
            state.algorithmResults.push(payload);
        },
    },

    actions: {
        SET_RESULTS: async (injectee, payload) => {
            for (let value of payload.values()) {
                let formData = new FormData;
                formData.append('file', value)
                let res = await Axios.post(
                    `${URL + 'loadAndCheckFile'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    });
                injectee.commit('SET_RESULTS', [res.data, value.name]);
            }
        },

        SET_GIT_RESULTS: async (injectee, payload) => {
            console.log(payload)
            if (payload.status) {
                console.log('is private')
            } else {
                console.log(payload.repository)
                let formData = new FormData();
                formData.append('url', payload.repository)
                let res = await Axios.post(
                    `${URL + 'load_repo'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
                console.log(res)
                console.log('is not private')
            }
        }
    },

});
