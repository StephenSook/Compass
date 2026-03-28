import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Car, BookOpen, Globe, ArrowRight, CheckCircle2 } from 'lucide-react'
import Navbar from '../components/Navbar'
import { journeys, journeyOrder } from '../data/journeys'

const iconMap = {
  Car,
  BookOpen,
  Globe,
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [profile, setProfile] = useState(null)
  const [completedSteps, setCompletedSteps] = useState({})

  useEffect(() => {
    const saved = localStorage.getItem('compass-profile')
    if (!saved) {
      navigate('/onboard')
      return
    }
    setProfile(JSON.parse(saved))

    const completed = {}
    journeyOrder.forEach((id) => {
      const data = localStorage.getItem(`compass-completed-${id}`)
      completed[id] = data ? JSON.parse(data) : []
    })
    setCompletedSteps(completed)
  }, [navigate])

  if (!profile) return null

  const primaryJourneyId = profile.journeyId
  const primaryJourney = journeys[primaryJourneyId]
  const otherJourneys = journeyOrder.filter((id) => id !== primaryJourneyId)

  const getProgress = (journeyId) => {
    const journey = journeys[journeyId]
    const completed = completedSteps[journeyId] || []
    return Math.round((completed.length / journey.totalSteps) * 100)
  }

  return (
    <div style={{ width: '100%', minHeight: '100vh', background: '#F7FAFC' }}>
      <Navbar />

      <div style={{ width: '100%', paddingTop: '7rem', paddingBottom: '4rem', paddingLeft: '1.5rem', paddingRight: '1.5rem' }}>
        <div style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>

          {/* Welcome */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ marginBottom: '2rem', textAlign: 'center' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '1.125rem', color: '#6b7280' }}>Welcome back</span>
              <span style={{ padding: '0.25rem 0.75rem', background: '#E8F5EE', color: '#10532C', fontSize: '0.875rem', fontWeight: 500, borderRadius: '9999px' }}>
                {profile.situation}
              </span>
            </div>
            <h1 style={{ fontSize: 'clamp(2rem, 4vw, 2.5rem)', fontWeight: 700, color: '#0F1B2D' }}>
              Your Journeys
            </h1>
          </motion.div>

          {/* Active Journey — Large Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            style={{ marginBottom: '2rem' }}
          >
            <Link to={`/journey/${primaryJourneyId}`} style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}>
              <div style={{ background: 'white', borderRadius: '1rem', border: '1px solid #e5e7eb', padding: '2rem', transition: 'all 0.2s' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ width: 56, height: 56, borderRadius: '0.75rem', background: '#E8F5EE', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {(() => {
                        const Icon = iconMap[primaryJourney.icon]
                        return <Icon style={{ width: 28, height: 28, color: '#1B8A4A' }} />
                      })()}
                    </div>
                    <div>
                      <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#1B8A4A', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                        Active Journey
                      </span>
                      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#0F1B2D', margin: 0 }}>
                        {primaryJourney.title}
                      </h2>
                    </div>
                  </div>
                  <ArrowRight style={{ width: 24, height: 24, color: '#9ca3af' }} />
                </div>

                <p style={{ color: '#6b7280', fontSize: '1.06rem', marginBottom: '1.5rem' }}>
                  {primaryJourney.description}
                </p>

                {/* Progress */}
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '1rem', fontWeight: 500, color: '#4b5563' }}>Progress</span>
                    <span style={{ fontSize: '1rem', fontWeight: 700, color: '#1B8A4A' }}>
                      {getProgress(primaryJourneyId)}%
                    </span>
                  </div>
                  <div style={{ height: 10, background: '#f3f4f6', borderRadius: 9999, overflow: 'hidden' }}>
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${getProgress(primaryJourneyId)}%` }}
                      transition={{ duration: 0.6, delay: 0.3 }}
                      style={{ height: '100%', background: '#1B8A4A', borderRadius: 9999 }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', marginTop: '0.5rem' }}>
                    <CheckCircle2 style={{ width: 18, height: 18, color: '#47AF6A' }} />
                    <span style={{ fontSize: '0.9rem', color: '#6b7280' }}>
                      {(completedSteps[primaryJourneyId] || []).length} of{' '}
                      {primaryJourney.totalSteps} steps completed
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          </motion.div>

          {/* Other Journeys */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1rem', textAlign: 'center' }}>
              Other Journeys
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
              {otherJourneys.map((journeyId) => {
                const journey = journeys[journeyId]
                const Icon = iconMap[journey.icon]
                const progress = getProgress(journeyId)

                return (
                  <Link
                    key={journeyId}
                    to={`/journey/${journeyId}`}
                    style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}
                  >
                    <div style={{ background: 'white', borderRadius: '1rem', border: '1px solid #e5e7eb', padding: '1.5rem', transition: 'all 0.2s', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                      <div style={{ width: 48, height: 48, borderRadius: '0.75rem', background: '#E8F5EE', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '0.75rem' }}>
                        <Icon style={{ width: 24, height: 24, color: '#1B8A4A' }} />
                      </div>
                      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#0F1B2D', marginBottom: '0.5rem' }}>
                        {journey.title}
                      </h3>
                      <p style={{ color: '#6b7280', fontSize: '1rem', marginBottom: '1rem' }}>
                        {journey.description}
                      </p>
                      <div style={{ width: '100%', height: 6, background: '#f3f4f6', borderRadius: 9999, overflow: 'hidden' }}>
                        <div
                          style={{ height: '100%', background: '#75C38F', borderRadius: 9999, width: `${progress}%`, transition: 'all 0.3s' }}
                        />
                      </div>
                    </div>
                  </Link>
                )
              })}
            </div>
          </motion.div>

        </div>
      </div>
    </div>
  )
}
