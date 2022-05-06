import axios from "axios";
import {LOGIN_URL} from "../const";


// Login Api
export async function loginApi(email, password){
    return await axios.post(`${LOGIN_URL}`, {
        email: email,
        password: password,
    })
}