import { useState } from 'react'
import { motion } from 'framer-motion'

export default function AnimatedShinyText({
  text,
  gradientColors = 'linear-gradient(90deg, #0B371E, #1B8A4A, #75C38F, #1B8A4A, #0B371E)',
  gradientAnimationDuration = 2,
  hoverEffect = true,
  className = '',
}) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <motion.span
      className={className}
      style={{
        background: gradientColors,
        backgroundSize: '200% auto',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        textShadow: isHovered ? '0 0 12px rgba(27,138,74,0.3)' : 'none',
      }}
      initial={{ backgroundPosition: '0 0' }}
      animate={{
        backgroundPosition: '100% 0',
        transition: {
          duration: gradientAnimationDuration,
          repeat: Infinity,
          repeatType: 'reverse',
        },
      }}
      onHoverStart={() => hoverEffect && setIsHovered(true)}
      onHoverEnd={() => hoverEffect && setIsHovered(false)}
    >
      {text}
    </motion.span>
  )
}
