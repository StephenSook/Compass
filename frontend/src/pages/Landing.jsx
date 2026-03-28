import { Link } from 'react-router-dom'
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'
import { CheckCircle2, Route, MessageCircle } from 'lucide-react'
import Navbar from '../components/Navbar'
import DanceText from '../components/DanceText'
import StarButton from '../components/StarButton'
import AnimatedUnderline from '../components/AnimatedUnderline'
import CountUp from '../components/CountUp'

const features = [
  {
    icon: CheckCircle2,
    title: 'Personalized Checklists',
    description: 'Every step tailored to your state, county, and situation. No more generic guides.',
  },
  {
    icon: Route,
    title: 'Two Journeys at Launch',
    description: "Driver's license and passport — with visa & immigration guidance. More coming soon.",
  },
  {
    icon: MessageCircle,
    title: 'AI Follow-Up Q&A',
    description: 'Stuck on a step? Ask our AI assistant for specific help with your situation.',
  },
]

const stats = [
  { value: '44.9', suffix: 'M', label: 'foreign-born residents in the US' },
  { value: '67', suffix: '%', label: 'report difficulty navigating government systems' },
  { value: '0', suffix: '', label: 'consumer tools that personalize the process' },
]

export default function Landing() {
  return (
    <div style={{ width: '100%', minHeight: '100vh', background: '#F7FAFC' }}>
      <Navbar />

      {/* Hero with Video Background */}
      <section style={{ position: 'relative', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', width: '100%' }}>
        {/* Video Background */}
        <video
          autoPlay
          loop
          muted
          playsInline
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }}
        >
          <source src="/background.mp4" type="video/mp4" />
        </video>

        {/* Dark overlay */}
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.5)' }} />

        {/* Hero Content */}
        <div style={{ position: 'relative', zIndex: 10, width: '100%', maxWidth: '1100px', margin: '0 auto', padding: '0 24px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}
          >
            <DanceText
              text="Your guide to navigating America"
              className="h-16 sm:h-20 mb-6 text-xl sm:text-2xl lg:text-3xl"
            />

            <h1 style={{ fontSize: 'clamp(2.5rem, 6vw, 5.5rem)', fontWeight: 800, color: 'white', lineHeight: 1.05, letterSpacing: '-0.02em', marginBottom: '2rem', textAlign: 'center' }}>
              Every government process.{' '}
              <span style={{ color: '#75C38F', fontStyle: 'italic' }}>One clear path.</span>
            </h1>

            <p style={{ fontSize: 'clamp(1.1rem, 2vw, 1.5rem)', color: 'rgba(255,255,255,0.75)', lineHeight: 1.7, maxWidth: '750px', marginBottom: '3rem', textAlign: 'center' }}>
              Stop Googling conflicting answers. Compass takes your specific situation and gives
              you a personalized, step-by-step checklist with the exact documents, forms, costs,
              and offices you need.
            </p>

            <Link to="/onboard">
              <StarButton label="Start Your Journey" large />
            </Link>
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          style={{ position: 'absolute', bottom: '2rem', left: '50%', transform: 'translateX(-50%)', zIndex: 10 }}
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{ width: 24, height: 40, borderRadius: 9999, border: '2px solid rgba(255,255,255,0.3)', display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 6 }}
          >
            <div style={{ width: 6, height: 10, background: 'rgba(255,255,255,0.5)', borderRadius: 9999 }} />
          </motion.div>
        </motion.div>
      </section>

      {/* Features */}
      <section style={{ width: '100%', padding: '6rem 1.5rem', background: '#F7FAFC' }}>
        <div style={{ width: '100%', maxWidth: '1100px', margin: '0 auto', textAlign: 'center' }}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            style={{ marginBottom: '4rem', textAlign: 'center' }}
          >
            <h2 style={{ fontSize: 'clamp(2rem, 4vw, 3rem)', fontWeight: 700, color: '#0F1B2D', marginBottom: '1rem', fontStyle: 'italic', textAlign: 'center' }}>
              Built for people <AnimatedUnderline>navigating a new system</AnimatedUnderline>
            </h2>
            <p style={{ color: '#6b7280', fontSize: '1.25rem', maxWidth: '640px', margin: '0 auto', textAlign: 'center' }}>
              Whether you just arrived or you're helping a family member, Compass gives you clarity.
            </p>
          </motion.div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 40, scale: 0.9 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ delay: i * 0.15, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                whileHover={{ y: -8, boxShadow: '0 20px 40px rgba(27,138,74,0.12)' }}
                style={{ background: 'white', borderRadius: '1rem', border: '1px solid #e5e7eb', padding: '2rem', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', cursor: 'default', transition: 'box-shadow 0.3s' }}
              >
                <motion.div
                  initial={{ scale: 0, rotate: -20 }}
                  whileInView={{ scale: 1, rotate: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.15 + 0.2, duration: 0.5, type: 'spring', stiffness: 200 }}
                  style={{ width: 56, height: 56, borderRadius: '1rem', background: '#E8F5EE', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}
                >
                  <feature.icon style={{ width: 28, height: 28, color: '#1B8A4A' }} />
                </motion.div>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 600, color: '#0F1B2D', marginBottom: '0.75rem' }}>
                  {feature.title}
                </h3>
                <p style={{ color: '#6b7280', fontSize: '1.125rem', lineHeight: 1.7 }}>
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section style={{ width: '100%', padding: '5rem 1.5rem', background: 'white', borderTop: '1px solid #e5e7eb', borderBottom: '1px solid #e5e7eb' }}>
        <div style={{ width: '100%', maxWidth: '1000px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2.5rem', textAlign: 'center' }}>
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 30, scale: 0.9 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ delay: i * 0.2, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
              style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
            >
              <div style={{ fontSize: 'clamp(2.5rem, 5vw, 3.75rem)', fontWeight: 700, color: '#1B8A4A', marginBottom: '0.75rem', fontStyle: 'italic' }}>
                <CountUp value={stat.value} suffix={stat.suffix} duration={2000} />
              </div>
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2 + 0.4, duration: 0.5 }}
                style={{ color: '#6b7280', fontSize: '1.125rem' }}
              >
                {stat.label}
              </motion.div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={{ width: '100%', padding: '6rem 1.5rem', background: '#F7FAFC' }}>
        <div style={{ width: '100%', maxWidth: '640px', margin: '0 auto', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <motion.div
            initial={{ opacity: 0, y: 40, scale: 0.95 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            viewport={{ once: true, margin: '-60px' }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
            style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
          >
            <h2 style={{ fontSize: 'clamp(2rem, 4vw, 3rem)', fontWeight: 700, color: '#0F1B2D', marginBottom: '1.25rem', fontStyle: 'italic', textAlign: 'center' }}>
              Ready to <AnimatedUnderline delay={0.1}>simplify the process?</AnimatedUnderline>
            </h2>
            <p style={{ color: '#6b7280', fontSize: '1.25rem', marginBottom: '2.5rem', textAlign: 'center' }}>
              Answer a few questions and get your personalized checklist in seconds.
            </p>
            <Link to="/onboard">
              <StarButton label="Get Started — It's Free" large />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ width: '100%', padding: '2.5rem 1.5rem', borderTop: '1px solid #e5e7eb', background: 'white' }}>
        <div style={{ width: '100%', maxWidth: '1100px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <img src="/compass-logo.png" alt="Compass" style={{ width: 32, height: 32, borderRadius: 8, objectFit: 'cover' }} />
            <span style={{ fontSize: '1.125rem', fontWeight: 600, color: '#0F1B2D' }}>Compass</span>
          </div>
          <p style={{ fontSize: '1rem', color: '#9ca3af', textAlign: 'center' }}>
            Built at Vibe&lt;ATL&gt; 2026 &middot; Georgia Tech
          </p>
        </div>
      </footer>
    </div>
  )
}
