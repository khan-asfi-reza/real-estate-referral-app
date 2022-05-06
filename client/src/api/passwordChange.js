import axios from "axios";
import {CHANGE_PASSWORD} from "../const";
import {getHeaders} from "../utils";


export async function changePasswordApi(request_body, token) {
   return await axios.post(CHANGE_PASSWORD, request_body, getHeaders(token))
}