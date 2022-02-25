import React from "react";
import SignIn from "./components/SignIn";
import Chat from "./components/Chat";
import { useAuthState } from 'react-firebase-hooks/auth'
import { auth } from "./Firebase";
function App() {

  const [user] = useAuthState(auth)

  return (
    <div className="m-4 p-4 bg-blue-100">
      {user ? <Chat /> : <SignIn />}
    </div>
  );
}

export default App;
