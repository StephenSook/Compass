import { motion } from 'framer-motion'

export default function AnimatedUnderline({ children, color = '#1B8A4A', delay = 0 }) {
  return (
    <span style={{ position: 'relative', display: 'inline-block' }}>
      {children}
      <motion.span
        initial={{ scaleX: 0 }}
        whileInView={{ scaleX: 1 }}
        viewport={{ once: true, margin: '-50px' }}
        transition={{ duration: 0.8, delay: delay + 0.3, ease: [0.22, 1, 0.36, 1] }}
        style={{
          position: 'absolute',
          bottom: -4,
          left: 0,
          width: '100%',
          height: 4,
          borderRadius: 9999,
          background: `linear-gradient(90deg, ${color}, #75C38F)`,
          transformOrigin: 'left',
        }}
      />
    </span>
  )
}
