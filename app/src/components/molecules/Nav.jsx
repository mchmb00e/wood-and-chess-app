import Logo from '@/components/atoms/Logo';
import Button from '@/components/atoms/Button';
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from 'react';
import { getUserData } from '@/services/authService'; // Asegúrate que la ruta sea correcta

function Nav({ pageTitle, isLogged }) {

    const [userName, setUserName] = useState("Usuario"); // Valor por defecto

    const Routes = {
        home: '/',
        catalogo: '/catalogo',
        visor_3d: '/visor_3d'
    }

    const navigate = useNavigate();

    const activeBorderColor = "#ffffff85"; 

    // Función auxiliar para formatear (Primera palabra + Capitalizada)
    const formatString = (str) => {
        if (!str) return "";
        // 1. Separamos por espacio y nos quedamos con la primera parte (index 0)
        const firstWord = str.trim().split(' ')[0];
        // 2. Capitalizamos la primera letra y concatenamos el resto en minúscula
        return firstWord.charAt(0).toUpperCase() + firstWord.slice(1).toLowerCase();
    };

    useEffect(() => {
        const fetchUserData = async () => {
            // Solo ejecutamos si el usuario está logueado
            if (isLogged) {
                try {
                    // getUserData internamente busca el token o se lo pasas según tu implementación previa
                    const response = await getUserData(); 

                    if (response.status === 200) {
                        const { nombre, apellido } = response.data;
                        
                        const nombreFormateado = formatString(nombre);
                        const apellidoFormateado = formatString(apellido);

                        setUserName(`${nombreFormateado} ${apellidoFormateado}`);
                    } else {
                        // Si el status no es 200 (ej: 401 token vencido), recargamos
                        window.location.reload();
                    }
                } catch (error) {
                    // Si falla la petición por red u otro motivo grave
                    window.location.reload();
                }
            }
        };

        fetchUserData();
    }, [isLogged]); // Se ejecuta cuando cambia el estado de login


    const renderLabel = (label, isActive) => (
        <span style={{ 
            borderBottom: isActive ? `1px solid ${activeBorderColor}` : '2px solid transparent',
            paddingBottom: '2px',
            transition: 'border-color 0.3s ease'
        }}>
            {label}
        </span>
    );

    return (
        <div className="d-flex justify-content-between align-items-center container-md py-3">
            <div className="col-4">
            <Logo image="/logos/logo1.svg" width="auto" height="40px" alt="Logo" />
            </div>
            
            <div className="col-4 d-flex flex-row align-items-center justify-content-center gap-3">
                <Link to={Routes.home} className="text-decoration-none">
                    <Button
                        isNoButton="true"
                        textColor="white"
                    >
                        {renderLabel("Home", pageTitle === 'Home')}
                    </Button>
                </Link>

                <Link to={Routes.catalogo} className="text-decoration-none">
                    <Button
                        isNoButton="true"
                        textColor="white"
                    >
                        {renderLabel("Catálogo", pageTitle === 'Catalogo')}
                    </Button>
                </Link>

                <Link to={Routes.visor_3d} className="text-decoration-none">
                    <Button
                        iconName="box"
                        iconSize="20"
                        textColor="white"
                        isBold="true"
                    >
                        Visor 3D
                    </Button>
                </Link>
            </div>

            {
                (isLogged) ?
                <div className="col-4 d-flex flex-row align-items-center justify-content-end gap-2">
                    <Button iconName="cart" iconSize="24" isOutline="true" btnColor="light">Carro</Button>
                    
                    {/* Botón con el nombre del usuario cargado dinámicamente */}
                    <Button iconName="person" iconSize="24" btnColor="light" isBold={true}>
                        {userName}
                    </Button>
                </div>
                :
                <div className="col-4 d-flex flex-row align-items-center justify-content-end gap-2">
                    <Button iconName="person" iconSize="24" isOutline="true" btnColor="light" onClick={() => navigate('/registrarse')}>Registrarse</Button>
                    <Button iconName="person-circle" iconSize="24" btnColor="light" isBold={true} onClick={() => navigate('/iniciar_sesion')}>Iniciar sesión</Button>
                </div>
            }

        </div>
    );
}

export default Nav;