import React from "react";
import { Switch, Route } from "react-router-dom";
import LoginComponent from "./Login";
import Home from "./Home";

function App() {
  return (
    <div>
      <Switch>
        <Route path="/login" component={LoginComponent} />
        <Route path="/" component={Home} />
      </Switch>
    </div>
  );
}

export default App;
