import React, { useRef, Suspense, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, ContactShadows, Html } from '@react-three/drei';
import ChessKing from '@/components/atoms/ChessKing';
import { MathUtils } from 'three';

function Scene() {
  const ref = useRef();
  
  // Referencia para el valor normalizado (-1 a 1) que usa el useFrame
  const mousePosition = useRef(0);
  
  // NUEVO: Referencia para guardar la última posición en píxeles crudos (X)
  const lastPixelX = useRef(0);

  useEffect(() => {
    const handleMove = (event) => {
      let clientX;

      if (event.touches && event.touches.length > 0) {
        clientX = event.touches[0].clientX;
      } else {
        clientX = event.clientX;
      }

      // --- LÓGICA DE OPTIMIZACIÓN (Umbral de 4px) ---
      // Calculamos la distancia entre donde está el mouse ahora y donde estaba la última vez
      const diff = Math.abs(clientX - lastPixelX.current);

      // Solo actualizamos si se movió 4 píxeles o más
      if (diff >= 30) {
        // 1. Actualizamos la referencia del pixel para la próxima comparación
        lastPixelX.current = clientX;

        // 2. Ejecutamos la matemática de normalización (ahorro de CPU)
        const normalizedX = (clientX / window.innerWidth) * 2 - 1;
        mousePosition.current = normalizedX;
      }
    };

    window.addEventListener('mousemove', handleMove);
    window.addEventListener('touchmove', handleMove);

    return () => {
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('touchmove', handleMove);
    };
  }, []);

  useFrame((state, delta) => {
    if (!ref.current) return;

    const maxRotation = Math.PI / 3;

    const targetRotationY = mousePosition.current * maxRotation;
    
    // El Lerp se encargará de suavizar esos "saltos" de 4 píxeles
    // para que visualmente no se vea trabado.
    ref.current.rotation.y = MathUtils.lerp(
      ref.current.rotation.y, 
      targetRotationY, 
      0.1
    );

    ref.current.rotation.x = MathUtils.lerp(ref.current.rotation.x, 0.2 + (mousePosition.current * 0.6), 0.3);
  });

  return (
    <group ref={ref}>
      <ChessKing scale={0.25} position={[0, 0, 0]} rotation={[0.1, 0, 0]} />
    </group>
  );
}

function Loader() {
  return <Html center><span className="text-white">Cargando...</span></Html>
}

export default function ChessKingViewer({
    width,
    height,
    className
  }) {

  return (
    <div style={{ height: height || '500px',
                  width: width || '100%',
                  position: 'relative' }} className = {className ? className : ""}>
      
      <Canvas camera={{ position: [0, 0, 4], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <Environment preset="city" />

        <Suspense fallback={<Loader />}> 
          <Scene />
        </Suspense>

        <ContactShadows position={[0, -1.2, 0]} opacity={0.4} blur={2.5} />
      </Canvas>
    </div>
  );
}