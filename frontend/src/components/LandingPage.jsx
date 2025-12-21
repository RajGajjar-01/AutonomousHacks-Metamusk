import { Link } from 'react-router'
import Footer from './Footer'

const LandingPage = () => {
  return (
    <>
      <div className="relative w-full overflow-x-hidden min-h-screen flex flex-col">
        {/* Gradient Background - Emerging from bottom, covering entire screen */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute bottom-[200px] left-1/2 -translate-x-1/2 w-full max-w-[1400px] h-[900px] bg-gradient-to-t from-primary/20 via-secondary/15 to-transparent blur-[250px] rounded-full"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-4 sm:px-6 md:px-8">
          <div className="text-center max-w-3xl w-full">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 sm:mb-5 md:mb-6 leading-tight">
              Smarter Debugging <br />
              Starts Here
            </h1>
            <p className="text-base sm:text-lg md:text-xl mb-6 sm:mb-7 md:mb-8 max-w-2xl mx-auto opacity-80 px-2">
              From error detection to validated fixes powered by intelligent agents. Scanner, Fixer,
              and Validator agents working together to improve your code.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center">
              <Link to="/debug" className="btn btn-primary btn-sm sm:btn-md md:btn-lg w-full sm:w-auto">
                Get Started
              </Link>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </>
  )
}

export default LandingPage
