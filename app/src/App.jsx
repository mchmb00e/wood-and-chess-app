import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { useState, useEffect } from "react"; 
import { getUserData } from "@/services/authService";

// Routes
import Home from '@/components/templates/Home';
import Register from "@/components/templates/Register";
import Login from "@/components/templates/Login";

// 1. Creamos este componente hijo para poder usar el hook useLocation
function AppContent() {
  const [logged, setLogged] = useState(undefined);
  
  // Obtenemos la ubicación actual
  const location = useLocation();

  useEffect(() => {
    const verifyAuth = async () => {
      const token = localStorage.getItem('token');

      if (token) {
        const userData = await getUserData();

        if (userData.status === 200) {
          setLogged(true);
        } else {
          localStorage.removeItem('token');
          setLogged(false);
        }
      } else {
        setLogged(false);
      }
    };

    verifyAuth();
    
    // 2. AGREGAMOS 'location.pathname' AL ARRAY DE DEPENDENCIAS
    // Esto hará que el useEffect se dispare cada vez que la URL cambie.
  }, [location.pathname]); 

  return (
      <Routes>
        <Route path="/" element={<Home isLogged={logged} />} />
        <Route path="/registrarse" element={<Register />} />
        <Route path="/iniciar_sesion" element={<Login />} />
      </Routes>
  );
}

// 3. El componente principal solo configura el Router y renderiza el contenido
function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;