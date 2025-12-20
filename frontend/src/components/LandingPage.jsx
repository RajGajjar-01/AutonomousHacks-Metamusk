import Footer from './Footer'

const LandingPage = () => {
    return (
        <>
            
            <div>
                {/* Gradient Background - Emerging from bottom, covering entire screen */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute bottom-[-300px] left-1/2 -translate-x-1/2 w-full max-w-[1400px] h-[900px] bg-gradient-to-t from-blue-600/50 via-purple-500/30 to-transparent blur-[150px] rounded-full"></div>
                </div>
                
                {/* Content */}
                <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
                    <div className="text-center max-w-3xl">
                        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                            Smarter Debugging <br/>
                            Starts Here
                        </h1>
                        <p className="text-lg mb-8 max-w-2xl mx-auto opacity-80">
                            From error detection to validated fixes powered by intelligent agents.Scanner, Fixer, and Validator agents working together to improve your code.
                        </p>
                        <div className="flex gap-4 justify-center">
                    
                            <button className="px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition shadow-lg">
                                Get Started
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <Footer/>
        </>
    )
}

export default LandingPage
