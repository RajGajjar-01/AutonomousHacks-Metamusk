import { Link } from 'react-router'
import { Github, Twitter, Linkedin } from 'lucide-react'                                                                      

const Footer = () => {
  return (
    <footer className="footer footer-center p-10 bg-base-200 text-base-content rounded-t-2xl [data-theme='dark']:bg-black [data-theme='dark']:text-gray-400 mt-20">
      <div className="grid grid-flow-col gap-4">
        <Link to="/" className="link link-hover">
          Home
        </Link>
        <Link to="/debug" className="link link-hover">
          Debug Tool
        </Link>
      </div>
      <div>
        <div className="grid grid-flow-col gap-4">
          <a href="#" className="btn btn-ghost btn-circle">
            <Github className="w-5 h-5" />
          </a>
          <a href="#" className="btn btn-ghost btn-circle">
            <Twitter className="w-5 h-5" />
          </a>
          <a href="#" className="btn btn-ghost btn-circle">
            <Linkedin className="w-5 h-5" />
          </a>
        </div>
      </div>
      <div>
        <p>Copyright © {new Date().getFullYear()} - AutonomousHacks MetaMusk</p>
        <p className="text-sm opacity-70">Empowering developers with AI debugging</p>
      </div>
    </footer>
  )
}

export default Footer
