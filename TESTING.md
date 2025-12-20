# Testing Guide

## Quick Test Steps

### 1. Backend Test

```bash
cd backend

# Check setup
python check_setup.py

# Start the backend server
./start.sh
# OR
uvicorn app.main:app --reload
```

The backend should start on `http://localhost:8000`

**Test the API:**
- Open browser to `http://localhost:8000` - should see API info
- Open `http://localhost:8000/health` - should see health status

### 2. Frontend Test

```bash
cd frontend

# Start the frontend dev server
npm run dev
```

The frontend should start on `http://localhost:5173`

**Test the UI:**
1. Open `http://localhost:5173` in your browser
2. You should see the landing page
3. Click "Start Debugging" to go to the debugger
4. Try entering some buggy code (example below)
5. Click "Debug Code" and watch the agents work!

## Example Test Code

### Python (with bugs)
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: division by zero if empty list

result = calculate_average([])
print(result)
```

### JavaScript (with bugs)
```javascript
function findMax(arr) {
    let max = arr[0];
    for (let i = 1; i <= arr.length; i++) {  // Bug: off-by-one error
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

console.log(findMax([1, 5, 3, 9, 2]));
```

## Expected Behavior

1. **Scanner Agent** should detect the bugs
2. **Fixer Agent** should propose fixes
3. **Validator Agent** should validate the fixes
4. You should see real-time streaming updates in the UI
5. Final result should show the fixed code

## Troubleshooting

### Backend Issues

**"GEMINI_API_KEY not configured"**
- Make sure you've created `.env` file in backend directory
- Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

**"Module not found"**
- Run: `pip install -r requirements.txt`

**Port 8000 already in use**
- Change PORT in `.env` file
- Update `API_URL` in `frontend/src/components/Debugger.jsx`

### Frontend Issues

**"Failed to connect to debug server"**
- Make sure backend is running on port 8000
- Check browser console for CORS errors

**Blank page**
- Check browser console for errors
- Make sure all dependencies are installed: `npm install`

**Theme not working**
- Clear browser cache
- Check if DaisyUI is properly installed

## Development Tips

- Backend auto-reloads when you change Python files
- Frontend auto-reloads when you change React files
- Check terminal logs for detailed error messages
- Use browser DevTools Network tab to debug API calls
- Use browser DevTools Console for frontend errors
