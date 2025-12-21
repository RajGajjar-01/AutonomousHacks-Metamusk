import { Link } from 'react-router'
import Snowfall from 'react-snowfall'
import Footer from './Footer'

const LandingPage = () => {
  return (
    <>
      <div>
        <div className="fixed inset-0 w-full h-full pointer-events-none -z-10 overflow-hidden">
          <Snowfall snowflakeCount={30} />
        </div>
        {/* Gradient Background - Emerging from bottom, covering entire screen */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute bottom-[200px] left-1/2 -translate-x-1/2 w-full max-w-[1400px] h-[900px] bg-gradient-to-t from-primary/20 via-secondary/15 to-transparent blur-[250px] rounded-full"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-4">
          <div className="text-center max-w-3xl">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Smarter Debugging <br />
              Starts Here
            </h1>
            <p className="text-lg mb-8 max-w-2xl mx-auto opacity-80">
              From error detection to validated fixes powered by intelligent agents.Scanner, Fixer,
              and Validator agents working together to improve your code.
            </p>
            <div className="flex gap-4 justify-center">
              <Link to="/debug" className="btn btn-primary btn-lg">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </>
  )
}

export default LandingPage
