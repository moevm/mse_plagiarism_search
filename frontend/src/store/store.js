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
                console.log(res.data);
                injectee.commit('SET_RESULTS', [res.data, value.name]);
            }
        },

        SET_GIT_RESULTS: async (injectee, payload) => {
            console.log(payload)
            if (payload.status) {
                console.log('is private')
                let formData = new FormData();
                console.log(payload)
                // https://github.com/Artex-Test-Organization/Test-Repository-A-Private
                formData.append('login', payload.login);
                formData.append('token', payload.token);
                formData.append('organization', payload.organization);
                let first = await Axios.post(
                    `${URL + 'update_org_settings'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
                console.log(first.data);
                /*
                {
            "login": "AlexRyzhickov",
            "token": "fb464859ebc0740b7f841f2cd950c47d6f7ca627",
            "organization": "Artex-Test-Organization"
            "https://github.com/Artex-Test-Organization/Test-Repository-A-Privat"
         }*/
            } else {
                let formData = new FormData();
                formData.append('url', payload.repository);
                let first = await Axios.post(
                    `${URL + 'load_repo'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
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
               // console.log(second.data);
                for(let file of second.data.values())
                {
                    console.log(file[7]);
                    injectee.commit('SET_RESULTS',[file, file[7]]);
                }

                console.log('is not private')
            }
        }
    },

});
