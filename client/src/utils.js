import {DASHBOARD, INVITATION_URL, LOGIN, RECRUIT_REG, RECRUITER_REG} from "./const";


export function getHeaders(token) {
    return {
        headers: {
            Authorization: `Token ${token}`
        }
    }
}

const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]

export function formatDate(date){
    const d = new Date(date);
    return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
}

export function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}

export function getFrom(location){
    let from = location.state && location.state.from || `/${DASHBOARD}`;
    console.log(from);
    if(from === `/${LOGIN}` || from === `/${RECRUIT_REG}` || from === `/${RECRUITER_REG}`){
        from = `/${DASHBOARD}`
    }
    return from
}

// Password Validation
export function passwordValidation(password, confirm_password) {
    if (password && confirm_password) {
        if (password !== confirm_password) {
            return [false, "Password does not match"]
        } else {
            if (password.length < 8) {
                return [false, "Password is short"]
            } else return [true, ""];
        }
    }
    return [false, "INVALID"]
}


// Copy to clipboard
export function copyToClipboard(data, func) {
    navigator.clipboard.writeText(`${INVITATION_URL}/${data}`)
        .then(() => {
            func()
        })
        .catch((e) => {
        })
}

// Phone Number Format
export function formatPhoneNumber(phoneNumberString) {
    const charRemoved = phoneNumberString.replace(/[a-zA-Z]/g, '')
    const cleaned = ('' + charRemoved).replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{3})$/);
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3];
    }
    return charRemoved;
}

//
export function formatPhoneNumber2(phoneNumberString){

}