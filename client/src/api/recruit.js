import axios from "axios";
import {REF_CODE, REFERRED} from "../const";

export async function recruitCreate(data){
    return axios.post(REFERRED, data)
}

export async function refCodeGet(data){
    return axios.post(REF_CODE, data)
}