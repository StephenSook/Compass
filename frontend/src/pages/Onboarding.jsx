import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, ArrowRight, MapPin, Users, Target, Languages } from 'lucide-react'

const questions = [
  {
    id: 'state',
    icon: MapPin,
    title: 'Where are you located?',
    subtitle: 'We tailor your checklist to your state\'s requirements.',
    options: ['Georgia', 'California', 'Texas', 'New York', 'Florida', 'Other'],
  },
  {
    id: 'county',
    icon: MapPin,
    title: 'What county are you in?',
    subtitle: 'Some steps depend on your specific county in Georgia.',
    options: ['Fulton', 'DeKalb', 'Gwinnett', 'Cobb', 'Clayton', 'Other'],
    condition: (answers) => answers.state === 'Georgia',
  },
  {
    id: 'situation',
    icon: Users,
    title: 'What best describes your situation?',
    subtitle: 'This helps us personalize your experience.',
    options: [
      'New immigrant',
      'First-gen navigator',
      'Visa holder',
      'Recently relocated',
      'New citizen',
      'Other',
    ],
  },
  {
    id: 'goal',
    icon: Target,
    title: 'What do you need help with?',
    subtitle: 'Choose your first journey. You can always add more later.',
    options: ["Driver's License", 'Passport', 'Visa / Immigration'],
  },
  {
    id: 'language',
    icon: Languages,
    title: 'Preferred language?',
    subtitle: 'We\'ll do our best to guide you in your preferred language.',
    options: ['English', 'Espanol', '中文', '한국어', 'Tieng Viet', 'Amharic'],
  },
]

const goalToJourneyId = {
  "Driver's License": 'ga-drivers-license',
  'Passport': 'us-passport',
  'Visa / Immigration': 'visa-immigration',
}

export default function Onboarding() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(0)
  const [answers, setAnswers] = useState({})
  const [direction, setDirection] = useState(1)

  // Filter questions based on conditions
  const activeQuestions = questions.filter(
    (q) => !q.condition || q.condition(answers)
  )

  const currentQuestion = activeQuestions[currentStep]
  const totalSteps = activeQuestions.length
  const progress = ((currentStep + 1) / totalSteps) * 100

  const handleSelect = (option) => {
    const newAnswers = { ...answers, [currentQuestion.id]: option }
    setAnswers(newAnswers)

    // Auto-advance after a short delay
    setTimeout(() => {
      if (currentStep < totalSteps - 1) {
        setDirection(1)
        setCurrentStep(currentStep + 1)
      } else {
        // Save profile and navigate
        const profile = {
          state: newAnswers.state,
          county: newAnswers.county || null,
          situation: newAnswers.situation,
          goal: newAnswers.goal,
          language: newAnswers.language,
          journeyId: goalToJourneyId[newAnswers.goal] || 'ga-drivers-license',
        }
        localStorage.setItem('compass-profile', JSON.stringify(profile))
        navigate('/dashboard')
      }
    }, 300)
  }

  const handleBack = () => {
    if (currentStep > 0) {
      setDirection(-1)
      setCurrentStep(currentStep - 1)
    }
  }

  const Icon = currentQuestion.icon

  return (
    <div className="min-h-screen bg-[#f0f4f8] flex flex-col">
      {/* Top bar */}
      <div className="px-4 sm:px-6 pt-6">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2.5">
              <img src="/compass-logo.png" alt="Compass" className="w-8 h-8 rounded-xl object-cover" />
              <span className="text-xl font-bold text-dark">Compass</span>
            </div>
            <span className="text-base text-gray-400">
              {currentStep + 1} of {totalSteps}
            </span>
          </div>

          {/* Progress bar */}
          <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-compass-500 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.div
              key={currentQuestion.id}
              custom={direction}
              initial={{ opacity: 0, x: direction * 60 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: direction * -60 }}
              transition={{ duration: 0.25 }}
            >
              {/* Question title above the card */}
              <div className="text-center mb-8">
                <h1 className="text-3xl sm:text-4xl font-bold text-dark italic">
                  {currentQuestion.title}
                </h1>
                <p className="text-gray-500 text-lg mt-2">{currentQuestion.subtitle}</p>
              </div>

              {/* Beam card */}
              <div className="beam-card">
                <div className="beam-card-inner px-8 py-8 sm:px-10 sm:py-10">
                  {/* Icon */}
                  <div className="flex justify-center mb-6">
                    <div className="w-14 h-14 rounded-2xl bg-compass-50 flex items-center justify-center">
                      <Icon className="w-7 h-7 text-compass-500" />
                    </div>
                  </div>

                  {/* Options */}
                  <div className="space-y-3">
                    {currentQuestion.options.map((option) => {
                      const isSelected = answers[currentQuestion.id] === option
                      return (
                        <motion.button
                          key={option}
                          whileHover={{ scale: 1.01 }}
                          whileTap={{ scale: 0.99 }}
                          onClick={() => handleSelect(option)}
                          className={`w-full px-5 py-4 rounded-xl border text-left font-medium text-lg transition-all duration-150 flex items-center gap-3 ${
                            isSelected
                              ? 'bg-compass-50 border-compass-500 text-compass-700'
                              : 'bg-gray-50 border-gray-200 text-dark hover:border-compass-300 hover:bg-white'
                          }`}
                        >
                          {/* Radio circle */}
                          <div
                            className={`w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all ${
                              isSelected
                                ? 'border-compass-500'
                                : 'border-gray-300'
                            }`}
                          >
                            {isSelected && (
                              <div className="w-2.5 h-2.5 rounded-full bg-compass-500" />
                            )}
                          </div>
                          {option}
                        </motion.button>
                      )
                    })}
                  </div>
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Bottom nav */}
      <div className="px-4 pb-8">
        <div className="max-w-2xl mx-auto flex justify-between">
          <button
            onClick={handleBack}
            disabled={currentStep === 0}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium text-base transition-all ${
              currentStep === 0
                ? 'text-gray-300 cursor-not-allowed'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>

          {answers[currentQuestion.id] && currentStep < totalSteps - 1 && (
            <button
              onClick={() => {
                setDirection(1)
                setCurrentStep(currentStep + 1)
              }}
              className="flex items-center gap-2 px-6 py-2.5 bg-compass-500 text-white rounded-xl font-medium text-base hover:bg-compass-600 transition-colors"
            >
              Continue
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
