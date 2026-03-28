import { Link, useLocation } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import StarButton from './StarButton'
import AnimatedShinyText from './AnimatedShinyText'

export default function Navbar() {
  const location = useLocation()
  const isHome = location.pathname === '/'
  const showBack = location.pathname !== '/' && location.pathname !== '/onboard'

  const userProfile = (() => {
    try {
      return JSON.parse(localStorage.getItem('compass-profile'))
    } catch {
      return null
    }
  })()

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-colors duration-300 ${isHome ? 'bg-transparent' : 'bg-white/80 backdrop-blur-md border-b border-compass-100'}`}>
      <div className="w-full px-6 sm:px-10 h-20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {showBack && (
            <Link
              to="/dashboard"
              className="p-2 -ml-2 rounded-lg hover:bg-compass-50 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-dark" />
            </Link>
          )}
          <Link to="/" className="flex items-center gap-3">
            <img src="/compass-logo.png" alt="Compass" className="w-12 h-12 rounded-xl object-cover" />
            <AnimatedShinyText
              text="Compass"
              className="text-4xl font-bold tracking-tight"
              gradientColors={isHome
                ? 'linear-gradient(90deg, #A3D7B4, #75C38F, #ffffff, #75C38F, #A3D7B4)'
                : undefined
              }
            />
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {userProfile && !isHome && (
            <div className="hidden sm:flex items-center gap-2">
              <span className="px-3.5 py-1.5 bg-compass-50 text-compass-700 rounded-full text-base font-semibold">
                {userProfile.state}
              </span>
            </div>
          )}
          {isHome && (
            <Link to="/onboard">
              <StarButton large />
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}
