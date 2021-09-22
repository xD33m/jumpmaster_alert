import React from "react";

import Titlebar from "components/titlebar/Titlebar";

import logo from "logo.svg";
import styles from "components/App.module.scss";

function App() {
  return (
    <>
      <Titlebar />

      <div className={styles.app}>
        <header className={styles["app-header"]}>
          <img src={logo} className={styles["app-logo"]} alt="logo" />
          <p>Apex Jumpmaster Detection</p>
        </header>
      </div>
    </>
  );
}

export default App;
