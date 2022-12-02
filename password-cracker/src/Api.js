import axios from 'axios';

export const getInfo = () => {
    return new Promise((res, rej) => {
        axios.get('http://127.0.0.1:5000/')
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
        axios.post('http://127.0.0.1:5000/password-cracker', {
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
        axios.post('http://127.0.0.1:5000/add-client', {
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
        axios.get('http://127.0.0.1:5000/get-available-clients')
        .then(function (response) {
            res(response);
        })
        .catch(function (error) {
            rej(error);
        });
    });
}