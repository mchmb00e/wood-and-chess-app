import Model from '@/components/organisms/Authentication/Model';
import LoginSection from '@/components/organisms/Authentication/LoginSection';
import { useState } from 'react';

// Services
import { login } from "@/services/authService";
import { useNavigate } from 'react-router-dom';
import { useTitle } from '@/hooks/useTitle';

export default function Login({onSubmit}) {

    useTitle('Iniciar sesión');
    
    const [ error, setError ] = useState(undefined);
    const navigate = useNavigate();

     // Autenticación de usuario
    const handleSubmitLogin = async (e) => {
        const authUser = await login(e.email, e.contrasena);

        if (authUser.status === 200) {
            setError(undefined);
            localStorage.setItem('token', authUser.data.token);
            navigate('/');
        } else if (authUser.status === 400) {
            setError(authUser.data.error);
        }
    }

    return (
        <div className="d-flex flex-row">
            <Model className="w-50 vh-100" />
            <LoginSection message={error} onSubmit={(e) => handleSubmitLogin(e)} className="w-50 vh-100 d-flex flex-row align-items-center justify-content-center" />
        </div>
    );
}