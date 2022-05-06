export const API_URL = "http://localhost:8000";
export const URL = "http://localhost:5000/";
export const PROD = __app.env.PROD;
export const INIT = "referral"

export const LOGIN_URL = `${API_URL}/api/auth/login/`;

export const CHANGE_PASSWORD = `${API_URL}/api/auth/password/change`;

export const FORGET_PASSWORD_API = `${API_URL}/api/auth/password/forget`;

export const PASSWORD_RESET_VALIDATION = `${API_URL}/api/auth/password/forget/validate`;

export const PASSWORD_RESET = `${API_URL}/api/auth/password/reset`

export const UPDATE_ACCOUNT = `${API_URL}/api/auth/user/update/`

export const RECRUITER_RETRIEVE = `${API_URL}/api/core/recruiter/`;

export const RECRUITER_CREATE = `${API_URL}/api/core/recruiter/create`

export const COMMISSION_LIST = `${API_URL}/api/core/recruiter/commission`;

export const REFERRAL_LIST = `${API_URL}/api/core/referral/`;

export const REF_CODE = `${API_URL}/api/core/ref-code/`;

export const REFERRED = `${API_URL}/api/core/recruit/`;

export const RECRUITER_INFO = `${API_URL}/api/core/recruiter/info`;

export const EMAIL_VALIDATION = `${API_URL}/api/auth/user/email/check`;

export const HOME_PAGE = "/"

export const FORGET_PASSWORD = "forget-password"

export const RESET_PASSWORD = "reset-password"

export const RECRUITERS_REFERRAL_ROUTE = "recruits"

export const DASHBOARD = "dashboard"

export const ABOUT = "about"

export const RECRUIT_REG = "recruit/registration"

export const RECRUITER_REG = "recruiter/registration"

export const MY_ACCOUNT = "my-account"

export const LOGIN = "login"

export const INVITATION_URL = `${URL}/${INIT}/${RECRUIT_REG}`

export const tck = "xAGVy1Lol5";
export const tckrm = "AtTEp85Nbi"
export const tckrma = "CXcsjPrMvL"

export const LIST_LOAD_ERROR_MSG = "We are unable to load your data, please try again or reload the page, make sure you have a stable internet connection"
export const REF_CODE_ERROR_MSG = "We are unable to load your referral code, please try again later, make sure you have a stable internet connection"