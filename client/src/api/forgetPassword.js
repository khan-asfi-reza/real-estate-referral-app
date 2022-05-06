import axios from "axios";
import {FORGET_PASSWORD_API, PASSWORD_RESET_VALIDATION, PASSWORD_RESET} from "../const";

export async function forgetPasswordSendEmailApi(email){
    return await axios.post(FORGET_PASSWORD_API, {email: email})
}

export async function validatePasswordReset(uniqueLink){
    return await axios.post(PASSWORD_RESET_VALIDATION, {unique_link: uniqueLink})
}

export async function resetPasswordApi(data){
    return await axios.post(PASSWORD_RESET, data)
}

