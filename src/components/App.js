import React, { useState } from "react";

import Titlebar from "components/titlebar/Titlebar";

import logo from "logo.svg";
import styles from "components/App.module.scss";
import { get } from "../utils/requests";

function App() {
  const [isRunning, setIsRunning] = useState(false);

  const startAndStop = () => {
    if (!isRunning) {
      get(
        "start", // Route
        (response) => console.log("start", response), // Response callback
        (error) => console.error("Error Starting...", error) // Error callback
      );
      setIsRunning(true);
    } else {
      get(
        "stop", // Route
        (response) => console.log("stop", response), // Response callback
        (error) => console.error("Error Stopping...", error) // Error callback
      );
      setIsRunning(false);
    }
  };

  return (
    <>
      <Titlebar />

      <div className={styles.app}>
        <header className={styles["app-header"]}>
          <img src={logo} className={styles["app-logo"]} alt="logo" />
          <p>Apex Jumpmaster Detection</p>
          <button
            type="button"
            className={styles.button}
            aria-label="Increment value"
            onClick={startAndStop}
          >
            {isRunning ? "Stop" : "Start"}
          </button>
        </header>
      </div>
    </>
  );
}

export default App;
