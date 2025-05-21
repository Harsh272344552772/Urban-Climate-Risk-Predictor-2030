
import { Routes, Route } from 'react-router-dom'
import Index from './pages/Index'
import Contact from './pages/Contact'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Predict from './pages/Predict'
import { useToast } from './hooks/use-toast'
import { useEffect } from 'react'

function App() {
  const { toast } = useToast();
  
  useEffect(() => {
    // Check if Flask API is available
    fetch('/api/climate-data')
      .catch(error => {
        console.error("Flask API connection error:", error);
        toast({
          title: "Backend Connection Issue",
          description: "Could not connect to the Flask backend. Some features may not work.",
          variant: "destructive"
        });
      });
  }, [toast]);

  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/predict" element={<Predict />} />
    </Routes>
  )
}

export default App
