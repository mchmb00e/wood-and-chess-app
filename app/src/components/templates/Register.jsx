import Model from '@/components/organisms/Authentication/Model';
import RegisterSection from '@/components/organisms/Authentication/RegisterSection';
import { useTitle } from '@/hooks/useTitle';
import { register } from '@/services/authService';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Register() {
    useTitle('Registrarse');
    const navigate = useNavigate();
    const [ error, setError ] = useState(undefined);

    const handleSubmitRegister = async (e) => {
        const registerUser = await register(e.rut, e.nombre, e.apellido, e.telefono, e.email, e.contrasena);
        
                if (registerUser.status === 200) {
                    setError(undefined);
                    localStorage.setItem('token', registerUser.data.token);
                    navigate('/');
                } else if (registerUser.status === 400) {
                    setError(registerUser.data.error);
                }
    }

    return (
        <div className="d-flex flex-row-reverse">
            <Model className="w-50 vh-100" />
            <RegisterSection message={error} onSubmit={handleSubmitRegister} className="w-50 vh-100 d-flex flex-row align-items-center justify-content-center" />
        </div>
    );
}