const STORAGE_KEY = "meal:star";

/**
 * @typedef Star
 * @property {string} name
 * @property {string} path
 */

/**
 * @returns {Star[]}
 */
export function get_star() {
    let star = JSON.parse(localStorage.getItem(STORAGE_KEY));

    if (star == null) {
        star = [];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(star));
    }

    return star;
}

/**
 * @param {string} name
 * @param {string} path
 */
export function add_star(name, path) {
    let star = get_star();

    star.push({ name, path });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(star));
}

/**
 * @param {string} name
 */
export function del_star(name) {
    let star = get_star();

    star = star.filter((x) => x.name != name);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(star));
}
