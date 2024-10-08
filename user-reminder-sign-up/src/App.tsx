import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './index.css'
import Signup from './views/Signup'
import Checkout from './components/Checkout'


const App = () => (
  <div>
    <BrowserRouter>
      <Routes>
        <Route key='/' path='/' element={<Signup/>}></Route>
        <Route key='/checkout' path='/checkout' element={<Checkout productId='' emailAddress = ''/>}></Route>
      </Routes>
      
    </BrowserRouter>

  </div>
  
)

export default App;
