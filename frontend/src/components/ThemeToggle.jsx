import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme()

    return (
        <label className="swap swap-rotate">
            <input type="checkbox" onChange={toggleTheme} checked={theme === 'light'} />
            <Sun className="swap-on h-6 w-6" />
            <Moon className="swap-off h-6 w-6" />
        </label>
    )
}
