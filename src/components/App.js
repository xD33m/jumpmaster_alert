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
  const [status, setStatus] = useState(false);
  const [soundActivated, setSoundActivated] = useState(false);
  const [dicordDM, setDiscordDM] = useState(false);
  const [socket, setSocket] = useState();
  const [jumpDetectionRunning, setJumpDetectionRunning] = useState(false);

  const toggleLoading = (prevLogs, type) => {
    const oppositeType = type === "jumpmaster" ? "champion" : "jumpmaster";
    console.log(`logs (toggle)`, logs);
    const reverseArr = [...prevLogs].reverse();
    console.log(`reverseArr`, reverseArr);
    // if reverseArr contains oppositeType, change it's loading status to false
    if (reverseArr.find((log) => log.type === oppositeType)) {
      const index = reverseArr.findIndex((log) => log.type === oppositeType);
      reverseArr[index].loading = false;
    }
    const updatedArr = reverseArr.reverse();
    console.log(`updatedArr`, updatedArr);
    return updatedArr;
  };

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

    s.on("logs", (log) => {
      const [time] = new Date().toTimeString().split(" ");
      const fullLog = { time, message: log };
      // if (type === "jumpDetection" && loading === false) {
      //   // letzten log eintrag im state auf 'loading = false' setzten
      //   const reverseArr = [...prevLogs].reverse();
      //   reverseArr.find((log) => log.type === "jumpDetection").loading = false;
      //   const newArr = reverseArr.reverse();
      //   setLogs(newArr);
      // }
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    });

    s.on("detection_log", (detectionLog) => {
      const [time] = new Date().toTimeString().split(" ");
      const { type, message, loading } = detectionLog;
      const fullLog = { time, message, loading, type };

      setLogs((prevLogs) => {
        const updatedArr = toggleLoading(prevLogs, type);
        return [...updatedArr, fullLog];
      });

      if (type === "jumpmaster" && loading === true) {
        setJumpDetectionRunning(true);
      } else if (type === "champion" && loading === true) {
        console.log("charDetectionRunning");
        setJumpDetectionRunning(false);
      }

      // // check if there is something to update
      // if (loading === false && logs.filter((log) => log.loading === true).length > 0) {
      //   const updatedLogs = stopLoadingLog(type);
      //   setLogs(updatedLogs);

      // } else {
      //   setLogs((prevLogs) => [...prevLogs, fullLog]);
      // }

      // check if there is

      // setLogs((prevLogs) => [...prevLogs, fullLog]);
      // console.log(jumpDetection, charDetection);
      // setJumpDetectionRunning(jumpDetection);
      // setCharDetectionRunning(charDetection);
      // if (!jumpDetectionRunning && jumpDetection === true) {
      // } else if (jumpDetection === false) {
      //   setJumpDetectionRunning(false);
      // }

      // if(!charDetectionRunning && charDetection === true){

      // }
    });

    return () => {
      s.close();
    };
  }, []);

  const removeAllLoadingStates = () => {
    setLogs(
      logs.map((log) => {
        if (log?.loading === true) {
          log.loading = false;
          return log;
        }
        return log;
      })
    );
  };

  const startAndStop = () => {
    if (status === true) {
      socket.emit("toggle", { type: "startAndStop", status: false });
      setStatus(false);
      removeAllLoadingStates();
    } else {
      socket.emit("toggle", { type: "startAndStop", status: true });
      setStatus(true);
    }
  };

  const soundToggle = () => {
    if (soundActivated === true) {
      socket.emit("toggle", { type: "sound", status: false });
      setSoundActivated(false);
    } else {
      socket.emit("toggle", { type: "sound", status: true });
      setSoundActivated(true);
    }
  };

  const discordDMToggle = () => {
    if (dicordDM === true) {
      socket.emit("toggle", { type: "discordDM", status: false });
      setDiscordDM(false);
    } else {
      socket.emit("toggle", { type: "discordDM", status: true });
      setDiscordDM(true);
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
            soundToggle={soundToggle}
            discordDMToggle={discordDMToggle}
          />
        </div>
        <div className={styles.col}>
          <Terminal
            logs={logs}
            setLogs={setLogs}
            jumpDetectionRunning={jumpDetectionRunning}
            setJumpDetectionRunning={setJumpDetectionRunning}
            removeAllLoadingStates={removeAllLoadingStates}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
