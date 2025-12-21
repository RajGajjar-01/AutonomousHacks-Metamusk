import { Link } from 'react-router'
import { Github, Twitter, Linkedin } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="w-full flex flex-col items-center justify-center p-6 sm:p-8 md:p-10 bg-base-200 text-base-content rounded-t-2xl [data-theme='dark']:bg-black [data-theme='dark']:text-gray-400 mt-12 sm:mt-16 md:mt-20">
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-center text-sm sm:text-base mb-4 sm:mb-0 w-full">
        <Link to="/" className="link link-hover">
          Home
        </Link>
        <Link to="/debug" className="link link-hover">
          Debug Tool
        </Link>
      </div>
      <div className="mt-2 sm:mt-0">
        <div className="grid grid-flow-col gap-3 sm:gap-4">
          <a href="#" className="btn btn-ghost btn-circle btn-sm sm:btn-md">
            <Github className="w-4 h-4 sm:w-5 sm:h-5" />
          </a>
          <a href="#" className="btn btn-ghost btn-circle btn-sm sm:btn-md">
            <Twitter className="w-4 h-4 sm:w-5 sm:h-5" />
          </a>
          <a href="#" className="btn btn-ghost btn-circle btn-sm sm:btn-md">
            <Linkedin className="w-4 h-4 sm:w-5 sm:h-5" />
          </a>
        </div>
      </div>
      <div className="px-4 sm:px-0 mt-2 sm:mt-0">
        <p className="text-center text-sm sm:text-base">Copyright © {new Date().getFullYear()} - AutonomousHacks MetaMusk</p>
        <p className="text-center text-xs sm:text-sm opacity-70 mt-1">Empowering developers with AI debugging</p>
      </div>
    </footer>
  )
}

export default Footer
