import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { AlertTriangle, CheckCircle2, PartyPopper } from 'lucide-react'
import Navbar from '../components/Navbar'
import StepCard from '../components/StepCard'
import ChatPanel from '../components/ChatPanel'
import { journeys } from '../data/journeys'

export default function Journey() {
  const { journeyId } = useParams()
  const navigate = useNavigate()
  const [completedSteps, setCompletedSteps] = useState([])

  const journey = journeys[journeyId]

  useEffect(() => {
    if (!journey) {
      navigate('/dashboard')
      return
    }
    const saved = localStorage.getItem(`compass-completed-${journeyId}`)
    if (saved) setCompletedSteps(JSON.parse(saved))
  }, [journeyId, journey, navigate])

  const userProfile = (() => {
    try {
      return JSON.parse(localStorage.getItem('compass-profile'))
    } catch {
      return null
    }
  })()

  if (!journey) return null

  const toggleStep = (stepId) => {
    setCompletedSteps((prev) => {
      const next = prev.includes(stepId)
        ? prev.filter((id) => id !== stepId)
        : [...prev, stepId]
      localStorage.setItem(`compass-completed-${journeyId}`, JSON.stringify(next))
      return next
    })
  }

  const progress = Math.round((completedSteps.length / journey.totalSteps) * 100)
  const isComplete = completedSteps.length === journey.totalSteps

  return (
    <div style={{ width: '100%', minHeight: '100vh', background: '#F7FAFC' }}>
      <Navbar />

      <div style={{ width: '100%', paddingTop: '6rem', paddingBottom: '8rem', paddingLeft: '1.5rem', paddingRight: '1.5rem' }}>
        <div style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>

          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ marginBottom: '2rem', textAlign: 'center' }}
          >
            <h1 style={{ fontSize: 'clamp(2rem, 4vw, 2.5rem)', fontWeight: 700, color: '#0F1B2D', marginBottom: '0.5rem' }}>
              {journey.title}
            </h1>
            <p style={{ color: '#6b7280', fontSize: '1.1rem' }}>{journey.description}</p>
          </motion.div>

          {/* Disclaimer (visa journey) */}
          {journey.disclaimer && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              style={{
                marginBottom: '1.5rem',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
                background: '#FFFBEB',
                border: '1px solid #FDE68A',
                borderRadius: '1rem',
                padding: '1.25rem 1.5rem',
              }}
            >
              <AlertTriangle style={{ width: 20, height: 20, color: '#F59E0B', flexShrink: 0, marginTop: 2 }} />
              <p style={{ fontSize: '0.95rem', color: '#92400E', lineHeight: 1.6 }}>{journey.disclaimer}</p>
            </motion.div>
          )}

          {/* Progress bar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            style={{
              marginBottom: '2rem',
              background: 'white',
              borderRadius: '1rem',
              border: '1px solid #e5e7eb',
              padding: '1.5rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <CheckCircle2 style={{ width: 20, height: 20, color: '#1B8A4A' }} />
                <span style={{ fontSize: '1rem', fontWeight: 600, color: '#0F1B2D' }}>Your Progress</span>
              </div>
              <span style={{ fontSize: '1rem', fontWeight: 700, color: '#1B8A4A' }}>{progress}%</span>
            </div>
            <div style={{ height: 10, background: '#f3f4f6', borderRadius: 9999, overflow: 'hidden' }}>
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
                style={{ height: '100%', background: '#1B8A4A', borderRadius: 9999 }}
              />
            </div>
            <p style={{ fontSize: '0.9rem', color: '#6b7280', marginTop: '0.5rem' }}>
              {completedSteps.length} of {journey.totalSteps} steps completed
            </p>
          </motion.div>

          {/* Completion banner */}
          {isComplete && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{
                marginBottom: '2rem',
                background: '#E8F5EE',
                border: '1px solid #A3D7B4',
                borderRadius: '1rem',
                padding: '2rem',
                textAlign: 'center',
              }}
            >
              <PartyPopper style={{ width: 40, height: 40, color: '#1B8A4A', margin: '0 auto 0.75rem' }} />
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#10532C', marginBottom: '0.25rem' }}>Journey Complete!</h3>
              <p style={{ fontSize: '1rem', color: '#166E3B' }}>
                You've completed all steps. You're ready to go!
              </p>
            </motion.div>
          )}

          {/* Steps */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {journey.steps.map((step, index) => (
              <StepCard
                key={step.id}
                step={step}
                index={index}
                isCompleted={completedSteps.includes(step.id)}
                onToggle={toggleStep}
              />
            ))}
          </div>

        </div>
      </div>

      {/* Chat Panel */}
      <ChatPanel journeyId={journeyId} userProfile={userProfile} />
    </div>
  )
}
