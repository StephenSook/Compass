import { motion } from 'framer-motion'
import { Check } from 'lucide-react'
import StarButton from './StarButton'

export default function PricingCard({ plan, index, isPopular }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40, scale: 0.95 }}
      whileInView={{ opacity: 1, y: 0, scale: isPopular ? 1.05 : 1 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ delay: index * 0.15, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      style={{
        position: 'relative',
        background: isPopular
          ? 'linear-gradient(135deg, rgba(27,138,74,0.08), rgba(232,245,238,0.9))'
          : 'rgba(255,255,255,0.85)',
        backdropFilter: 'blur(14px)',
        borderRadius: '1.5rem',
        border: isPopular ? '2px solid #1B8A4A' : '1px solid #e5e7eb',
        padding: '2.5rem 2rem',
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        maxWidth: 340,
        boxShadow: isPopular
          ? '0 25px 50px rgba(27,138,74,0.15)'
          : '0 4px 20px rgba(0,0,0,0.06)',
        transition: 'transform 0.3s, box-shadow 0.3s',
      }}
    >
      {/* Popular badge */}
      {isPopular && (
        <div style={{
          position: 'absolute',
          top: -14,
          right: 24,
          background: '#1B8A4A',
          color: 'white',
          fontSize: '0.8rem',
          fontWeight: 700,
          padding: '0.35rem 1rem',
          borderRadius: 9999,
          letterSpacing: '0.03em',
        }}>
          Most Popular
        </div>
      )}

      {/* Plan name */}
      <h3 style={{
        fontSize: '1.5rem',
        fontWeight: 700,
        color: '#0F1B2D',
        marginBottom: '0.5rem',
      }}>
        {plan.name}
      </h3>

      <p style={{
        fontSize: '1rem',
        color: '#6b7280',
        lineHeight: 1.5,
        marginBottom: '1.5rem',
        minHeight: '3rem',
      }}>
        {plan.description}
      </p>

      {/* Price */}
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.25rem', marginBottom: '1.5rem' }}>
        <span style={{
          fontSize: 'clamp(2.5rem, 4vw, 3.5rem)',
          fontWeight: 300,
          color: '#0F1B2D',
          letterSpacing: '-0.02em',
        }}>
          {plan.price === '0' ? 'Free' : `$${plan.price}`}
        </span>
        {plan.price !== '0' && (
          <span style={{ fontSize: '1rem', color: '#9ca3af' }}>{plan.priceLabel || '/mo'}</span>
        )}
      </div>

      {/* Divider */}
      <div style={{
        width: '100%',
        height: 1,
        background: isPopular
          ? 'linear-gradient(90deg, transparent, #1B8A4A40, transparent)'
          : 'linear-gradient(90deg, transparent, #e5e7eb, transparent)',
        marginBottom: '1.5rem',
      }} />

      {/* Features */}
      <ul style={{
        listStyle: 'none',
        padding: 0,
        margin: 0,
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        marginBottom: '2rem',
        flex: 1,
      }}>
        {plan.features.map((feature, i) => (
          <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', fontSize: '1rem', color: '#374151' }}>
            <Check style={{ width: 16, height: 16, color: '#1B8A4A', flexShrink: 0 }} strokeWidth={3} />
            {feature}
          </li>
        ))}
      </ul>

      {/* Button */}
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        {isPopular ? (
          <StarButton label={plan.buttonText} large />
        ) : (
          <button
            style={{
              width: '100%',
              padding: '0.875rem 1.5rem',
              borderRadius: '0.75rem',
              border: '2px solid #e5e7eb',
              background: 'transparent',
              color: '#0F1B2D',
              fontSize: '1.05rem',
              fontWeight: 600,
              cursor: 'pointer',
              fontFamily: 'inherit',
              transition: 'all 0.2s',
            }}
            onMouseEnter={e => {
              e.target.style.borderColor = '#1B8A4A'
              e.target.style.color = '#1B8A4A'
            }}
            onMouseLeave={e => {
              e.target.style.borderColor = '#e5e7eb'
              e.target.style.color = '#0F1B2D'
            }}
          >
            {plan.buttonText}
          </button>
        )}
      </div>
    </motion.div>
  )
}
