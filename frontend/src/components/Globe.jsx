import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Sphere } from '@react-three/drei'
import * as THREE from 'three'

function EarthSphere() {
  const meshRef = useRef()
  const pointsRef = useRef()

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.15
    }
    if (pointsRef.current) {
      pointsRef.current.rotation.y += delta * 0.15
    }
  })

  const landPoints = useMemo(() => {
    const points = []
    const count = 2000

    // Simplified continent regions (lat/lon ranges)
    const continents = [
      // North America
      { latMin: 25, latMax: 55, lonMin: -130, lonMax: -70, density: 1 },
      // South America
      { latMin: -55, latMax: 10, lonMin: -80, lonMax: -35, density: 0.8 },
      // Europe
      { latMin: 35, latMax: 60, lonMin: -10, lonMax: 40, density: 1 },
      // Africa
      { latMin: -35, latMax: 35, lonMin: -20, lonMax: 50, density: 0.9 },
      // Asia
      { latMin: 10, latMax: 55, lonMin: 60, lonMax: 140, density: 1 },
      // Australia
      { latMin: -40, latMax: -12, lonMin: 112, lonMax: 155, density: 0.6 },
      // Central America
      { latMin: 7, latMax: 25, lonMin: -105, lonMax: -75, density: 0.5 },
      // Middle East
      { latMin: 12, latMax: 40, lonMin: 35, lonMax: 60, density: 0.5 },
      // Southeast Asia
      { latMin: -10, latMax: 20, lonMin: 95, lonMax: 140, density: 0.6 },
    ]

    for (let i = 0; i < count; i++) {
      const continent = continents[Math.floor(Math.random() * continents.length)]
      if (Math.random() > continent.density) continue

      const lat = continent.latMin + Math.random() * (continent.latMax - continent.latMin)
      const lon = continent.lonMin + Math.random() * (continent.lonMax - continent.lonMin)

      const phi = (90 - lat) * (Math.PI / 180)
      const theta = (lon + 180) * (Math.PI / 180)

      const r = 2.01
      const x = -(r * Math.sin(phi) * Math.cos(theta))
      const y = r * Math.cos(phi)
      const z = r * Math.sin(phi) * Math.sin(theta)

      points.push(x, y, z)
    }

    return new Float32Array(points)
  }, [])

  return (
    <group>
      {/* Ocean sphere */}
      <Sphere ref={meshRef} args={[2, 64, 64]}>
        <meshPhongMaterial
          color="#1a3a5c"
          shininess={15}
          transparent
          opacity={0.95}
        />
      </Sphere>

      {/* Land dots */}
      <points ref={pointsRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={landPoints.length / 3}
            array={landPoints}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          color="#1B8A4A"
          size={0.04}
          sizeAttenuation
          transparent
          opacity={0.85}
        />
      </points>

      {/* Atmosphere glow */}
      <Sphere args={[2.08, 64, 64]}>
        <meshPhongMaterial
          color="#1B8A4A"
          transparent
          opacity={0.06}
          side={THREE.BackSide}
        />
      </Sphere>
    </group>
  )
}

export default function Globe({ className = '' }) {
  return (
    <div className={`${className}`}>
      <Canvas
        camera={{ position: [0, 0, 5.5], fov: 45 }}
        style={{ background: 'transparent' }}
        gl={{ alpha: true, antialias: true }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 3, 5]} intensity={1.2} />
        <directionalLight position={[-3, -2, -3]} intensity={0.3} color="#1B8A4A" />
        <EarthSphere />
      </Canvas>
    </div>
  )
}
