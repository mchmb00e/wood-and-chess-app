import Title from "@/components/atoms/Title";
import TextField from "../atoms/TextField";
import Button from "../atoms/Button";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
// Asegúrate de que estas funciones existen y funcionan. 
// Si dudas, coméntalas y usa las versiones temporales de abajo.
import { isEmail, isPassword } from "@/utils/AuthString";
import Alert from "@/components/atoms/Alert";

// --- VALIDACIONES TEMPORALES DE PRUEBA (Descomenta si las tuyas fallan) ---
// const isEmail = (text) => text && text.includes('@');
// const isPassword = (text) => text && text.length > 3;

export default function LoginForm({className="", onSubmit, message}) {
    const [ credential, setCredential ] = useState({'email': '', 'contrasena': ''});
    
    // Calculamos el estado de cada campo por separado para ver cuál falla
    const emailValido = isEmail(credential.email);
    const passValido = isPassword(credential.contrasena);
    
    const isValid = emailValido && passValido;

    const handleChange = (key, value) => {
        setCredential({
            ...credential,
            [key]: value
        });
    };

    const navigate = useNavigate();

    return (
        <div className={`${className}`}>
            <Title color="white" heading="1">¡Bienvenido a Wood&Chess!</Title>
            <Alert
                className={`${message !== undefined ? "d-block" : "d-none"} mt-5 mb-3`}
                color="warning"
            >{message !== undefined ? message : ""}</Alert>
            <div>
                <Title color="white" heading="2">Que alegría tenerte de vuelta.</Title>
                
                <div className="d-flex flex-column gap-4 mt-4">
                    <TextField
                        onChange={(e) => handleChange('email', e.target.value)}
                        label="Correo electrónico:"
                        placeholder="ejemplo@correo.com"
                        placeholderSize="16"
                        fontSize="5"
                        value={credential.email}
                    />
                    <TextField
                        onChange={(e) => handleChange('contrasena', e.target.value)}
                        label="Contraseña:"
                        placeholder="Escribe tu contraseña..."
                        placeholderSize="16"
                        fontSize="5"
                        type="password"
                        value={credential.contrasena}
                    />
                </div>

                <div className="d-flex flex-column align-items-center justify-content-center gap-3 mt-5">
                    
                    {/* Botón Principal */}
                    <Button 
                        iconName="person" 
                        iconSize="24" 
                        textColor="white" 
                        disabled={!isValid}  // Si isValid es false, el botón se apaga
                        onClick={() => onSubmit(credential)}
                    >
                        Iniciar sesión
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