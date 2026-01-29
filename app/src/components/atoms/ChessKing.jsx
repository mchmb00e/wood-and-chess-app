
import React from 'react'
import { useGLTF } from '@react-three/drei' 

export default function ChessKing(rest) {
  const { nodes, materials } = useGLTF('/models/chess_king.glb')
  
  return (
    <group {...rest} dispose={null}>
      <group scale={1}>
        <mesh 
          geometry={nodes.Cylinder__0.geometry} 
          material={materials['Scene_-_Root']} 
          rotation={[-Math.PI / 2, 0, 0]} 
          scale={[2.151, 2.05, 4.533]} 
        />
      </group>
    </group>
  )
}

useGLTF.preload('/models/chess_king.glb')