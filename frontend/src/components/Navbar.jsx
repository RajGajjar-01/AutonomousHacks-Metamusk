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
    <nav className="navbar bg-base-100/80 backdrop-blur-md border-b border-base-content/10 sticky top-0 z-50 px-4 lg:px-6 transition-all duration-300">
      <div className="navbar-start">
        {/* Mobile Menu Button */}
        <div className="dropdown lg:hidden">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle" onClick={toggleMenu}>
            {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </div>
          <ul
            tabIndex={0}
            className={`menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-base-100/95 backdrop-blur rounded-box w-52 border border-base-content/10 ${isMenuOpen ? 'block' : 'hidden'}`}
          >
            {navLinks.map(link => (
              <li key={link.path}>
                <Link
                  to={link.path}
                  className={`${location.pathname === link.path ? 'active font-bold' : ''} py-3`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Brand */}
        <Link to="/" className="font-bold text-2xl hover:bg-transparent">
          MetaMusk.ai
        </Link>
      </div>

      {/* Right Side: Links + Toggle */}
      <div className="navbar-end flex gap-4 items-center">
        {/* Desktop Menu */}
        <ul className="menu menu-horizontal px-1 hidden lg:flex gap-1">
          {navLinks.map(link => (
            <li key={link.path}>
              <Link
                to={link.path}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  location.pathname === link.path
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
