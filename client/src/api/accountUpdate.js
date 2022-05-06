import axios from "axios";
import {UPDATE_ACCOUNT} from "../const";
import {getHeaders} from "../utils";


export async function accountUpdateApi(request_body, token){
    return await axios.patch(UPDATE_ACCOUNT, request_body, getHeaders(token))
}