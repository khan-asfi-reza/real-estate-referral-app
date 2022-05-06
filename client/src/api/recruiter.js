import axios from "axios";
import {RECRUITER_CREATE, RECRUITER_INFO, RECRUITER_RETRIEVE, COMMISSION_LIST, REFERRAL_LIST} from "../const";
import {getHeaders} from "../utils";


export async function recruiter(data){
    return await axios.post(RECRUITER_CREATE, data)
}

export async function getCommissionList(token, nextPage){
    return await axios.get(`${COMMISSION_LIST}?page=${nextPage}`, getHeaders(token))
}

export async function getRecruiterInfo(token){
    return await axios.get(RECRUITER_INFO, getHeaders(token))
}

export async function getRefCode(token){
    return await axios.get(RECRUITER_RETRIEVE, getHeaders(token))
}

export async function getReferralList(token, nextPage){
    return await axios.get(`${REFERRAL_LIST}?page=${nextPage}`, getHeaders(token))
}