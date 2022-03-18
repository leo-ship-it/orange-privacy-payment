import logo from './logo.svg';
import './App.css';
import OnboardingButton from "./component/ButtonMetamask";
import Account from './component/Account';
import DeployNewToken from "./component/DeployNewToken";

function App() {
  return (
    <div className="App">
      <OnboardingButton />
      <Account />
    </div>
  );
}

export default App;
