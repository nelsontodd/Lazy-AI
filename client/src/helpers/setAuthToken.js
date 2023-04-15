const timeLimit = 30 * 60 * 1000;


export const setAuthToken = (token) => {
    var now = new Date();
    var expireTime = new Date(now.getTime() + timeLimit);
    const tokenCookie = `token=${token};expires=${expireTime.toUTCString()};`;
    document.cookie = tokenCookie;
}

export const getCookies = () => {
    return document.cookie
        .split(";")
        .map(cookie => cookie.split("="))
        .reduce(
                (accumulator, [key, value]) => (
                {...accumulator, [key.trim()]: decodeURIComponent(value)}
            ),
            {}
        );
}

export const isLoggedIn = () => {
    const cookies = getCookies();
    const token = cookies.token;
    if (token !== undefined && token !== "") {
        return true;
    }
    return false;
}

export const deleteCookie = (cookie) => {
    document.cookie = `${cookie}=;expires=-1`;
}
