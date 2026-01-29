import Logo from '@/components/atoms/Logo';
import Button from '@/components/atoms/Button';
import { Link } from "react-router-dom";

function Nav({ pageTitle, isLogged }) {

    const Routes = {
        home: '/',
        catalogo: '/catalogo',
        visor_3d: '/visor_3d'
    }

    const activeBorderColor = "#ffffff85"; 

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
            <div className="col-3">
            <Logo image="/logos/logo1.svg" width="auto" height="40px" alt="Logo" />
            </div>
            
            <div className="col-6 d-flex flex-row align-items-center justify-content-center gap-3">
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
                <div className="col-3 d-flex flex-row align-items-center justify-content-end">
                    <Button iconName="person" iconSize="24" isOutline="true" btnColor="light">Registrarse</Button>
                    <Button iconName="person-circle" iconSize="24" btnColor="light" isBold={true}>Iniciar sesión</Button>
                </div>
                :
                <div className="col-3 d-flex flex-row align-items-center justify-content-end gap-2">
                    <Button iconName="person" iconSize="24" isOutline="true" btnColor="light">Registrarse</Button>
                    <Button iconName="person-circle" iconSize="24" btnColor="light" isBold={true}>Iniciar sesión</Button>
                </div>
            }

        </div>
    );
}

export default Nav;