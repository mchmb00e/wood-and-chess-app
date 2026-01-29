import Title from "@/components/atoms/Title";
import TextField from "@/components/atoms/TextField";
import Button from "@/components/atoms/Button";
import Alert from "@/components/atoms/Alert";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { isDataRegister } from "@/utils/AuthString";

export default function RegisterForm({ className = "", onSubmit, message}) {

    const [data, setData] = useState({
        'rut': '',
        'nombre': '',
        'apellido': '',
        'email': '',
        'telefono': '',
        'contrasena': '',
        'verificar_contrasena': ''
    });

    const handleChange = (key, value) => {
        setData(prev => ({
            ...prev,
            [key]: value
        }));
    };

    // Función especial para el RUT: Solo permite números
    const handleRutChange = (e) => {
        const value = e.target.value;
        // Reemplaza todo lo que NO sea dígito (\D) por vacío
        const cleanValue = value.replace(/\D/g, '');
        handleChange('rut', cleanValue);
    };

    const isValid = isDataRegister(data);
    const navigate = useNavigate();

    const fs = 6;
    const phs = 16;

    return (
        <div className={`${className}`}>
            <Title color="white" heading="1">¡Bienvenido a Wood&Chess!</Title>
            <Alert
                            className={`${message !== undefined ? "d-block" : "d-none"} mt-5 mb-3`}
                            color="warning"
                        >{message !== undefined ? message : ""}</Alert>
            <div>
                <Title color="white" heading="2">Necesitamos conocerte un poco más...</Title>
                <div className="d-flex flex-column gap-4 mt-4">
                    <div className="d-flex flex-row justify-content-center align-items-center gap-3">
                        <TextField
                            label="¿Cuál es tu nombre?"
                            placeholder="Mi nombre es..."
                            placeholderSize={phs}
                            fontSize={fs}
                            value={data.nombre}
                            maxLength={50} // Máximo 50 caracteres
                            onChange={(e) => handleChange('nombre', e.target.value)}
                        />
                        <TextField
                            label="¿Cuál es tu apellido?"
                            placeholder="Mi apellido es..."
                            placeholderSize={phs}
                            fontSize={fs}
                            value={data.apellido}
                            maxLength={50} // Máximo 50 caracteres
                            onChange={(e) => handleChange('apellido', e.target.value)}
                        />
                    </div>
                    <div className="d-flex flex-row justify-content-center align-items-center gap-3">
                        <TextField
                            label="¿Cuál es tu rut?"
                            placeholder="Ej: 12345678 (Sin dígito verif.)"
                            placeholderSize={phs}
                            fontSize={fs}
                            value={data.rut}
                            maxLength={9} // Máximo 9 caracteres
                            onChange={handleRutChange} // Usamos el handler especial
                        />
                        <TextField
                            label="¿Cuál es tu teléfono?"
                            placeholder="9 ..."
                            placeholderSize={phs}
                            fontSize={fs}
                            value={data.telefono}
                            maxLength={9} // Máximo 9 caracteres
                            onChange={(e) => handleChange('telefono', e.target.value)}
                        />
                    </div>
                    <TextField
                        label="¿Dónde te podemos escribir?"
                        placeholder="Mi correo electrónico es..."
                        placeholderSize={phs}
                        fontSize={fs}
                        value={data.email}
                        maxLength={50} // Máximo 50 caracteres
                        onChange={(e) => handleChange('email', e.target.value)}
                    />
                    <div className="d-flex flex-row justify-content-center align-items-center gap-3">
                        <TextField
                            label="Ingresa una contraseña:"
                            placeholder="Contraseña..."
                            placeholderSize={phs}
                            fontSize={fs}
                            type="password"
                            value={data.contrasena}
                            maxLength={20} // Máximo 20 caracteres
                            onChange={(e) => handleChange('contrasena', e.target.value)}
                        />
                        <TextField
                            label="Verifica tu contraseña:"
                            placeholder="Repite tu contraseña..."
                            placeholderSize={phs}
                            fontSize={fs}
                            type="password"
                            value={data.verificar_contrasena}
                            maxLength={20} // Máximo 20 caracteres
                            onChange={(e) => handleChange('verificar_contrasena', e.target.value)}
                        />
                    </div>
                </div>
                <div className="d-flex flex-column align-items-center justify-content-center gap-3 mt-5">
                    <Button 
                        iconName="person" 
                        iconSize="24" 
                        textColor="white"
                        disabled={!isValid} 
                        onClick={() => onSubmit && onSubmit(data)}
                    >
                        Registrarse en Wood&Chess
                    </Button>
                    <Button 
                        iconName="arrow-left" 
                        iconSize="24" 
                        textColor="white" 
                        onClick={() => navigate('/')} 
                        isOutline="true" 
                        btnColor="light"
                    >
                        Regresar
                    </Button>
                </div>
            </div>
        </div>
    );
}