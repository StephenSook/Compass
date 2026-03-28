import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Check,
  ChevronDown,
  FileText,
  DollarSign,
  MapPin,
  Clock,
  Lightbulb,
  Phone,
} from 'lucide-react'

export default function StepCard({ step, index, isCompleted, onToggle }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
      style={{
        borderRadius: '1rem',
        border: isCompleted ? '1px solid #A3D7B4' : '1px solid #e5e7eb',
        background: isCompleted ? 'rgba(232,245,238,0.5)' : 'white',
        transition: 'all 0.2s',
      }}
    >
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        style={{
          width: '100%',
          padding: '1.5rem 1.75rem',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '1rem',
          textAlign: 'left',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontFamily: 'inherit',
        }}
      >
        {/* Checkbox */}
        <button
          onClick={(e) => {
            e.stopPropagation()
            onToggle(step.id)
          }}
          style={{
            marginTop: 2,
            flexShrink: 0,
            width: 32,
            height: 32,
            borderRadius: '50%',
            border: isCompleted ? '2px solid #1B8A4A' : '2px solid #d1d5db',
            background: isCompleted ? '#1B8A4A' : 'transparent',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s',
            padding: 0,
          }}
        >
          {isCompleted && <Check style={{ width: 18, height: 18, color: 'white' }} strokeWidth={3} />}
        </button>

        {/* Content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
            <span style={{
              fontSize: '0.85rem',
              fontWeight: 700,
              color: '#1B8A4A',
              background: '#E8F5EE',
              padding: '0.25rem 0.75rem',
              borderRadius: 9999,
            }}>
              Step {step.id}
            </span>
          </div>
          <h3 style={{
            fontSize: '1.25rem',
            fontWeight: 600,
            color: isCompleted ? '#9ca3af' : '#0F1B2D',
            textDecoration: isCompleted ? 'line-through' : 'none',
            transition: 'color 0.2s',
          }}>
            {step.title}
          </h3>
          <p style={{ fontSize: '1.05rem', color: '#6b7280', marginTop: '0.25rem', lineHeight: 1.5 }}>
            {step.summary}
          </p>
        </div>

        {/* Expand icon */}
        <ChevronDown
          style={{
            width: 22,
            height: 22,
            color: '#9ca3af',
            flexShrink: 0,
            marginTop: 4,
            transition: 'transform 0.2s',
            transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
          }}
        />
      </button>

      {/* Expanded Details */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            style={{ overflow: 'hidden' }}
          >
            <div style={{ padding: '0 1.75rem 1.75rem', paddingLeft: '4.75rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              {/* Action */}
              <p style={{ fontSize: '1.05rem', color: '#374151', lineHeight: 1.7, whiteSpace: 'pre-line' }}>
                {step.action}
              </p>

              {/* Documents */}
              {step.documents?.length > 0 && (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    <FileText style={{ width: 18, height: 18, color: '#1B8A4A' }} />
                    <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#0F1B2D', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Documents Needed
                    </span>
                  </div>
                  <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', listStyle: 'none', padding: 0 }}>
                    {step.documents.map((doc, i) => (
                      <li key={i} style={{ fontSize: '1.05rem', color: '#4b5563', display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                        <span style={{ color: '#47AF6A', marginTop: 2 }}>&#8226;</span>
                        {doc}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Forms */}
              {step.forms?.length > 0 && (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    <FileText style={{ width: 18, height: 18, color: '#3b82f6' }} />
                    <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#0F1B2D', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Forms
                    </span>
                  </div>
                  <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', listStyle: 'none', padding: 0 }}>
                    {step.forms.map((form, i) => (
                      <li key={i} style={{ fontSize: '1.05rem', color: '#4b5563', display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                        <span style={{ color: '#60a5fa', marginTop: 2 }}>&#8226;</span>
                        {form}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Resources (for visa journey) */}
              {step.resources?.length > 0 && (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    <Phone style={{ width: 18, height: 18, color: '#1B8A4A' }} />
                    <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#0F1B2D', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Legal Resources
                    </span>
                  </div>
                  <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem', listStyle: 'none', padding: 0 }}>
                    {step.resources.map((r, i) => (
                      <li key={i} style={{
                        fontSize: '1.05rem',
                        color: '#4b5563',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        background: '#f9fafb',
                        borderRadius: '0.75rem',
                        padding: '0.75rem 1rem',
                      }}>
                        <span style={{ fontWeight: 500 }}>{r.name}</span>
                        <a href={`tel:${r.phone}`} style={{ color: '#1B8A4A', fontWeight: 500, textDecoration: 'none' }}>
                          {r.phone}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Cost / Location / Timeline row */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
                {/* Cost */}
                {step.cost && (
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.625rem', background: '#FFFBEB', borderRadius: '0.75rem', padding: '1rem 1.125rem' }}>
                    <DollarSign style={{ width: 20, height: 20, color: '#D97706', flexShrink: 0, marginTop: 2 }} />
                    <div>
                      <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#92400E', textTransform: 'uppercase' }}>Cost</span>
                      <p style={{ fontSize: '1.05rem', color: '#B45309', marginTop: '0.125rem' }}>{step.cost}</p>
                    </div>
                  </div>
                )}

                {/* Location */}
                {step.location && (
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.625rem', background: '#EFF6FF', borderRadius: '0.75rem', padding: '1rem 1.125rem' }}>
                    <MapPin style={{ width: 20, height: 20, color: '#2563EB', flexShrink: 0, marginTop: 2 }} />
                    <div>
                      <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#1E40AF', textTransform: 'uppercase' }}>Location</span>
                      <p style={{ fontSize: '1.05rem', color: '#1D4ED8', marginTop: '0.125rem' }}>{step.location}</p>
                    </div>
                  </div>
                )}

                {/* Timeline */}
                {step.timeline && (
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.625rem', background: '#F5F3FF', borderRadius: '0.75rem', padding: '1rem 1.125rem' }}>
                    <Clock style={{ width: 20, height: 20, color: '#7C3AED', flexShrink: 0, marginTop: 2 }} />
                    <div>
                      <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#5B21B6', textTransform: 'uppercase' }}>Timeline</span>
                      <p style={{ fontSize: '1.05rem', color: '#6D28D9', marginTop: '0.125rem' }}>{step.timeline}</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Pro Tip */}
              {step.tip && (
                <div style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  background: '#E8F5EE',
                  border: '1px solid #A3D7B4',
                  borderRadius: '0.75rem',
                  padding: '1.125rem 1.25rem',
                }}>
                  <Lightbulb style={{ width: 22, height: 22, color: '#1B8A4A', flexShrink: 0, marginTop: 2 }} />
                  <div>
                    <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#10532C', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Pro Tip
                    </span>
                    <p style={{ fontSize: '1.05rem', color: '#0B371E', marginTop: '0.25rem', lineHeight: 1.6 }}>{step.tip}</p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
