import { Link, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Index from "./pages/Index"
import User from "./pages/User"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="/home" element={<Home />} />
      <Route path="/user" element={<User />} />
    </Routes>
  )
}

export default App
