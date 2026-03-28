import { useEffect, useRef, useState } from 'react'

export default function TextParticle({
  text,
  fontSize = 80,
  fontFamily = "'Cormorant Garamond', Georgia, serif",
  particleSize = 2,
  particleColor = '#1B8A4A',
  particleDensity = 8,
  backgroundColor = 'transparent',
  className = '',
}) {
  const canvasRef = useRef(null)
  const particlesRef = useRef([])
  const mouseRef = useRef({ x: null, y: null })
  const animationRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const initText = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight

      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.font = `700 ${fontSize}px ${fontFamily}`
      ctx.fillStyle = 'black'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'

      ctx.fillText(text, canvas.width / 2, canvas.height / 2)

      const textCoordinates = ctx.getImageData(0, 0, canvas.width, canvas.height)
      const newParticles = []

      for (let y = 0; y < textCoordinates.height; y += particleDensity) {
        for (let x = 0; x < textCoordinates.width; x += particleDensity) {
          const index = (y * textCoordinates.width + x) * 4
          const alpha = textCoordinates.data[index + 3]

          if (alpha > 128) {
            newParticles.push({
              x,
              y,
              size: particleSize,
              baseX: x,
              baseY: y,
              density: Math.random() * 30 + 1,
              color: particleColor,
            })
          }
        }
      }

      particlesRef.current = newParticles
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      if (backgroundColor !== 'transparent') {
        ctx.fillStyle = backgroundColor
        ctx.fillRect(0, 0, canvas.width, canvas.height)
      }

      const mouse = mouseRef.current

      particlesRef.current.forEach((particle) => {
        let forceDirectionX = 0
        let forceDirectionY = 0

        if (mouse.x !== null && mouse.y !== null) {
          const dx = mouse.x - particle.x
          const dy = mouse.y - particle.y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < 100) {
            forceDirectionX = (dx / distance) * 3
            forceDirectionY = (dy / distance) * 3
          }
        }

        particle.x += forceDirectionX + (particle.baseX - particle.x) * 0.05
        particle.y += forceDirectionY + (particle.baseY - particle.y) * 0.05

        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        ctx.fillStyle = particle.color
        ctx.fill()
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    initText()
    animate()

    const handleResize = () => {
      initText()
    }
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      if (animationRef.current) cancelAnimationFrame(animationRef.current)
    }
  }, [text, fontSize, fontFamily, particleSize, particleColor, particleDensity, backgroundColor])

  const handleMouseMove = (e) => {
    const rect = canvasRef.current.getBoundingClientRect()
    mouseRef.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    }
  }

  const handleMouseLeave = () => {
    mouseRef.current = { x: null, y: null }
  }

  return (
    <canvas
      ref={canvasRef}
      className={`w-full h-full ${className}`}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    />
  )
}
