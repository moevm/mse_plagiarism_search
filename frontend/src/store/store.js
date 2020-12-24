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
                let first = await Axios.post(
                    `${URL + 'load_repo'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
                console.log('entries', first.data)
                formData.append('entries', JSON.stringify(first.data))
                let second = await Axios.post(
                    `${URL + 'checkFilesByEntries'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
                console.log(typeof(second.data));
                for (let i = 0; i < second.data.length; ++i) {
                    injectee.commit('SET_RESULTS', [second.data[i], 'value.name']);
                    console.log(second.data[i]);
                }
                console.log('is not private')
            }
        }
    },

});
