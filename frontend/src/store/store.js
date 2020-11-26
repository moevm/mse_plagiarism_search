import Vuex from 'vuex'
import Vue from 'vue'
import Axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        algorithmResult: {},
        fileName: ''
    },

    getters: {
        RESULT: state => {
            return state.algorithmResult;
        },
        FILE_NAME: state => {
            return state.fileName;
        }
    },

    mutations: {
        SET_RESULT: (state, payload) => {
            state.algorithmResult = payload;
        },
        SET_FILE_NAME: (state, payload) => {
            state.fileName = payload;
        }
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
            injectee.commit('SET_RESULT', res.data);
        },
        SET_FILENAME: (injectee, payload) =>{
            console.log(payload);
            injectee.commit('SET_FILE_NAME', payload);
        }
    }
});