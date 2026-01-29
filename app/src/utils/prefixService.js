export const prefixService = (service) => import.meta.env.VITE_PREFIX_API + '/' + service;

export const concatUrl = (prefix, endpoint) => prefix + endpoint;