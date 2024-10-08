import axios from 'axios';

export interface IAccount {
    email_address: string;
    password: string;
}

export interface IAccountResponse {
    email_address: string;
    username: string;
}

export interface APIResponse<T> {
    success: boolean;
    message: string;
    result: T;
    error_fields?: [],
    error_message?: string;
}

export const headers = {

    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin' : '*',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
    'Secret-Key': ''
}

const baseURL: string = "http://127.0.0.1:5001";

export async function createNewAccount(account: IAccount): Promise<APIResponse<IAccount>> {

    const response = await axios.post(baseURL + '/users/create', account, {

        headers: headers
    })
    return response.data
}