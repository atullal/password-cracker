import axios from 'axios';

const base = "127.0.0.1:5000";
export const api = `https://${base}/`;
export const wsApi = `ws://${base}/password`;

export const getInfo = () => {
    return new Promise((res, rej) => {
        axios.get(api)
        .then(function (response) {
            res(response);
        })
        .catch(function (error) {
            rej(error);
        });
    });
}

export const submitForm = (md5, clients) => {
    return new Promise((res, rej) => {
        axios.post(`${api}password-cracker`, {
            hash: md5,
            clients: clients
        })
        .then(function (response) {
            res(response);
        })
        .catch(function (error) {
            rej(error);
        });
    });
}

export const addClientsApi = (md5, clients, requestId) => {
    return new Promise((res, rej) => {
        axios.post(`${api}add-client`, {
            hash: md5,
            clients: clients,
            requestId: requestId
        })
        .then(function (response) {
            res(response);
        })
        .catch(function (error) {
            rej(error);
        });
    });
}

export const getAvailableClients = () => {
    return new Promise((res, rej) => {
        axios.get(`${api}get-available-clients`)
        .then(function (response) {
            res(response);
        })
        .catch(function (error) {
            rej(error);
        });
    });
}