import Title from "@/components/atoms/Title";
import Icon from "@/components/atoms/Icon";
import { Link } from "react-router-dom";

export default function Footer() {
    return (
        <footer style={{background: "#404040"}} className="d-flex flex-row">
            <div className="py-5 container-md d-flex gap-5">
            <div className="d-flex flex-column gap-3">
                <div>
                <Link to="/">
                <img src="/logos/logo1.svg"/>
                </Link>
                <Title color="white" heading="6">Herencia de mi Abuelo</Title>
                </div>
                <div className="d-flex gap-3">
                <Link to="https://www.google.com/">
                <Icon name="whatsapp" color="white" size="24"></Icon>
                </Link>
                <Link to="https://www.google.com/">
                <Icon name="facebook" color="white" size="24"></Icon>
                </Link>
                </div>
                <Link to="https://web.flow.cl/es-cl/">
                <img src="/logos/flow.webp" style={{height: "100px", width: "100px"}} />
                </Link>
            </div>
            <div>
                <Title heading="4" color="white">Explora</Title>
                <div className="d-flex flex-column gap-2">
                    <Link className="text-decoration-none" to="/">
                    <span className="text-white">Inicio</span>
                    </Link>
                    <Link className="text-decoration-none" to="/catalogo">
                    <span className="text-white">Catálogo</span>
                    </Link>
                    <Link className="text-decoration-none" to="/visor_3d">
                    <span className="fw-bold text-white">Visor 3D</span>
                    </Link>
                </div>
            </div>
            </div>
        </footer>
    );
}