import React, { useEffect, useState } from "react";
import io from "socket.io-client";

import styles from "components/App.module.scss";
import Titlebar from "components/titlebar/Titlebar";
import Terminal from "./terminal/Terminal";
import SettingsPanel from "./settingsPanel/SettingsPanel";

const { ipcRenderer } = window.require("electron");
const port = ipcRenderer.sendSync("get-port-number");

function App() {
  const [darkTheme, setTheme] = useState(false);
  const [logs, setLogs] = useState([]);
  const [socketStatus, setSocketStatus] = useState(false);
  const [status, setStatus] = useState("Off");
  const [socket, setSocket] = useState();

  useEffect(() => {
    const s = io(`http://localhost:${port}`);
    setSocket(s);

    s.on("connect", () => {
      setSocketStatus(true);
      console.log("Connected to socket");
    });

    s.on("disconnect", () => {
      setSocketStatus(false);
      console.log("Disconnected to socket");
    });

    s.on("status", (message) => {
      setStatus(message.status);
      console.log("status", message.status);
    });

    s.on("logs", (log) => {
      const [time] = new Date().toTimeString().split(" ");
      const fullLog = { time, log };
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    });

    return () => {
      s.close();
    };
  }, []);

  const startAndStop = () => {
    if (status === "On") {
      socket.emit("message", { data: "Stop Jumpmaster Alert", status: "Off" });
      setStatus("Off");
    } else {
      socket.emit("message", { data: "Start Jumpmaster Alert", status: "On" });
      setStatus("On");
    }
  };

  return (
    <div className={`${styles.main} ${darkTheme ? styles.dark : styles.light}`}>
      <Titlebar darkTheme={darkTheme} />

      <div className={styles["app-header"]}>
        <div className={styles.col}>
          <SettingsPanel
            setTheme={setTheme}
            darkTheme={darkTheme}
            socketStatus={socketStatus}
            status={status}
            startAndStop={startAndStop}
          />
        </div>
        <div className={styles.col}>
          <Terminal logs={logs} setLogs={setLogs} />
        </div>
      </div>
    </div>
  );
}

export default App;
