import axios from "axios";
import {EMAIL_VALIDATION} from "../const";

export async function emailValidation(data){
    return axios.post(EMAIL_VALIDATION, data)
}