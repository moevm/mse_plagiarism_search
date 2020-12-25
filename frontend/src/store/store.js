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
                console.log(value);
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
                if(value.name.indexOf('.zip' || '.zipp') + 1) {
                    for (let i = 0; i < res.data.length; ++i) {
                        console.log(res.data[i])
                        injectee.commit('SET_RESULTS', [res.data[i], res.data[i][7].replace(/^.*[\\/]/, '')]);
                    }
                } else {
                    injectee.commit('SET_RESULTS', [res.data, value.name]);
                }
            }
        },

        SET_GIT_RESULTS: async (injectee, payload) => {
            console.log(payload)
            let formData = new FormData();
            let loadRepository;

            if (payload.status) {
                console.log('is private')
                formData.append('url', payload.repository.replace(/(https:\/\/)?(www.)?github.com\//, ''));
                console.log(payload.repository.replace(/(www.)?github.com/, ''));
                formData.append('login', payload.login);
                formData.append('token', payload.token);
                formData.append('organization', payload.organization);
                let loginData = await Axios.post(
                    `${URL + 'update_org_settings'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
                console.log(loginData);
                loadRepository = await Axios.post(
                    `${URL + 'load_repos_from_org'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                )
            } else {
                formData.append('url', payload.repository);
                loadRepository = await Axios.post(
                    `${URL + 'load_repo'}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data; charset=utf-8'
                        }
                    }
                );
                console.log(loadRepository)
            }

            formData.append('entries', JSON.stringify(loadRepository.data));
            let getResult = await Axios.post(
                `${URL + 'checkFilesByEntries'}`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data; charset=utf-8'
                    }
                }
            )
            console.log(getResult)
            for (let file of getResult.data.values())
                injectee.commit('SET_RESULTS', [file, file[7]]);
        },

        SET_HISTORY_RESULTS: async (injectee, payload) => {
            await Axios.get(`${URL + 'getResult/' + payload}`)
                .then(res => {
                    for(let i = 0; i < res.data.length; ++i)
                    {
                        injectee.commit('SET_RESULTS', [res.data[0][i], res.data[0][i][7].replace(/^.*[\\/]/, '')]);
                    }
                });
        }
    },

});
