import ThemeToggle from './ThemeToggle'
import { Link, useLocation } from 'react-router'
import { Menu, X } from 'lucide-react'
import { useState } from 'react'

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()

  // Helper to determine active link class
  const getLinkClass = path => {
    return location.pathname === path
      ? 'btn btn-sm btn-primary'
      : 'btn btn-sm btn-ghost hover:bg-base-200'
  }

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen)

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Debug', path: '/debug' },
  ]

  return (
    <nav className="navbar bg-base-100/80 backdrop-blur-md border-b border-base-content/10 sticky top-0 z-50 px-3 sm:px-4 md:px-6 lg:px-8 transition-all duration-300 min-h-[60px] sm:min-h-[64px]">
      <div className="navbar-start">
        {/* Mobile Menu Button */}
        <div className="relative lg:hidden">
          <button className="btn btn-ghost btn-circle btn-sm sm:btn-md" onClick={toggleMenu}>
            {isMenuOpen ? <X className="h-4 w-4 sm:h-5 sm:w-5" /> : <Menu className="h-4 w-4 sm:h-5 sm:w-5" />}
          </button>

          {isMenuOpen && (
            <ul className="absolute top-full left-0 mt-3 p-2 shadow-lg bg-base-100/95 backdrop-blur rounded-box w-48 sm:w-52 border border-base-content/10 flex flex-col gap-1 z-[100]">
              {navLinks.map(link => (
                <li key={link.path}>
                  <Link
                    to={link.path}
                    className={`block px-4 py-2.5 sm:py-3 rounded-lg text-sm sm:text-base hover:bg-base-200 transition-colors ${location.pathname === link.path ? 'bg-primary/10 text-primary font-bold' : ''
                      }`}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Brand */}
        <Link to="/" className="font-bold text-lg sm:text-xl md:text-2xl text-gradient hover:bg-transparent ml-2 sm:ml-0">
          MetaMusk.AI
        </Link>
      </div>

      {/* Right Side: Links + Toggle */}
      <div className="navbar-end flex gap-2 sm:gap-3 md:gap-4 items-center">
        {/* Desktop Menu */}
        <ul className="menu menu-horizontal px-1 hidden lg:flex gap-1">
          {navLinks.map(link => (
            <li key={link.path}>
              <Link
                to={link.path}
                className={`px-3 md:px-4 py-2 rounded-lg transition-colors text-sm md:text-base ${location.pathname === link.path
                  ? 'bg-primary/10 text-primary font-bold'
                  : 'hover:bg-base-200 text-base-content/80 hover:text-base-content'
                  }`}
              >
                {link.name}
              </Link>
            </li>
          ))}
        </ul>

        <div className="divider divider-horizontal mx-0 hidden lg:flex h-6 self-center opacity-20"></div>

        <ThemeToggle />
      </div>
    </nav>
  )
}

export default Navbar
