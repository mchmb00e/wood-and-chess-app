import api from '@/api/axiosConfig';
import { prefixService, concatUrl } from '@/utils/prefixService';
import { schema } from '@/utils/schema';

const prefixName = prefixService('usuario');

export const login = async (email, password) => {

    const body = {
        'email': email,
        'contrasena': password
    };

    const res = await api.post(
        concatUrl(prefixName, '/autenticar'),
        body
    );
    console.log(res.data)
    return schema(res.status, res.data);
};

export const register = async (
    rut, nombre, apellido, telefono, email, password
) => {
    const body = {
        'rut': rut,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'contrasena': password
    };

    const res = await api.post(
        concatUrl(prefixName, '/registrar'),
        body
    );

    return schema(res.status, res.data);
}

export const getUserData = async (token) => {

    const res = await api.get(
        concatUrl(prefixName, '/obtener_sesion'), 
        {
            headers: {
                'Authorization': `Bearer ${token}` 
            }
        }
    );
    console.log(res.data)
    return schema(res.status, res.data);
};