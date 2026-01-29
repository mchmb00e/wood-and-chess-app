import React from 'react'
import { useGLTF, useTexture } from '@react-three/drei' // 1. Importamos useTexture

export default function ChessKing(props) {
  // Ya no necesitamos 'materials' porque usaremos el nuestro
  const { nodes } = useGLTF('/models/chess_king.glb') 

  // 2. Cargamos las texturas
  const textures = useTexture({
    map: '/models/textures/diffuse.jpg',      // Color base (Diffuse)
    normalMap: '/models/textures/normal.jpg', // Relieve (Normal)
    roughnessMap: '/models/textures/rough.jpg'// Rugosidad (Roughness)
  })

  return (
    <group {...props} dispose={null}>
      <group scale={1}>
        <mesh 
          geometry={nodes.Cylinder__0.geometry} 
          // 3. Quitamos la prop 'material={...}' original
          rotation={[-Math.PI / 2, 0, 0]} 
          scale={[2.151, 2.05, 4.533]} 
        >
          {/* 4. Aplicamos el nuevo material estándar */}
          <meshStandardMaterial 
            {...textures} 
            roughness={1} // Multiplicador para ajustar la intensidad de la textura rough
          />
        </mesh>
      </group>
    </group>
  )
}

useGLTF.preload('/models/chess_king.glb')
// Opcional: Pre-cargar texturas también para evitar parpadeos
useTexture.preload('/models/textures/diffuse.jpg')