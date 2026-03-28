import { useEffect, useRef, useState } from 'react'
import { useInView } from 'framer-motion'

export default function CountUp({ value, suffix = '', duration = 2000 }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })
  const [display, setDisplay] = useState('0')

  useEffect(() => {
    if (!isInView) return

    const numericValue = parseFloat(value.replace(/[^0-9.]/g, ''))
    const hasDecimal = value.includes('.')
    const startTime = performance.now()

    const animate = (now) => {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      const current = eased * numericValue

      if (hasDecimal) {
        setDisplay(current.toFixed(1))
      } else {
        setDisplay(Math.round(current).toString())
      }

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }, [isInView, value, duration])

  return (
    <span ref={ref}>
      {display}{suffix}
    </span>
  )
}
